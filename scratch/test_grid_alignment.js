const fs = require('fs');
const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf8');

function extract(fnName) {
  const start = html.indexOf('function ' + fnName);
  if (start < 0) throw new Error('missing ' + fnName);
  let i = html.indexOf('{', start);
  let depth = 0;
  for (; i < html.length; i++) {
    if (html[i] === '{') depth++;
    else if (html[i] === '}') {
      depth--;
      if (depth === 0) return html.slice(start, i + 1);
    }
  }
  throw new Error('unclosed ' + fnName);
}

eval(extract('getDeviceChrome'));
eval(extract('getArtboardContentSize'));
eval(extract('renderGridOverlaySVG'));

const mobile = { type: 'mobile', width: 360, height: 740, gridCols: 4, gridRows: 8, showCols: true, showRows: true };
const tablet = { type: 'tablet', width: 768, height: 1024, gridCols: 4, gridRows: 8, showCols: true, showRows: true };
const desktop = { type: 'desktop', width: 1200, height: 760, gridCols: 4, gridRows: 8, showCols: true, showRows: true };

const mInner = getArtboardContentSize(mobile);
if (mInner.w !== 350) throw new Error('mobile inner width expected 350, got ' + mInner.w);
if (mInner.h !== 730) throw new Error('mobile inner height expected 730, got ' + mInner.h);

const svg = renderGridOverlaySVG(mobile);
if (svg.includes('width="360"') || svg.includes('height="740"')) {
  throw new Error('grid still uses outer device size instead of content box');
}
if (!svg.includes('x1="175"')) {
  throw new Error('missing vertical centerline for camera alignment');
}

const chrome = getDeviceChrome(mobile);
if (chrome.safeTop !== 48) throw new Error('mobile safeTop should skip status/notch');
if (!svg.includes(`y="${chrome.safeTop}"`)) throw new Error('columns should start below the notch band');

const tInner = getArtboardContentSize(tablet);
if (tInner.w !== 756) throw new Error('tablet inner width expected 756, got ' + tInner.w);

const dInner = getArtboardContentSize(desktop);
if (dInner.w !== 1196) throw new Error('desktop inner width expected 1196, got ' + dInner.w);

console.log('OK  : mobile/tablet/desktop grid uses content box, not device chrome');
console.log('OK  : camera centerline at inner width / 2');
console.log('OK  : rows/cols inset below mobile status band');
console.log('\nGrid alignment tests PASSED');
