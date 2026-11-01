# Customization keywords after /generate

Space-separated `key:value` tokens. Values with spaces use double quotes. Unknown keys join the free-subject string.

## Required-enough

| Key | Values | Default |
|---|---|---|
| type | slug from power-rank.md | inferred, else catalog |
| subject | nouns the prompt must name | remainder after keys |
| brand | aether, aether-cinema, house, or a proper name | aether when type is video or when gnitekram is present; else house |

## Audience and use

| Key | Values | Default |
|---|---|---|
| use | marketing, academic, pitch, product, studio | marketing |
| audience | investors, scholars, clients, operators, public | inferred from use |
| tone | awe, clinical, ceremonial, nocturnal, precision | awe + precision |

## Picture and motion

| Key | Values | Default |
|---|---|---|
| aspect | 16:9, 21:9, 9:16, 1:1, 4:5 | 16:9 stills; 21:9 hero video |
| duration | Ns or N seconds | 8s for video |
| camera | macro, three-quarter, aerial, tracking, locked-off | three-quarter |
| light | gold-rim, violet-rim, dawn, nocturnal, surgical | gold-rim plus volumetric |
| material | named surfaces only | brand materials |
| setting | named place only | brand setting |
| motion | dolly-in, orbit, rack, hold, extend | slow dolly-in for video |
| count | integer stills or shots | 1 still; 6 shots for video |

## Product and document

| Key | Values | Default |
|---|---|---|
| pages | comma list | studio,gate,timeline for Aether web-app |
| stack | comma list of builder flags | none |
| length | pages or words | folio compact; coffee page count |
| run | true, false | false (prompt only) |

## Aether / gnitekram extras

| Key | Values | Default |
|---|---|---|
| mode | t2v, i2v, extend, lipsync, recast, audio | t2v |
| cast | fictional character slugs | unnamed 21+ fictional adult |
| policy | strict, standard | strict |
| studio | https://gnitekram.org/ | that URL |

Free words after the keys become the subject lock. Example remainder

```
video brand:aether duration:12s camera:tracking subject:obsidian gate, gold filament, 21+ attendant
```
