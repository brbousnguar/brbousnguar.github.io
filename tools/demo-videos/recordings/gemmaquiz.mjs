// Records a real gemmaquiz session for the demo video.
//
// Prerequisites: gemmaquiz running locally, e.g. from a clone in .work/:
//   PORT=3917 OLLAMA_MODEL=gemma4:e4b-mlx node server.js
// Output: recordings/gemmaquiz/ with 1920x1080 JPEG frames (CDP screencast),
// frames.json (timestamps), marks.json (event times in seconds) and quiz.json.
//
// The page is zoomed 1.5x so a 1280-wide layout renders crisply at 1080p. Because
// of that zoom, real mouse coordinates don't match the screen, so a visible cursor
// is drawn inside the page and glides to each target; Playwright does the clicks.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const URL = process.env.GEMMAQUIZ_URL || 'http://127.0.0.1:3917/';
const SUBJECT = process.env.SUBJECT || 'black hoels';
const QUESTIONS = 3;
const OUT = path.resolve('recordings/gemmaquiz');
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const CURSOR = `
(() => {
  const css = document.createElement('style');
  css.textContent = \`
    #__cur{position:fixed;left:0;top:0;width:26px;height:26px;z-index:2147483647;pointer-events:none;transform:translate(-3px,-2px)}
    .__rip{position:fixed;z-index:2147483646;pointer-events:none;width:14px;height:14px;margin:-7px 0 0 -7px;
      border-radius:50%;border:2px solid #1446C8;animation:__r .55s ease-out forwards}
    @keyframes __r{from{opacity:.9;transform:scale(1)}to{opacity:0;transform:scale(4.2)}}\`;
  const cur = document.createElement('div');
  cur.id = '__cur';
  cur.innerHTML = '<svg viewBox="0 0 24 24" width="26" height="26"><path d="M3 2l7.5 19 2.6-7.4L20.5 11z" fill="#131211" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  const mount = () => { document.documentElement.style.zoom = '1.5'; document.head.appendChild(css); document.body.appendChild(cur); };
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', mount) : mount();
  let x = 700, y = 560; cur.style.left = x + 'px'; cur.style.top = y + 'px';
  window.__glide = (tx, ty, ms = 520) => new Promise(done => {
    const sx = x, sy = y, t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / ms), e = k < 0.5 ? 4*k*k*k : 1 - Math.pow(-2*k + 2, 3) / 2;
      x = sx + (tx - sx) * e; y = sy + (ty - sy) * e;
      cur.style.left = x + 'px'; cur.style.top = y + 'px';
      k < 1 ? requestAnimationFrame(step) : done();
    };
    requestAnimationFrame(step);
  });
  window.__ripple = () => { const r = document.createElement('div'); r.className = '__rip';
    r.style.left = x + 'px'; r.style.top = y + 'px'; document.body.appendChild(r); setTimeout(() => r.remove(), 700); };
})();`;

const events = [];
const mark = (name) => { events.push({ name, t: Date.now() / 1000 }); console.log('event', name); };

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await ctx.addInitScript(CURSOR);
const page = await ctx.newPage();
let quiz = null;
page.on('response', async (r) => { if (r.url().endsWith('/api/quiz')) { try { quiz = await r.json(); } catch {} } });

await page.goto(URL, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const cdp = await ctx.newCDPSession(page);
const frames = [];
cdp.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
  const file = path.join(OUT, `f${String(frames.length).padStart(5, '0')}.jpg`);
  fs.writeFileSync(file, Buffer.from(data, 'base64'));
  frames.push({ file, t: metadata.timestamp });
  await cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {});
});
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });

async function moveTo(locator) {
  const bb = await locator.boundingBox();
  // boundingBox is in screen px; fixed positions inside the zoomed page are scaled by 1.5.
  await page.evaluate(([x, y]) => window.__glide(x, y), [(bb.x + bb.width / 2) / 1.5, (bb.y + bb.height / 2) / 1.5]);
}
async function click(locator) {
  await moveTo(locator); await page.waitForTimeout(160);
  await page.evaluate(() => window.__ripple()); await locator.click(); await page.waitForTimeout(80);
}

await page.waitForTimeout(1200);
mark('start');
await click(page.locator('#subject'));
mark('typing');
await page.keyboard.type(SUBJECT, { delay: 110 });
await page.waitForTimeout(500);
await click(page.locator('#go'));
mark('refining');
await page.locator('#generate').waitFor({ timeout: 120000 });
mark('refined');
await page.waitForTimeout(1600);
await moveTo(page.locator('#count'));
await page.locator('#count').selectOption(String(QUESTIONS));
await page.waitForTimeout(500);
await click(page.locator('#generate'));
mark('generating');
await page.locator('.option').first().waitFor({ timeout: 180000 });
mark('quiz');
await page.waitForTimeout(1400);
for (let q = 0; q < QUESTIONS; q++) {
  const answer = quiz?.questions?.[q]?.answerIndex ?? 0;
  await page.waitForTimeout(900);
  await click(page.locator(`.option[data-idx="${answer}"]`));
  mark(`answer${q + 1}`);
  await page.waitForTimeout(1900);
  await click(page.locator('#next'));
  await page.waitForTimeout(700);
}
mark('results');
await page.waitForTimeout(3000);
mark('end');

await cdp.send('Page.stopScreencast');
await page.waitForTimeout(300);
const t0 = frames[0].t;
fs.writeFileSync(path.join(OUT, 'frames.json'), JSON.stringify(frames));
fs.writeFileSync(path.join(OUT, 'marks.json'), JSON.stringify(Object.fromEntries(events.map((e) => [e.name, +(e.t - t0).toFixed(3)])), null, 1));
fs.writeFileSync(path.join(OUT, 'quiz.json'), JSON.stringify(quiz, null, 2));
console.log('frames', frames.length, 'span', (frames.at(-1).t - t0).toFixed(1) + 's');
await browser.close();
