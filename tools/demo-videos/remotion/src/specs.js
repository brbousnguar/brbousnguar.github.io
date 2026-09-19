// Edit scripts. Cut points come from the recording's marks (recorder + stage.mjs), and
// shot lengths from the narration timings (narrate.py), so a re-take or a re-voice lines
// up by itself.
import gq from '../public/marks-gemmaquiz.json';
import gqEn from '../public/narration-gemmaquiz-en.json';
import gqFr from '../public/narration-gemmaquiz-fr.json';

const FPS = 30;
const TEXT = {
  en: {
    title: { eyebrow: 'SIDE PROJECT', title: 'gemmaquiz',
      lines: ['Turn any subject into a quiz.', 'Local Gemma + the real Wikipedia article.'], foot: 'OPEN SOURCE · MIT' },
    end: { eyebrow: 'TRY IT', title: 'gemmaquiz', lines: ['github.com/brbousnguar/gemmaquiz', 'npm start · Ollama + Gemma · MIT'] },
    captions: ['Type anything. Typos welcome.', 'Local Gemma fixes it: Black hole', 'It reads the real Wikipedia article',
      'Every answer comes with the why', 'Runs on my Mac. No cloud, no API keys.', '3/3 on black holes'],
  },
  fr: {
    title: { eyebrow: 'PROJET PERSO', title: 'gemmaquiz',
      lines: ["Transformer n'importe quel sujet en quiz.", 'Gemma en local + le vrai article Wikipédia.'], foot: 'OPEN SOURCE · MIT' },
    end: { eyebrow: 'À ESSAYER', title: 'gemmaquiz', lines: ['github.com/brbousnguar/gemmaquiz', 'npm start · Ollama + Gemma · MIT'] },
    captions: ['Tapez n\'importe quoi, fautes comprises.', 'Gemma en local corrige : Black hole', 'Il lit le vrai article Wikipédia',
      'Chaque réponse est expliquée', 'Sur mon Mac. Pas de cloud, pas de clé d\'API.', '3/3 sur les trous noirs'],
  },
};

// Lines: 0 name, 1 typing, 2 fix, 3 article + quiz, 4 answers, 5 local, 6 try it.
function gemmaquiz(lang, n) {
  const L = n.lines, T = TEXT[lang];
  const between = (a, b) => L[b].start - L[a].start;
  const localShare = 0.7;   // "runs on my Mac" covers answers 2-3; the rest shows the score
  return {
    frames: 'frames-gemmaquiz',
    narration: { src: `narration-gemmaquiz-${lang}.mp3`, lines: L },
    music: 'music-bed.mp3',
    captions: false,   // no on-screen captions: the voice carries it (Brahim, 2026-09-19); speed badges still show
    titleFrames: Math.round(L[1].start * FPS),
    endFrames: Math.round((n.total - L[6].start + 1.0) * FPS),
    title: T.title,
    end: T.end,
    clips: [
      { src: [gq.start + 0.2, gq.refining + 0.3], dur: between(1, 2), cam: [1.55, 900, 400], caption: T.captions[0] },
      { src: [gq.refining + 0.3, gq.generating - 0.15], dur: between(2, 3), cam: [1.3, 960, 540], caption: T.captions[1] },
      { src: [gq.generating - 0.15, gq.answer1 - 1.0], dur: between(3, 4), cam: [1.15, 960, 520], caption: T.captions[2] },
      { src: [gq.answer1 - 1.0, gq.answer2 - 2.4], dur: between(4, 5), cam: [1.25, 960, 620], caption: T.captions[3] },
      { src: [gq.answer2 - 2.4, gq.results - 0.8], dur: between(5, 6) * localShare, cam: [1.25, 960, 620], caption: T.captions[4] },
      { src: [gq.results - 0.8, gq.duration], dur: between(5, 6) * (1 - localShare), hold: true,
        cam: [1.6, 960, 400], camSquare: [1.25, 960, 400], caption: T.captions[5] },
    ],
  };
}

export const demos = {
  gemmaquiz: gemmaquiz('en', gqEn),
  'gemmaquiz-fr': gemmaquiz('fr', gqFr),
};
