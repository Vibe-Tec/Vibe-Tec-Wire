function fitLabelFont(str, boxW, boxH, padX, padY, maxSize, minSize) {
  const availW = Math.max(4, boxW - padX * 2);
  const availH = Math.max(4, boxH - padY * 2);
  let size = Math.min(maxSize || 16, Math.max(minSize || 9, Math.floor(availH * 0.62)));
  const min = minSize || 9;
  const approx = (s, fs) => s.length * fs * 0.62;
  while (size > min) {
    if (approx(str, size) <= availW) break;
    size--;
  }
  return Math.max(min, size);
}

const cta = fitLabelFont('CTA', 260, 48, 16, 8, 14, 9);
if (cta < 12) throw new Error('short CTA should stay large, got ' + cta);

const long = fitLabelFont('PARTECIPA ALLA PARTITA OGGI STESSO', 120, 48, 16, 8, 14, 9);
if (long >= cta) throw new Error('long label must shrink inside the button');

const tiny = fitLabelFont('OK', 40, 24, 8, 4, 14, 9);
if (tiny > 12) throw new Error('short box should cap font to height');

console.log('OK  : label font shrinks with container / long copy');
console.log('\nText layout tests PASSED');
