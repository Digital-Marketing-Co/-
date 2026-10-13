---
name: ringtone
description: Build an iPhone-safe ringtone pack from a prompt, TTS line, or source audio. Trigger on /ringtone, custom ringtone, M4R, iPhone 16 Pro Max tone, iPhone 12 Pro Max tone, GarageBand export, Use as Ringtone, or convert audio to a 30-second AAC ringtone. Portable for Grok and other generative AI apps.
metadata:
  type: workflow
  version: "3.0"
  flag: /ringtone
  updatable: true
---

# /ringtone — iPhone-safe tone from a prompt or file

Turn a text prompt, a spoken line, or any DRM-free audio into a dual-path ringtone pack that installs on both iPhone 16 Pro Max and iPhone 12 Pro Max.

Always emit three files with the same stem:

- `.m4r` — AAC-LC in an MPEG-4 container. This is the classic iOS Tones format.
- `.m4a` — AAC sibling for iOS 26 Files Use as Ringtone.
- `.mp3` — 160 kbps CBR fallback for iOS 26 Files and Android.

Hard product spec (do not relax):

- Duration at most 30.00 seconds. Prefer 8–20 seconds for a call loop.
- AAC-LC, 44100 Hz, 1 or 2 channels, 160k CBR.
- No video stream, no attached album-art video, no FairPlay/DRM.
- Fade-in about 40 ms, fade-out about 120 ms, integrated loudness near -14 LUFS, true peak at most -1.5 dBTP.
- High-pass 80 Hz, low-pass 15 kHz so the tone survives both the iPhone 12 Pro Max stereo speakers and the louder iPhone 16 Pro Max speakers.

Skill root is /root/.grok/server-skills/ringtone.

If the user only asked to create or revise this skill and supplied no prompt or file, stop after the skill files exist.

## Read on demand

- references/iphone-spec.md — container, codec, length, install paths by iOS generation
- references/prompt-to-audio.md — how an agent should obtain source audio from a prompt
- scripts/make_ringtone.py — deterministic encoder and validator

## Workflow

### 1. Collect input

Need one of:

1. An attached or local audio/video file (--input)
2. A spoken line to synthesize with the Voice connector, then --input on the MP3
3. A musical or SFX prompt. Obtain audio first (see references/prompt-to-audio.md), then encode
4. --generate-motif only as a last-resort demo tone, never as a substitute for a user-described sound

Optional flags: --start, --duration (capped at 30), --title, --channels 1 or 2.

### 2. Obtain source audio if the user gave only text

Order of preference:

1. User-supplied file
2. Voice connector for speech or spoken-word ringtones (voice_generate_speech to an .mp3)
3. User-hosted or previously generated clip (Suno, Udio, MusicGen, GarageBand, Voice Memos)
4. Motif generator inside make_ringtone.py for a proof-of-pipeline file only

This environment does not ship a music-foundation model. Do not pretend a sine motif matches a cinematic or song prompt. Say so, encode the closest available clip, and tell the user where to drop a generated WAV/MP3 for a second pass.

### 3. Encode

```bash
python3 /root/.grok/server-skills/ringtone/scripts/make_ringtone.py \
  --input /path/to/source.wav \
  --title "short-title" \
  --prompt "user prompt text" \
  --start 0 \
  --duration 30 \
  --outdir /workspace/artifacts
```

No source file, demo only:

```bash
python3 /root/.grok/server-skills/ringtone/scripts/make_ringtone.py \
  --generate-motif --title demo-motif --duration 12 \
  --outdir /workspace/artifacts
```

The script prints a JSON validation report. Exit code 1 means the pack is not iPhone-safe. Do not deliver a failing pack.

### 4. Install instructions to give the user

iPhone 12 Pro Max (and any iOS before the Files Use as Ringtone sheet):

1. AirDrop or USB-copy the .m4r
2. Open it, or import into GarageBand and Share, then Ringtone
3. Settings, Sounds and Haptics, Ringtone, Custom

iPhone 16 Pro Max on iOS 26+:

1. Save the .m4a or .mp3 into On My iPhone in Files (not only iCloud)
2. Share, then Use as Ringtone
3. Same Settings path to assign it default or per-contact

Keep the .m4r in every pack so one file still works if the phone is on iOS 17 or 18.

### 5. Reply

Give, in this order:

1. Paths to .m4r, .m4a, .mp3
2. Measured duration, codec, sample rate, size
3. Which install path to use on 12 Pro Max vs 16 Pro Max
4. What source was used (user file, TTS, external generator, demo motif)

Do not claim Apple certification. Do not ship copyrighted commercial tracks unless the user supplied a file they own.

## Agent portability

Other generative apps can copy this folder. Minimum runtime:

- ffmpeg and ffprobe on PATH
- Python 3.10+ (stdlib only)
- Optional Voice / music model for prompt-to-waveform

The product contract is the JSON report plus the three files. Do not invent a fourth container.


## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
