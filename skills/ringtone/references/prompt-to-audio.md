# Prompt to waveform

The ringtone skill encodes. It does not compose a song model. Agents must obtain a waveform first.

## Speech or spoken hook

Use the Voice connector.

```
voice_generate_speech
  text: the spoken line, kept under ~20 seconds of speech
  dest_path: /home/workdir/artifacts/tts-source.mp3
```

Then:

```
python3 /home/workdir/.grok/skills/ringtone/scripts/make_ringtone.py \
  --input /home/workdir/artifacts/tts-source.mp3 \
  --title spoken-hook
```

Write the line the way it should be heard, not as a music-prompt paragraph. Example: "Hey. It's me. Pick up."

## Musical or cinematic prompt

This sandbox has ffmpeg, not Suno/Udio/MusicGen weights. Do the following in order:

1. Ask the user for a generated WAV/MP3 they already made.
2. If the host app exposes a music tool, call that tool, save locally, then encode.
3. If the user wants a proof file now, run `--generate-motif` and label it as a pipeline demo, not as fulfillment of a film-score prompt.

A good music prompt for an external generator, tuned for ringtones:

- One motif, not a full verse-chorus
- 10–18 seconds
- Strong attack in the first 300 ms (the phone must identify the owner immediately)
- Midrange-forward instrumentation (pluck, bell, brass stab, vocal chop)
- No long ambient pad as the only event
- No lyrics that collide with a real commercial recording the user does not own

## Video as source

ffmpeg will take the first audio stream. Pass `--start` and `--duration` to grab the hook. The encoder strips video (`-vn`).

## Legal

Only encode audio the user owns, recorded, or generated under a license that allows a personal ringtone. Do not rip Apple Music. Do not reconstruct a copyrighted chorus from memory and call it original.
