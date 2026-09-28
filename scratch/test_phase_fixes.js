const fs = require('fs');

console.log('=== TEST PHASE FIXES (v3.9 review) ===\n');
const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf8');
let failed = 0;
function check(name, cond) {
  if (!cond) {
    console.error('FAIL:', name);
    failed++;
  } else {
    console.log('OK  :', name);
  }
}

check('icon_ click-to-place branch', html.includes("state.tool.startsWith('icon_')") && html.includes('createIconObject'));
check('stroke width ids stroke-w2/4/8', html.includes('id="stroke-w2"') && html.includes('id="stroke-w4"') && html.includes('class="stroke-btn'));
check('setColor has el argument', html.includes('function setColor(color, el)'));
check('fitAllArtboards computes bounds', html.includes('const boundsW = Math.max(maxX - minX, 1)') && html.includes('function fitAllArtboards'));
check('dashed draw preview', html.includes('function applyPreviewDash') && html.includes("stroke-dasharray', '6 4'"));
check('tablet rotate button hooked', html.includes("toggleTabletOrientation('${ab.id}')"));
check('JSON version 3.9 on project save', /version:\s*"3.9"/.test(html) && !html.includes('version: "3.5"'));
check('no native prompt()', !html.includes('prompt('));
check('text editor modal present', html.includes('id="text-editor-modal"') && html.includes('function openTextEditorModal'));
check('Tailwind CDN removed', !html.includes('cdn.tailwindcss.com'));
check('offline Tailwind style tag', html.includes('id="tailwind-offline"'));
check('export draws wire_icon', html.includes('function drawIconToCanvas') && html.includes("type === 'wire_icon'"));
check('export draws exclamation/question', html.includes("type === 'exclamation'") && html.includes("type === 'question'"));
check('board export scales instead of crop', html.includes('fitScale') && html.includes('ctx.scale(fitScale, fitScale)'));
check('patchObjectRender live drag', html.includes('function patchObjectRender') && html.includes('bindCanvasObjectEvents'));
check('grid overlay refresh without rebuild', html.includes('function refreshGridOverlay'));
check('Auto-Layout applyAutoLayout', html.includes('function applyAutoLayout') && html.includes('parentId'));
check('Tokens + Inspector openers', html.includes('function openTokensModal') && html.includes('function openInspectorModal'));
check('WCAG contrast math', html.includes('function relativeLuminance') && html.includes('function contrastRatio'));
check('dead addUXElement removed', !html.includes('function addUXElement'));
check('dead smartGuidesState removed', !html.includes('smartGuidesState'));
check('free frame artboard type', html.includes("addArtboard('frame')") && html.includes('DEVICE_CONFIGS') && html.includes("type === 'frame'"));
check('marquee multi-select', html.includes('function startMarquee') && html.includes("transformType = 'marquee'"));
check('snap scoped to parentId', html.includes('function collectSnapCandidates') && html.includes('(o.parentId || null) !== parentKey'));
check('nested containers allowed', html.includes('function wouldCreateParentCycle') && !html.includes("newObj.type === 'wire_component') return"));
check('artboard resize handles', html.includes('function startResizeArtboard') && html.includes('resize_artboard'));
check('dead clearSmartGuides alias removed', !html.includes('function clearSmartGuides'));
check('load JSON does not reject 3.5', html.includes('function loadProjectJSON') && !/if\s*\(.*version/.test(html.slice(html.indexOf('function loadProjectJSON'))));

const renderFn = html.slice(html.indexOf('function renderShapeElement'), html.indexOf('function drawObjectToCanvas'));
const exportFn = html.slice(html.indexOf('function drawObjectToCanvas'), html.indexOf('function drawIconToCanvas'));
['wire_icon', 'exclamation', 'question', 'pen', 'text', 'postit'].forEach(t => {
  check('renderer has ' + t, renderFn.includes("type === '" + t + "'"));
  check('exporter has ' + t, exportFn.includes("type === '" + t + "'") || (t === 'wire_icon' && exportFn.includes('drawIconToCanvas')));
});

if (failed) {
  console.error('\n' + failed + ' checks failed');
  process.exit(1);
}
console.log('\nAll phase-fix checks PASSED');
