// Unit test for math and coordinate transformations in Vibe-Tec Wire

function updatePenBounds(obj) {
  if (!obj || !obj.points || obj.points.length === 0) return;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (let i = 0; i < obj.points.length; i++) {
    const pt = obj.points[i];
    if (pt.x < minX) minX = pt.x;
    if (pt.x > maxX) maxX = pt.x;
    if (pt.y < minY) minY = pt.y;
    if (pt.y > maxY) maxY = pt.y;
  }
  obj.x = Math.round(minX);
  obj.y = Math.round(minY);
  obj.width = Math.max(10, Math.round(maxX - minX));
  obj.height = Math.max(10, Math.round(maxY - minY));
}

console.log('--- Test 1: updatePenBounds ---');
const penObj = {
  type: 'pen',
  points: [
    { x: 10, y: 20 },
    { x: 50, y: 100 },
    { x: 110, y: 40 }
  ]
};
updatePenBounds(penObj);
console.log('Pen bounds:', penObj.x, penObj.y, penObj.width, penObj.height);
if (penObj.x === 10 && penObj.y === 20 && penObj.width === 100 && penObj.height === 80) {
  console.log('✅ Test 1 Passed: Bounds match exact min/max!');
} else {
  console.error('❌ Test 1 Failed');
  process.exit(1);
}

console.log('\n--- Test 2: Pen Scaling ---');
const oldW = penObj.width;
const oldH = penObj.height;
const newW = 200; // 2x scale
const newH = 160; // 2x scale
const scaleX = newW / oldW;
const scaleY = newH / oldH;
penObj.points.forEach(pt => {
  pt.x = Math.round(penObj.x + (pt.x - penObj.x) * scaleX);
  pt.y = Math.round(penObj.y + (pt.y - penObj.y) * scaleY);
});
updatePenBounds(penObj);
console.log('Scaled Pen bounds:', penObj.x, penObj.y, penObj.width, penObj.height);
if (penObj.width === 200 && penObj.height === 160) {
  console.log('✅ Test 2 Passed: Pen scaled proportionally without distortion!');
} else {
  console.error('❌ Test 2 Failed');
  process.exit(1);
}

console.log('\n--- Test 3: Reparenting Coordinate Shift ---');
// Suppose object was drawn in Artboard at x=100, y=100. Local point was (15, 25).
// When moved to world, shift is +100, +100 => (115, 125).
const shiftX = 100;
const shiftY = 100;
penObj.points.forEach(pt => {
  pt.x = Math.round(pt.x + shiftX);
  pt.y = Math.round(pt.y + shiftY);
});
updatePenBounds(penObj);
console.log('Reparented bounds:', penObj.x, penObj.y);
if (penObj.x === 110 && penObj.y === 120) {
  console.log('✅ Test 3 Passed: Reparenting shift preserves absolute positioning!');
} else {
  console.error('❌ Test 3 Failed');
  process.exit(1);
}

console.log('\nAll unit logic tests PASSED!');
