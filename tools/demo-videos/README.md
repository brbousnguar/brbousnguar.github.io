# Demo videos

Short captioned product demos for the project pages (and for sharing), recorded
from the **real** app and edited by script, so a re-take is one command.

1. **Record**: Playwright drives the running app at 1920×1080 (page zoomed 1.5×),
   captures Chrome screencast frames with timestamps, draws a visible cursor with
   click ripples, and writes `marks.json` (when each step happened).
2. **Stage**: `node stage.mjs <name>` turns the frames into numbered 30 fps JPEGs in
   `remotion/public/frames-<name>/` and copies the site fonts.
3. **Edit**: Remotion (`remotion/src/`) plays those frames with exact time remapping:
   speed-ups labelled with a badge, holds, a camera that eases between focus points,
   captions, and title/end cards in the site's Blueprint style. The cut points in
   `specs.js` are expressed from the marks, so a new take lines up by itself.
4. **Publish**: encode for the web into `assets/video/`, pull a poster into
   `assets/img/demo/`, and add `video`, `video_square`, `poster`, `video_caption`,
   `video_duration` to the project's front matter (EN and FR), then run
   `python3 tools/build_site.py`.

## Voiceover and music

- **Voice**: Brahim's own voice, an ElevenLabs instant clone ("Brahim (heybrahim demos)",
  id in `narrate.py`) made from his Aria Voice Coach recordings. The samples stay in
  `.work/voice/`, never in git; the clone can be deleted from the ElevenLabs account.
- **Script**: `narrations/<name>.<lang>.txt`, one line per shot (7 lines for gemmaquiz).
  `python3 narrate.py gemmaquiz en` generates one natural take plus per-line timings
  (character alignment) into `remotion/public/narration-<name>-<lang>.{mp3,json}`.
  The edit derives every shot's length from those timings, so the picture follows the voice.
- **Music**: one soft instrumental bed (`remotion/public/music-bed.mp3`, ElevenLabs Music),
  ducked under the voice by `musicVolume()` in `Demo.jsx`.
- **Key**: `ELEVENLABS_API_KEY` in `~/.config/heybrahim/elevenlabs.env` (chmod 600, a scoped key
  with a credit cap). Never commit it.
- **Captions** stay on screen (most people watch muted), and the page caption says the voice is
  an AI clone of Brahim's.
- Web encodes are normalised to −16 LUFS (`loudnorm=I=-16:TP=-1.5`).

## gemmaquiz, end to end

```bash
cd tools/demo-videos && npm install && npx playwright install chromium
git clone https://github.com/brbousnguar/gemmaquiz .work/gemmaquiz && (cd .work/gemmaquiz && npm install)
(cd .work/gemmaquiz && PORT=3917 OLLAMA_MODEL=gemma4:e4b-mlx node server.js &)
npm run record:gemmaquiz          # re-run if a question comes out malformed
pkill -f "node server.js"; ollama stop gemma4:e4b-mlx   # free the Mac mini straight away
node stage.mjs gemmaquiz
python3 narrate.py gemmaquiz en && python3 narrate.py gemmaquiz fr
for c in gemmaquiz-16x9 gemmaquiz-1x1 gemmaquiz-fr-16x9 gemmaquiz-fr-1x1; do npm run render -- $c out/$c.mp4; done
cd ../.. && ffmpeg -i tools/demo-videos/out/gemmaquiz-16x9.mp4 -an -c:v libx264 -crf 26 -preset slow \
  -pix_fmt yuv420p -movflags +faststart assets/video/gemmaquiz-demo.mp4   # same for the square cut
```

## House rules

- Real runs only; no mockups. Label any speed-up on screen (`4×`).
- Nothing personal or client-related on screen.
- The Mac mini is shared: render with `--concurrency=2` (the `render` script does), stop
  the app and `ollama stop` the model right after recording.
- `node_modules/`, `.work/`, `out/`, `recordings/*/` and `remotion/public/` are local only
  (see `.gitignore`); only the scripts and the published files in `assets/` are committed.
