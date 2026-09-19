// Edit scripts. Cut points come from the recording's own marks (written by the
// recorder, plus `duration` from stage.mjs), so a re-take lines up automatically.
import gq from '../public/marks-gemmaquiz.json';

export const gemmaquiz = {
  frames: 'frames-gemmaquiz',
  titleFrames: 54,
  endFrames: 75,
  title: { eyebrow: 'SIDE PROJECT', title: 'gemmaquiz',
    lines: ['Turn any subject into a quiz.', 'Local Gemma + the real Wikipedia article.'], foot: 'OPEN SOURCE · MIT' },
  end: { eyebrow: 'TRY IT', title: 'gemmaquiz',
    lines: ['github.com/brbousnguar/gemmaquiz', 'npm start · Ollama + Gemma · MIT'] },
  clips: [
    { src: [gq.start + 0.2, gq.refining + 0.3], rate: 1, cam: [1.55, 900, 400], caption: 'Type anything. Typos welcome.' },
    { src: [gq.refining + 0.3, gq.generating - 0.15], rate: 1.4, cam: [1.3, 960, 540], caption: 'Local Gemma fixes it: Black hole' },
    { src: [gq.generating - 0.15, gq.quiz + 0.45], rate: 4, cam: [1.15, 960, 500], caption: 'It reads the real Wikipedia article', badge: '4×' },
    { src: [gq.quiz + 0.45, gq.answer2 - 2.4], rate: 1.2, cam: [1.25, 960, 620], caption: 'Every answer comes with the why' },
    { src: [gq.answer2 - 2.4, gq.results - 0.1], rate: 3, cam: [1.25, 960, 620], caption: 'Runs on my Mac. No cloud, no API keys.', badge: '3×' },
    { src: [gq.results - 0.1, gq.duration], rate: 1, hold: 1.4, cam: [1.6, 960, 400], camSquare: [1.25, 960, 400], caption: '3/3 on black holes' },
  ],
};
