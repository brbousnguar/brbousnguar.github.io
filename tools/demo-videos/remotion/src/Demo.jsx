// A short captioned product demo cut from one real screen recording.
// Blueprint look: paper / ink / cobalt, Archivo + Hanken Grotesk + IBM Plex Mono.
// The recording is shown frame by frame from staged JPEGs (stage.mjs), so the time
// remapping (speed-ups, holds) is exact.
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

export const FPS = 30;
const PAPER = '#FBFAF7', INK = '#131211', INK2 = '#3A3833', COBALT = '#1446C8', SKY = '#9DB6FF', MARKER = '#FFD84D';
const SRC_W = 1920, SRC_H = 1080;

const Fonts = () => (
  <style>{`
    @font-face{font-family:Archivo;font-weight:600 800;src:url(${staticFile('archivo-latin-var.woff2')}) format('woff2')}
    @font-face{font-family:Hanken;font-weight:400 700;src:url(${staticFile('hanken-grotesk-latin-var.woff2')}) format('woff2')}
    @font-face{font-family:Plex;font-weight:500;src:url(${staticFile('ibm-plex-mono-500-latin.woff2')}) format('woff2')}
  `}</style>
);

// Each clip: src [start, end] seconds of the recording, playback rate, optional hold (s)
// on its last frame, camera [scale, focusX, focusY] in source px (camSquare for 1:1),
// caption and an optional speed badge.
export function buildTimeline(spec) {
  let at = spec.titleFrames;
  const clips = spec.clips.map((c) => {
    // With `dur` (target seconds, e.g. from the narration) the playback rate is derived so
    // the shot fits; a clip with `hold` plays at rate 1 and freezes for the rest of `dur`.
    const srcSec = c.src[1] - c.src[0];
    const rate = c.dur ? (c.hold ? 1 : srcSec / c.dur) : c.rate;
    const playFrames = Math.round((srcSec * FPS) / rate);
    const frames = c.dur ? Math.max(Math.round(c.dur * FPS), playFrames) : playFrames + (c.hold ? Math.round(c.hold * FPS) : 0);
    const badge = c.badge ?? (rate >= 1.8 ? `${rate.toFixed(1).replace(/\.0$/, '')}×` : null);
    const clip = { ...c, rate, badge, from: at, frames, playFrames };
    at += frames;
    return clip;
  });
  return { clips, endFrom: at, total: at + spec.endFrames };
}

const current = (frame, clips) => clips.reduce((cur, c) => (frame >= c.from ? c : cur), clips[0]);

function sourceFrame(frame, clips) {
  const c = current(frame, clips);
  const into = Math.min(Math.max(frame - c.from, 0), c.playFrames);
  return Math.min(Math.round(c.src[0] * FPS + into * c.rate), Math.round(c.src[1] * FPS) - 1);
}

function camera(frame, clips, W, H) {
  const cur = current(frame, clips);
  const prev = clips[Math.max(0, clips.indexOf(cur) - 1)];
  const k = interpolate(frame, [cur.from, cur.from + 14], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic),
  });
  const lerp = (a, b) => a + (b - a) * k;
  const s = Math.max(W / SRC_W, H / SRC_H) * lerp(prev.cam[0], cur.cam[0]);
  const fx = lerp(prev.cam[1], cur.cam[1]), fy = lerp(prev.cam[2], cur.cam[2]);
  const tx = Math.min(0, Math.max(W - SRC_W * s, W / 2 - fx * s));
  const ty = Math.min(0, Math.max(H - SRC_H * s, H / 2 - fy * s));
  return { s, tx, ty };
}

// Music bed: fades in, sits low under the voice, a little higher in the gaps, fades out.
function musicVolume(f, spec) {
  const t = f / FPS, total = buildTimeline(spec).total / FPS;
  const speaking = (spec.narration?.lines || []).some((l) => t >= l.start - 0.15 && t <= l.end + 0.25);
  const base = speaking ? 0.07 : 0.16;
  return base * Math.min(1, t / 0.6) * Math.min(1, Math.max(0, (total - t) / 1.2));
}

const Caption = ({ text, badge, W }) => {
  const frame = useCurrentFrame();
  const y = interpolate(frame, [0, 10], [24, 0], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const o = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });
  const size = W < 1400 ? 40 : 46;
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: W < 1400 ? 70 : 64 }}>
      <div style={{ display: 'flex', gap: 14, alignItems: 'center', transform: `translateY(${y}px)`, opacity: o }}>
        {text && <div style={{ background: INK, color: PAPER, fontFamily: 'Hanken', fontWeight: 600, fontSize: size,
          padding: '18px 30px', letterSpacing: '-0.01em', maxWidth: W * 0.86, lineHeight: 1.2 }}>{text}</div>}
        {badge && <div style={{ background: MARKER, color: INK, fontFamily: 'Plex', fontWeight: 500, marginLeft: text ? 0 : 'auto',
          fontSize: size * 0.7, padding: '14px 18px' }}>{badge}</div>}
      </div>
    </AbsoluteFill>
  );
};

// Speed label alone (captions off): bottom-right, same marker style.
const SpeedBadge = ({ badge, W }) => {
  const o = interpolate(useCurrentFrame(), [0, 8], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'flex-end', padding: W < 1400 ? 48 : 56, opacity: o }}>
      <div style={{ background: MARKER, color: INK, fontFamily: 'Plex', fontWeight: 500, fontSize: W < 1400 ? 30 : 34,
        padding: '12px 18px' }}>{badge}</div>
    </AbsoluteFill>
  );
};

const Card = ({ eyebrow, title, lines, foot, W, H }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });
  const y = interpolate(frame, [0, 14], [30, 0], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const narrow = W < 1400, pad = narrow ? 90 : 150;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', left: pad, right: pad, top: H * (narrow ? 0.3 : 0.26), opacity: o,
        transform: `translateY(${y}px)` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, fontFamily: 'Plex', fontWeight: 500, fontSize: 28,
          color: INK2, letterSpacing: '0.08em' }}>
          <span style={{ width: 20, height: 20, background: COBALT, display: 'inline-block' }} />{eyebrow}
        </div>
        <div style={{ fontFamily: 'Archivo', fontWeight: 800, fontSize: narrow ? 150 : 190, color: INK,
          letterSpacing: '-0.045em', lineHeight: 0.95, marginTop: 24 }}>{title}</div>
        {lines.map((l, i) => (
          <div key={i} style={{ fontFamily: 'Hanken', fontWeight: 600, fontSize: narrow ? 46 : 54, color: INK,
            marginTop: i ? 10 : 40, lineHeight: 1.2 }}>{l}</div>
        ))}
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 150, background: INK, display: 'flex',
        alignItems: 'center', justifyContent: 'space-between', padding: `0 ${pad}px` }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
          <div style={{ width: 70, height: 70, border: `3px solid ${PAPER}`, color: PAPER, fontFamily: 'Archivo',
            fontWeight: 800, fontSize: 34, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>BB</div>
          <div style={{ fontFamily: 'Archivo', fontWeight: 700, fontSize: 48, color: PAPER }}>heybrahim.com</div>
        </div>
        {foot && <div style={{ fontFamily: 'Plex', fontWeight: 500, fontSize: 26, color: SKY }}>{foot}</div>}
      </div>
    </AbsoluteFill>
  );
};

export const Demo = ({ spec }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const { clips, endFrom } = buildTimeline(spec);
  const camClips = W === H ? clips.map((c) => ({ ...c, cam: c.camSquare || [1, 960, c.cam[2]] })) : clips;
  const f = Math.max(frame, spec.titleFrames);
  const { s, tx, ty } = camera(f, camClips, W, H);
  const src = staticFile(`${spec.frames}/f${String(sourceFrame(f, clips)).padStart(4, '0')}.jpg`);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <Fonts />
      <AbsoluteFill style={{ transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${s})`,
        width: SRC_W, height: SRC_H }}>
        <Img src={src} style={{ width: SRC_W, height: SRC_H, display: 'block' }} />
      </AbsoluteFill>
      {clips.map((c, i) => {
        const text = spec.captions === false ? null : c.caption;
        return (text || c.badge) && (
          <Sequence key={i} from={c.from + 4} durationInFrames={c.frames - 4}>
            {text ? <Caption text={text} badge={c.badge} W={W} /> : <SpeedBadge badge={c.badge} W={W} />}
          </Sequence>
        );
      })}
      {spec.narration && <Audio src={staticFile(spec.narration.src)} />}
      {spec.music && <Audio src={staticFile(spec.music)} volume={(f) => musicVolume(f, spec)} />}
      <Sequence durationInFrames={spec.titleFrames}><Card W={W} H={H} {...spec.title} /></Sequence>
      <Sequence from={endFrom}><Card W={W} H={H} {...spec.end} /></Sequence>
    </AbsoluteFill>
  );
};
