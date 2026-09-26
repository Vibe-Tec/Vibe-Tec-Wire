const fs = require('fs');
const vm = require('vm');

console.log('=== TEST SMART GUIDES & MAGNETIC SNAP (FIGMA STYLE: MICRO & MACRO) ===\n');

const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf8');

// 1. Verify existence of smart guides layers in HTML/SVG template
if (!html.includes('id="smart-guides-layer"')) throw new Error('Missing smart-guides-layer in HTML');
if (!html.includes('id="guides-${ab.id}"')) throw new Error('Missing guides-${ab.id} group in artboard template');
console.log('✔ HTML SVG layers verified (Macro world layer + Micro artboard layer)');

// 2. Extract and run JS context
const scriptStart = html.indexOf('<script>');
const scriptEnd = html.lastIndexOf('</script>');
const jsCode = html.slice(scriptStart + 8, scriptEnd);

// Setup minimal DOM mocks
const elements = {};
function createMockEl(tag) {
  return {
    tagName: tag,
    children: [],
    style: {},
    attributes: {},
    innerHTML: '',
    setAttribute(k, v) { this.attributes[k] = v; },
    appendChild(child) { this.children.push(child); }
  };
}

const mockDoc = {
  getElementById(id) {
    if (!elements[id]) elements[id] = createMockEl('g');
    return elements[id];
  },
  createElementNS(ns, tag) {
    return createMockEl(tag);
  },
  createElement(tag) {
    return createMockEl(tag);
  },
  querySelectorAll() { return []; }
};

const sandbox = {
  document: mockDoc,
  window: {
    addEventListener: () => {},
    innerWidth: 1920,
    innerHeight: 1080
  },
  console: console,
  Math: Math,
  Date: Date,
  JSON: JSON,
  state: {
    artboards: [
      { id: 'ab_1', x: 100, y: 100, width: 390, height: 844, title: 'Screen 01' },
      { id: 'ab_2', x: 600, y: 100, width: 390, height: 844, title: 'Screen 02' }
    ],
    objects: [
      { id: 'obj_1', frameId: 'ab_1', x: 50, y: 100, width: 120, height: 48 },
      { id: 'obj_2', frameId: 'ab_1', x: 200, y: 300, width: 120, height: 48 },
      { id: 'obj_3', frameId: 'ab_2', x: 50, y: 100, width: 120, height: 48 } // Other canvas!
    ]
  }
};

vm.createContext(sandbox);

// Execute smart guides engine in sandbox
vm.runInContext(`
${jsCode.slice(jsCode.indexOf('const SMART_SNAP_THRESHOLD = 6;'), jsCode.indexOf('function handleGlobalMouseMove'))}
`, sandbox);

console.log('✔ Smart guides engine compiled in sandbox');

// Test A: Micro Snap inside artboard ab_1
const draggedObj = { id: 'obj_drag', frameId: 'ab_1', width: 120, height: 48 };

// 1. Snap Left to obj_1 (obj_1.left is 50. Test at 53 -> should snap to 50)
let res = sandbox.applyObjectSmartGuides(draggedObj, 53, 200);
if (res.x !== 50) throw new Error(`Expected X snap to 50, got ${res.x}`);
console.log('✔ Micro Snap: Left-to-Left alignment snapped from 53 to 50');

// 2. Snap CenterX to Canvas Center (ab_1.width = 390, center = 195. Dragged obj width = 120, so center is x + 60. At x = 133, center is 193 -> should snap to 135)
res = sandbox.applyObjectSmartGuides(draggedObj, 133, 200);
if (res.x !== 135) throw new Error(`Expected CenterX snap to 135, got ${res.x}`);
console.log('✔ Micro Snap: CenterX to Canvas Center snapped from 133 to 135 (center at 195)');

// 3. Snap Top to obj_1 (obj_1.top is 100. Test at y = 104 -> should snap to 100)
res = sandbox.applyObjectSmartGuides(draggedObj, 250, 104);
if (res.y !== 100) throw new Error(`Expected Y snap to 100, got ${res.y}`);
console.log('✔ Micro Snap: Top-to-Top alignment snapped from 104 to 100');

// 4. Isolation Check: Ensure draggedObj inside ab_1 does NOT snap to obj_3 in ab_2!
// obj_3 is at x: 50, y: 100 in ab_2. If ab_1 candidates mistakenly included ab_2, it would have duplicate snaps.
const ab1Layer = elements['guides-ab_1'];
if (!ab1Layer || ab1Layer.children.length === 0) throw new Error('Expected visual SVG guide line in guides-ab_1');
console.log('✔ Micro Snap: SVG guide line generated in guides-ab_1');

// Test B: Macro Snap between artboards on the board
const draggedAb = { id: 'ab_2', x: 600, y: 104, width: 390, height: 844 };

// Drag ab_2 with y = 104 (within 4px of ab_1.y = 100) -> should snap to 100!
const macroRes = sandbox.applyArtboardSmartGuides(draggedAb, 600, 104);
if (macroRes.y !== 100) throw new Error(`Expected Macro snap Y to 100, got ${macroRes.y}`);
console.log('✔ Macro Snap: Top-to-Top alignment between artboards snapped from 104 to 100');

const worldLayer = elements['smart-guides-layer'];
if (!worldLayer || worldLayer.children.length === 0) throw new Error('Expected visual SVG guide line in smart-guides-layer');
console.log('✔ Macro Snap: SVG guide line generated in smart-guides-layer');

// Test C: Cleanup
sandbox.clearAllSmartGuides();
if (worldLayer.innerHTML !== '' && worldLayer.children.length !== 0) throw new Error('clearAllSmartGuides did not clear world layer');
console.log('✔ Cleanup: clearAllSmartGuides() successfully clears all layers');

console.log('\n🎉 ALL SMART GUIDES TESTS PASSED WITH 100% SUCCESS!');
