console.log('=== TEST AUTO-LAYOUT PACKING MATH ===\n');

function applyAutoLayout(container, objects) {
  if (!container.layout) {
    container.layout = { enabled: true, direction: 'vertical', padding: 16, gap: 12, align: 'start' };
  }
  const L = container.layout;
  const pad = L.padding == null ? 16 : L.padding;
  const gap = L.gap == null ? 12 : L.gap;
  const kids = objects
    .filter(o => o.parentId === container.id)
    .sort((a, b) => (a.order || 0) - (b.order || 0) || a.y - b.y || a.x - b.x);
  const titleBand = 28;
  if (L.direction === 'horizontal') {
    let cursor = container.x + pad;
    kids.forEach((child, i) => {
      child.order = i;
      child.x = cursor;
      child.y = container.y + pad + titleBand;
      cursor += (child.width || 40) + gap;
    });
  } else {
    let cursor = container.y + pad + titleBand;
    kids.forEach((child, i) => {
      child.order = i;
      child.x = container.x + pad;
      child.y = cursor;
      cursor += (child.height || 40) + gap;
    });
    container.height = Math.max(container.height, Math.round(cursor - gap + pad - container.y));
  }
}

const container = { id: 'c1', type: 'wire_component', x: 10, y: 20, width: 260, height: 90, layout: { enabled: true, direction: 'vertical', padding: 16, gap: 12, align: 'start' } };
const a = { id: 'a', parentId: 'c1', width: 200, height: 40, x: 0, y: 0 };
const b = { id: 'b', parentId: 'c1', width: 200, height: 48, x: 0, y: 0 };
const c = { id: 'c', parentId: 'c1', width: 200, height: 32, x: 0, y: 0 };
applyAutoLayout(container, [a, b, c]);

if (a.x !== 26) throw new Error('child A x expected 26, got ' + a.x);
if (a.y !== 64) throw new Error('child A y expected 64, got ' + a.y);
if (b.y !== 116) throw new Error('child B y expected 116, got ' + b.y);
if (c.y !== 176) throw new Error('child C y expected 176, got ' + c.y);
if (container.height < 200) throw new Error('container should grow, height=' + container.height);

c.parentId = null;
applyAutoLayout(container, [a, b, c]);
if (c.y !== 176) throw new Error('detached child should keep last y');
if (b.y !== 116) throw new Error('remaining children should still pack');

console.log('OK  : vertical packing of 3 children with pad 16 / gap 12');
console.log('OK  : detach by clearing parentId');
console.log('\nAuto-layout unit tests PASSED');
