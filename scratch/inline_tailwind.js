const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const htmlPath = path.join(root, 'Vibe-Tec_Wire.html');
const css = fs.readFileSync(path.join(root, 'scratch', 'tw-out.css'), 'utf8');
let html = fs.readFileSync(htmlPath, 'utf8');
const needle = /<style id="tailwind-offline">[\s\S]*?<\/style>/;
if (!needle.test(html)) {
  console.error('tailwind-offline block not found');
  process.exit(1);
}
html = html.replace(needle, '<style id="tailwind-offline">\n' + css + '\n  </style>');
fs.writeFileSync(htmlPath, html);
console.log('Replaced Tailwind offline CSS (' + css.length + ' bytes).');
