#!/usr/bin/env python3
"""Generate a demo narration in Brahim's cloned voice (ElevenLabs), as one take,
with per-line timings from the character alignment.

    python3 narrate.py <name> <lang>     # reads narrations/<name>.<lang>.txt (one line per shot)

Writes remotion/public/narration-<name>-<lang>.mp3 and .json ({lines:[{text,start,end}], total}).
Key: ELEVENLABS_API_KEY in ~/.config/heybrahim/elevenlabs.env (never in the repo).
"""
import base64, json, os, subprocess, sys
from pathlib import Path

VOICE_ID = "6tRZCGl4ufFkjBp2Cvqq"   # "Brahim (heybrahim demos)", instant clone from his Aria recordings
SETTINGS = {"stability": 0.45, "similarity_boost": 0.85, "style": 0.15, "use_speaker_boost": True}

name, lang = sys.argv[1], sys.argv[2]
here = Path(__file__).resolve().parent
lines = [l.strip() for l in (here / f"narrations/{name}.{lang}.txt").read_text().splitlines() if l.strip()]
text = " ".join(lines)
key = next(l.split("=", 1)[1].strip() for l in open(os.path.expanduser("~/.config/heybrahim/elevenlabs.env"))
           if l.startswith("ELEVENLABS_API_KEY"))
body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "language_code": lang, "voice_settings": SETTINGS})
# curl, not urllib: the python.org build on this Mac has no CA bundle.
out = subprocess.run(["curl", "-s", "-X", "POST",
                      f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
                      "-H", f"xi-api-key: {key}", "-H", "Content-Type: application/json", "--data-binary", body],
                     capture_output=True, check=True).stdout
d = json.loads(out)
if "audio_base64" not in d:
    sys.exit(f"ElevenLabs error: {str(d)[:300]}")
pub = here / "remotion/public"
pub.mkdir(parents=True, exist_ok=True)
(pub / f"narration-{name}-{lang}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
al = d["alignment"]
starts, ends = al["character_start_times_seconds"], al["character_end_times_seconds"]
res, pos = [], 0
for ln in lines:
    i = text.index(ln, pos); j = i + len(ln) - 1; pos = j + 1
    res.append({"text": ln, "start": round(starts[i], 3), "end": round(ends[j], 3)})
(pub / f"narration-{name}-{lang}.json").write_text(json.dumps({"lines": res, "total": round(ends[-1], 3)}, indent=1))
for r in res:
    print(f'{r["start"]:5.2f}-{r["end"]:5.2f}  {r["text"]}')
print(f"{len(text)} characters")
