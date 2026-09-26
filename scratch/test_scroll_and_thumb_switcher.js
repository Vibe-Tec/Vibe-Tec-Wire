const fs = require('fs');
const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf8');

console.log('Testing guide scroll and thumb zone switcher...');

// 1. CSS
if (!html.includes('.custom-scrollbar')) throw new Error('Missing .custom-scrollbar');
console.log('✔ .custom-scrollbar present');

// 2. Guide HTML
if (!html.includes('id="guide-scroll-container"')) throw new Error('Missing #guide-scroll-container');
if (!html.includes('no-canvas-zoom')) throw new Error('Missing no-canvas-zoom');
console.log('✔ Guide panel scroll container and no-canvas-zoom verified');

// 3. Viewport wheel bypass
if (!html.includes("e.target.closest('#quick-guide-widget')")) throw new Error('Viewport wheel does not bypass quick guide');
console.log('✔ Viewport wheel bypasses guide widget correctly');

// 4. Header thumb zone button
if (!html.includes("cycleThumbZone('${ab.id}')")) throw new Error('Missing cycleThumbZone in artboard header');
console.log('✔ cycleThumbZone present in mobile header');

// 5. Dock segmented controls
if (!html.includes("setThumbZoneMode('${ab.id}', 'overlap')") ||
    !html.includes("setThumbZoneMode('${ab.id}', 'right')") ||
    !html.includes("setThumbZoneMode('${ab.id}', 'left')") ||
    !html.includes("setThumbZoneMode('${ab.id}', 'none')")) {
  throw new Error('Missing 4-state segmented switcher in canvas tools dock');
}
console.log('✔ 4-state segmented switcher present in tools dock');

// 6. JS functions
if (!html.includes('function setThumbZoneMode') ||
    !html.includes('function cycleThumbZone') ||
    !html.includes('function toggleThumbZone')) {
  throw new Error('Missing thumb zone JS functions');
}
console.log('✔ setThumbZoneMode, cycleThumbZone, toggleThumbZone all declared');

console.log('\nAll 6 tests PASSED cleanly!');
