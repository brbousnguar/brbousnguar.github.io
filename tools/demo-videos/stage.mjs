// Stage a recording for Remotion: timestamped screencast frames -> constant 30 fps
// numbered JPEGs in remotion/public/frames-<name>/, plus the site's fonts.
//   node stage.mjs gemmaquiz
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const name = process.argv[2];
if (!name) throw new Error('usage: node stage.mjs <recording-name>');
const rec = path.resolve('recordings', name);
const pub = path.resolve('remotion/public');
const frames = JSON.parse(fs.readFileSync(path.join(rec, 'frames.json'), 'utf8'));

// ffmpeg concat list: each frame lasts until the next one was captured.
const list = frames.map((f, i) => {
  const next = frames[i + 1];
  return `file '${f.file}'\nduration ${next ? Math.max(next.t - f.t, 0.001).toFixed(4) : '0.5'}`;
}).join('\n') + `\nfile '${frames.at(-1).file}'\n`;
fs.writeFileSync(path.join(rec, 'concat.txt'), list);

const out = path.join(pub, `frames-${name}`);
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', path.join(rec, 'concat.txt'),
  '-vf', 'fps=30', '-q:v', '3', '-start_number', '0', path.join(out, 'f%04d.jpg')]);

for (const f of fs.readdirSync('../../assets/fonts').filter((f) => f.endsWith('.woff2'))) {
  fs.copyFileSync(path.join('../../assets/fonts', f), path.join(pub, f));
}
const count = fs.readdirSync(out).length;
const marks = { ...JSON.parse(fs.readFileSync(path.join(rec, 'marks.json'), 'utf8')), duration: +(count / 30).toFixed(3) };
fs.writeFileSync(path.join(pub, `marks-${name}.json`), JSON.stringify(marks, null, 1));
console.log(`${count} frames at 30 fps -> ${path.relative(process.cwd(), out)}`);
console.log('marks', fs.readFileSync(path.join(rec, 'marks.json'), 'utf8').replace(/\s+/g, ' '));
