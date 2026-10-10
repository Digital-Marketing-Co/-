# Cover title

Page 1 is a unifying still of the whole subject, then a composited title.

Faces live in the skill tree. The old SlidesCarnival paths are not on this host and were dropping the title to a bitmap font.

- Title: assets/fonts/Cinzel-Variable.ttf at weight 700
- Fallback title: assets/fonts/PlayfairDisplay-Variable.ttf at weight 700
- Subtitle and company line: assets/fonts/CormorantGaramond-Italic-Variable.ttf
- Last fallback: /usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf

The title is 3 to 8 words. Subtitle is optional, at most 12 words. Do not ask the generate step to paint the title.

Veil only the lower third so the still still touches the top trim. Company line on the cover is Digital Marketing Co., which matches the link title. No running footer on later pages.

Command:

```bash
python3 /root/.grok/server-skills/coffee/scripts/composite_cover.py \
  stills/fit-01.png stills/cover.png \
  --title "TITLE" --subtitle "SUBTITLE"
```
