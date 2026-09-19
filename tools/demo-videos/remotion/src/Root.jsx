import { Composition } from 'remotion';
import { Demo, FPS, buildTimeline } from './Demo.jsx';
import { gemmaquiz } from './specs.js';

// One 16:9 (X, the site) and one 1:1 (feeds) cut per demo.
const demos = { gemmaquiz };

export const Root = () => (
  <>
    {Object.entries(demos).map(([id, spec]) => {
      const total = buildTimeline(spec).total;
      return [
        <Composition key={`${id}-16x9`} id={`${id}-16x9`} component={Demo} fps={FPS} width={1920} height={1080}
          durationInFrames={total} defaultProps={{ spec }} />,
        <Composition key={`${id}-1x1`} id={`${id}-1x1`} component={Demo} fps={FPS} width={1080} height={1080}
          durationInFrames={total} defaultProps={{ spec }} />,
      ];
    })}
  </>
);
