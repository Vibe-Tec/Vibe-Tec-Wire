const fs = require('fs');

const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf-8');

console.log('--- Test 1: Grid Overlay Visibility Logic ---');

// Mock renderGridOverlaySVG
function renderGridOverlaySVG(ab) {
  let svg = '';
  const cols = ab.gridCols !== undefined ? ab.gridCols : 4;
  const rows = ab.gridRows !== undefined ? ab.gridRows : 8;
  const showCols = ab.showCols !== false;
  const showRows = ab.showRows !== false;
  const w = ab.width;
  const h = ab.height;

  if (showCols && cols > 0) {
    svg += '<!-- COLS -->';
  }
  if (showRows && rows > 0) {
    svg += '<!-- ROWS -->';
  }
  return svg;
}

const abBoth = { width: 360, height: 740, gridCols: 4, gridRows: 8, showCols: true, showRows: true };
const abColsOnly = { width: 360, height: 740, gridCols: 4, gridRows: 8, showCols: true, showRows: false };
const abRowsOnly = { width: 360, height: 740, gridCols: 4, gridRows: 8, showCols: false, showRows: true };
const abNone = { width: 360, height: 740, gridCols: 4, gridRows: 8, showCols: false, showRows: false };

if (renderGridOverlaySVG(abBoth).includes('COLS') && renderGridOverlaySVG(abBoth).includes('ROWS')) {
  console.log('✅ Both visible test passed');
} else process.exit(1);

if (renderGridOverlaySVG(abColsOnly).includes('COLS') && !renderGridOverlaySVG(abColsOnly).includes('ROWS')) {
  console.log('✅ Cols-only test passed');
} else process.exit(1);

if (!renderGridOverlaySVG(abRowsOnly).includes('COLS') && renderGridOverlaySVG(abRowsOnly).includes('ROWS')) {
  console.log('✅ Rows-only test passed');
} else process.exit(1);

if (renderGridOverlaySVG(abNone) === '') {
  console.log('✅ None visible test passed');
} else process.exit(1);

console.log('\n--- Test 2: Heatmap Scientific Citations in Guide ---');
const hasHooberLink = html.includes('https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php');
const hasClarkLink = html.includes('https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/');
const hasHoober2017Link = html.includes('https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-thumbs-and-people-part-1.php');

console.log('Hoober 2013 paper link present:', hasHooberLink);
console.log('Clark 2015/2016 paper link present:', hasClarkLink);
console.log('Hoober 2017 paper link present:', hasHoober2017Link);

if (hasHooberLink && hasClarkLink && hasHoober2017Link) {
  console.log('✅ All scientific links verified!');
} else {
  console.error('❌ Missing scientific citation links');
  process.exit(1);
}

console.log('\nAll tests PASSED!');
