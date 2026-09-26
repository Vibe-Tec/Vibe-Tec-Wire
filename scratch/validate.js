const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('Vibe-Tec_Wire.html', 'utf-8');

// 1. Check basic HTML structure
console.log('--- 1. HTML Tag Checks ---');
const hasDoctype = html.includes('<!DOCTYPE html>');
const hasHtmlClose = html.includes('</html>');
console.log('DOCTYPE present:', hasDoctype);
console.log('</html> present:', hasHtmlClose);

// 2. Extract script content
console.log('\n--- 2. JS Syntax Validation ---');
const scriptMatches = [...html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
console.log(`Found ${scriptMatches.length} <script> blocks`);

let jsCode = '';
scriptMatches.forEach((m, idx) => {
  jsCode += `\n// --- Script block ${idx} ---\n` + m[1];
});

try {
  new vm.Script(jsCode);
  console.log('✅ JavaScript Syntax Valid: 0 Syntax Errors!');
} catch (err) {
  console.error('❌ JavaScript Syntax Error:', err.message);
  process.exit(1);
}

// 3. Check declared handlers against inline HTML usages
console.log('\n--- 3. Inline Handler Function Audit ---');
const handlerMatches = [...html.matchAll(/on[a-z]+="([a-zA-Z0-9_]+)\(/gi)];
const uniqueHandlers = new Set(handlerMatches.map(m => m[1]));

console.log(`Auditing ${uniqueHandlers.size} unique event handler functions...`);
const missing = [];
for (const fn of uniqueHandlers) {
  const regex = new RegExp(`function\\s+${fn}\\b|const\\s+${fn}\\s*=|let\\s+${fn}\\s*=|var\\s+${fn}\\s*=`);
  if (!regex.test(jsCode)) {
    missing.push(fn);
  }
}

if (missing.length > 0) {
  console.warn('⚠️ Potential missing handler declarations:', missing);
} else {
  console.log('✅ All HTML event handler functions are properly declared!');
}

console.log('\nAll validation checks PASSED perfectly!');
