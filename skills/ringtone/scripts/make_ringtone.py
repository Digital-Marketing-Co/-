#!/usr/bin/env python3
"""Encode any audio (or a generated motif) into an iPhone-safe ringtone pack.

Outputs a dual-compatible pack for iPhone 12 Pro Max and iPhone 16 Pro Max:
  .m4r  AAC in MPEG-4  — classic Tones / GarageBand / Finder / iTunes path
  .m4a  same AAC       — iOS 26 Files "Use as Ringtone" path
  .mp3  CBR            — iOS 26 Files fallback and Android

Hard constraints (fail closed):
  duration <= 30.00 s
  AAC-LC, 44100 Hz, 1 or 2 channels
  no video, no album art video stream, no DRM
  peak <= -1.0 dBTP after loudnorm
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MAX_SECONDS = 30.0
TARGET_SR = 44100
TARGET_BITRATE = "160k"
TARGET_LUFS = -14.0
TARGET_TP = -1.5
TARGET_LRA = 11.0


def die(msg: str, code: int = 2) -> None:
    print(json.dumps({"ok": False, "error": msg}), file=sys.stderr)
    raise SystemExit(code)


def run(cmd: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=False,
        capture_output=capture,
        text=True,
    )


def probe(path: str) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        path,
    ]
    p = run(cmd, capture=True)
    if p.returncode != 0:
        die(f"ffprobe failed on {path}: {p.stderr.strip()}")
    return json.loads(p.stdout or "{}")


def duration_of(path: str) -> float:
    info = probe(path)
    fmt = info.get("format") or {}
    try:
        return float(fmt.get("duration") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def first_audio_stream(info: dict) -> dict:
    for s in info.get("streams") or []:
        if s.get("codec_type") == "audio":
            return s
    return {}


def slugify(name: str) -> str:
    keep = []
    for ch in name.strip().lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in "-_ " and (not keep or keep[-1] != "-"):
            keep.append("-")
    s = "".join(keep).strip("-")
    return s[:60] or "ringtone"


def generate_motif(dest: Path, seconds: float = 12.0) -> None:
    """A short two-voice motif that survives phone speakers (no source file)."""
    seconds = min(max(seconds, 2.0), MAX_SECONDS)
    # A4 / E5 pentatonic-ish stabs that read on small speakers.
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        (
            f"sine=frequency=440:sample_rate={TARGET_SR}:duration={seconds},"
            "volume=0.45"
        ),
        "-f",
        "lavfi",
        "-i",
        (
            f"sine=frequency=659.25:sample_rate={TARGET_SR}:duration={seconds},"
            "volume=0.28"
        ),
        "-f",
        "lavfi",
        "-i",
        (
            f"sine=frequency=880:sample_rate={TARGET_SR}:duration={seconds},"
            "volume=0.12"
        ),
        "-filter_complex",
        (
            "[0:a][1:a][2:a]amix=inputs=3:normalize=0,"
            "afade=t=in:st=0:d=0.02,"
            f"afade=t=out:st={max(0.2, seconds - 0.18):.3f}:d=0.18,"
            "highpass=f=90,lowpass=f=12000"
        ),
        "-c:a",
        "pcm_s16le",
        "-ar",
        str(TARGET_SR),
        "-ac",
        "2",
        str(dest),
    ]
    p = run(cmd, capture=True)
    if p.returncode != 0 or not dest.exists():
        die(f"motif generation failed: {p.stderr[-800:]}")


def loudnorm_filter(measured: dict | None = None) -> str:
    if not measured:
        return (
            f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json"
        )
    return (
        f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:"
        f"measured_I={measured['input_i']}:"
        f"measured_TP={measured['input_tp']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:"
        "linear=true:print_format=summary"
    )


def measure_loudnorm(src: str, af_prefix: str) -> dict | None:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        src,
        "-af",
        f"{af_prefix},{loudnorm_filter(None)}" if af_prefix else loudnorm_filter(None),
        "-f",
        "null",
        "-",
    ]
    p = run(cmd, capture=True)
    blob = p.stderr or ""
    start = blob.rfind("{")
    end = blob.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        data = json.loads(blob[start : end + 1])
        needed = (
            "input_i",
            "input_tp",
            "input_lra",
            "input_thresh",
            "target_offset",
        )
        if all(k in data for k in needed):
            return data
    except json.JSONDecodeError:
        return None
    return None


def encode(
    src: str,
    dest: Path,
    codec: str,
    start: float,
    length: float,
    channels: int,
    fade_in: float,
    fade_out: float,
    measured: dict | None,
) -> None:
    fade_out_start = max(0.0, length - fade_out)
    parts = [
        f"atrim=start={start}:duration={length}",
        "asetpts=PTS-STARTPTS",
        "highpass=f=80",
        "lowpass=f=15000",
        f"afade=t=in:st=0:d={fade_in}",
        f"afade=t=out:st={fade_out_start:.3f}:d={fade_out}",
        loudnorm_filter(measured) if measured else f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}",
    ]
    af = ",".join(parts)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        src,
        "-vn",
        "-sn",
        "-dn",
        "-map",
        "0:a:0",
        "-af",
        af,
        "-ar",
        str(TARGET_SR),
        "-ac",
        str(channels),
        "-threads",
        "4",
    ]
    if codec == "aac":
        cmd += [
            "-c:a",
            "aac",
            "-profile:a",
            "aac_low",
            "-b:a",
            TARGET_BITRATE,
            "-movflags",
            "+faststart",
            "-f",
            "mp4",
        ]
    elif codec == "mp3":
        cmd += ["-c:a", "libmp3lame", "-b:a", "160k", "-f", "mp3"]
    else:
        die(f"unknown codec {codec}")
    cmd.append(str(dest))
    p = run(cmd, capture=True)
    if p.returncode != 0 or not dest.exists():
        die(f"encode failed for {dest.name}: {p.stderr[-1000:]}")


def validate_pack(files: dict[str, str]) -> dict:
    report = {"ok": True, "files": {}}
    for kind, path in files.items():
        info = probe(path)
        stream = first_audio_stream(info)
        dur = float((info.get("format") or {}).get("duration") or 0)
        size = int((info.get("format") or {}).get("size") or 0)
        entry = {
            "path": path,
            "duration_s": round(dur, 3),
            "bytes": size,
            "codec": stream.get("codec_name"),
            "profile": stream.get("profile"),
            "sample_rate": int(stream.get("sample_rate") or 0),
            "channels": int(stream.get("channels") or 0),
            "bit_rate": int((info.get("format") or {}).get("bit_rate") or 0),
        }
        reasons = []
        if dur <= 0.2:
            reasons.append("too short")
        if dur > MAX_SECONDS + 0.05:
            reasons.append(f"duration {dur:.3f}s exceeds 30s")
        if kind in ("m4r", "m4a"):
            if stream.get("codec_name") not in ("aac",):
                reasons.append(f"codec {stream.get('codec_name')} is not aac")
            if int(stream.get("sample_rate") or 0) != TARGET_SR:
                reasons.append("sample rate is not 44100")
        if reasons:
            report["ok"] = False
            entry["errors"] = reasons
        report["files"][kind] = entry
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Build an iPhone-safe ringtone pack.")
    ap.add_argument("--input", help="Source audio or video with audio.")
    ap.add_argument("--prompt", default="", help="Kept for agents; used as title slug.")
    ap.add_argument("--title", default="", help="Output basename.")
    ap.add_argument("--outdir", default="/home/workdir/artifacts")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--duration", type=float, default=MAX_SECONDS)
    ap.add_argument("--channels", type=int, default=2, choices=(1, 2))
    ap.add_argument("--fade-in", type=float, default=0.04)
    ap.add_argument("--fade-out", type=float, default=0.12)
    ap.add_argument(
        "--generate-motif",
        action="store_true",
        help="Synthesize a speaker-safe motif when no input is given.",
    )
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        die("ffmpeg and ffprobe are required")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    title = slugify(args.title or args.prompt or Path(args.input or "ringtone").stem)

    tmpdir = Path(tempfile.mkdtemp(prefix="ringtone-"))
    try:
        src = args.input
        if not src:
            if not args.generate_motif and not args.prompt:
                die("pass --input PATH or --generate-motif")
            motif = tmpdir / "motif.wav"
            generate_motif(motif, min(args.duration, 12.0))
            src = str(motif)
        if not os.path.isfile(src):
            die(f"input not found: {src}")

        info = probe(src)
        if not first_audio_stream(info):
            die("no audio stream in input")
        src_dur = duration_of(src)
        if src_dur <= 0.05:
            die("input duration is effectively zero")

        start = max(0.0, args.start)
        if start >= src_dur:
            die(f"--start {start} is past the source ({src_dur:.3f}s)")
        length = min(args.duration, MAX_SECONDS, src_dur - start)
        if length < 0.4:
            die("usable length is under 0.4s")

        measure_src = src
        af_prefix = (
            f"atrim=start={start}:duration={length},asetpts=PTS-STARTPTS,"
            "highpass=f=80,lowpass=f=15000"
        )
        measured = measure_loudnorm(src, af_prefix)

        m4r = outdir / f"{title}.m4r"
        m4a = outdir / f"{title}.m4a"
        mp3 = outdir / f"{title}.mp3"
        tmp_m4r = tmpdir / "out.m4r"
        tmp_mp3 = tmpdir / "out.mp3"

        encode(
            measure_src,
            tmp_m4r,
            "aac",
            start,
            length,
            args.channels,
            args.fade_in,
            args.fade_out,
            measured,
        )
        encode(
            measure_src,
            tmp_mp3,
            "mp3",
            start,
            length,
            args.channels,
            args.fade_in,
            args.fade_out,
            measured,
        )
        shutil.copy2(tmp_m4r, m4r)
        shutil.copy2(tmp_m4r, m4a)
        shutil.copy2(tmp_mp3, mp3)

        report = validate_pack({"m4r": str(m4r), "m4a": str(m4a), "mp3": str(mp3)})
        report["title"] = title
        report["prompt"] = args.prompt
        report["source"] = os.path.abspath(src) if args.input else "generated-motif"
        report["window"] = {"start_s": start, "duration_s": round(length, 3)}
        report["targets"] = {
            "iphone_12_pro_max": "use .m4r via GarageBand, Finder, or Files if iOS allows",
            "iphone_16_pro_max": "use .m4r or iOS 26 Files on .m4a/.mp3 <= 30s",
        }
        report["install"] = {
            "classic_m4r": [
                "AirDrop or USB-copy the .m4r onto the phone",
                "Open the .m4r in Files",
                "Or GarageBand > share as Ringtone",
                "Settings > Sounds & Haptics > Ringtone > Custom",
            ],
            "ios26_files": [
                "Save .m4a or .mp3 into On My iPhone in Files",
                "Share > Use as Ringtone (file must be <= 30s)",
            ],
        }
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
