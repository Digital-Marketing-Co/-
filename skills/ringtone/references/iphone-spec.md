# iPhone ringtone product spec

## Container and codec

An `.m4r` file is an MPEG-4 audio file whose only material difference from `.m4a` is the extension. iOS uses that extension as a Tones library flag.

Required encode:

| Field | Value | Why |
| --- | --- | --- |
| Container | MPEG-4 (`-f mp4`) | What iOS Tones expects |
| Extension | `.m4r` plus a sibling `.m4a` | Classic path + iOS 26 Files path |
| Codec | AAC-LC (`-profile:a aac_low`) | Device-native decoder since iPhone 12 |
| Sample rate | 44100 Hz | iOS tone pipeline default |
| Channels | 1 or 2 | Stereo is fine; mono is smaller and often clearer on a desk |
| Bitrate | 128–192 kbps CBR; default 160k | Phone speakers do not reward 256k+ |
| Duration | `<= 30.00 s` | GarageBand export and iOS 26 Files both reject longer clips |
| DRM | none | Apple Music / FairPlay files cannot become tones |
| Extra streams | none | Strip video, chapters, album-art video |

Some third-party pages quote a 40-second / 40 MB ceiling. Treat those as desktop-tool folklore. GarageBand still trims to 30 seconds. iOS 26 Files says the file is too large when the clip is longer than 30 seconds. Encode to 30.00 or less.

Typical pack size at 160 kbps / 15 s is about 300 KB. That is normal.

## Device matrix

| Device | Audio hardware note | Install path that always works | Bonus path |
| --- | --- | --- | --- |
| iPhone 12 Pro Max | Stereo speakers, weaker low end | `.m4r` via GarageBand, Finder/iTunes, or Files open | iOS 26 Files only if that unit received iOS 26 |
| iPhone 16 Pro Max | Louder, wider band, Adaptive Audio | Same `.m4r` | iOS 26 Files on `.m4a` or `.mp3` ≤ 30 s stored On My iPhone |

Master once for both. Do not ship two loudness versions. A tone peaked at `-1.5 dBTP` and landed near `-14 LUFS` reads on the quieter 12 Pro Max without harsh clipping on the 16 Pro Max.

## iOS generation split

Pre-iOS 26 (the safe assumption for many 12 Pro Max units):

- The system ringtone list is fed by the Tones library.
- Practical injectors: GarageBand "Share → Ringtone", Finder/iTunes tone sync, or opening a well-formed `.m4r`.

iOS 26+:

- Files can offer "Use as Ringtone" for local MP3 / M4A / M4R / WAV / AAC / AIFF / FLAC / AMR clips that are 30 seconds or shorter.
- The file must live in Files as a local item. An iCloud-only pointer often will not show the action.
- Protected Apple Music tracks still fail.

Because the 12 Pro Max may or may not be on iOS 26 in a given household, the encoder always writes `.m4r`.

## Psychoacoustic notes for phone speakers

- Cut rumble below 80 Hz. It eats headroom and never leaves the 12 Pro Max cabinet cleanly.
- Keep energy in 800 Hz–5 kHz. That band is what a phone on a table actually projects.
- Avoid a hard edit at t=0 or t=end. A 40 ms fade-in and 120 ms fade-out prevent the click that iOS then loops.
- Do not brickwall to 0 dBFS. iOS applies its own output limiter on top of a ringtone.

## What will make iOS reject the file

- Duration over 30 s
- DRM / FairPlay
- Wrong extension with a non-AAC payload (renaming `.mp3` to `.m4r` without re-encoding)
- A video track left in the MP4
- File reachable only through a cloud placeholder
- Source is a streaming preview rather than a local file
