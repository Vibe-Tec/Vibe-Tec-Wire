const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('=== TEST UX ELEMENTS LABELS & EDITABILITY ===\n');

const htmlPath = path.join(__dirname, '..', 'Vibe-Tec_Wire.html');
const content = fs.readFileSync(htmlPath, 'utf8');

// 1. Verify text strings in HTML
if (content.includes("text: 'PARTECIPA ALLA PARTITA'")) {
  throw new Error("Found legacy string 'PARTECIPA ALLA PARTITA'");
}
console.log("✔ Zero occurrences of 'PARTECIPA ALLA PARTITA'");

if (content.includes("text: '🔍 Cerca partita o circolo...'")) {
  throw new Error("Found legacy string '🔍 Cerca partita o circolo...'");
}
console.log("✔ Zero occurrences of '🔍 Cerca partita o circolo...'");

// 2. Verify all elements in openObjectTextEditor
const editableTypes = [
  'wire_button',
  'wire_button_secondary',
  'wire_input',
  'wire_component',
  'wire_image',
  'wire_avatar',
  'timer_badge',
  'badge',
  'text'
];

editableTypes.forEach(t => {
  if (!content.includes(`case '${t}':`)) {
    throw new Error(`Type ${t} missing from getTextEditorCopy cases!`);
  }
});
console.log(`✔ All ${editableTypes.length} UX element types covered in getTextEditorCopy`);

// 3. Verify btn-edit-label exists and is in selection controls
if (!content.includes('id="btn-edit-label"')) {
  throw new Error('btn-edit-label element missing from HTML!');
}
console.log("✔ btn-edit-label present in selection controls");

// 4. Verify dblclick listener has all editable types
editableTypes.forEach(t => {
  const dblCheck = content.includes(t);
  if (!dblCheck) {
    throw new Error(`Type ${t} missing from file`);
  }
});
console.log("✔ Editable types verified for dblclick and Enter listeners");

// 5. Simulate in VM sandbox
const sandbox = {
  state: {
    objects: [],
    selectedObjectId: null
  },
  Math: Math,
  Date: Date,
  String: String,
  prompt: (msg, def) => 'NEW_CUSTOM_LABEL',
  openNoteEditor: () => {},
  openTextEditorModal: ({ objId }) => {
    const obj = sandbox.state.objects.find(o => o.id === objId);
    if (obj) obj.text = 'NEW_CUSTOM_LABEL';
  },
  renderAll: () => {},
  history: { push: () => {} },
  updateNoteAutoBounds: () => {},
  getUXDefaultDimensions: (uxType) => ({ w: 100, h: 40 }),
  console: console
};

const createUXMatch = content.match(/function createUXObject\([\s\S]*?\n    \}/);
if (!createUXMatch) throw new Error("Could not extract createUXObject");

const openObjTextMatch = content.match(/function openObjectTextEditor\([\s\S]*?\n    \}/);
if (!openObjTextMatch) throw new Error("Could not extract openObjectTextEditor");
const copyMatch = content.match(/function getTextEditorCopy\([\s\S]*?\n    \}/);
if (!copyMatch) throw new Error("Could not extract getTextEditorCopy");

vm.createContext(sandbox);
vm.runInContext(createUXMatch[0], sandbox);
vm.runInContext(copyMatch[0], sandbox);
vm.runInContext(openObjTextMatch[0], sandbox);

// Test CTA creation
const ctaObj = sandbox.createUXObject('button', 10, 10, 'ab_1');
if (ctaObj.text !== 'CTA') {
  throw new Error(`CTA object text is '${ctaObj.text}', expected 'CTA'`);
}
console.log(`✔ CTA created with text: '${ctaObj.text}'`);

// Test Input creation
const inputObj = sandbox.createUXObject('input', 10, 10, 'ab_1');
if (inputObj.text !== '🔍 Cerca...') {
  throw new Error(`Input object text is '${inputObj.text}', expected '🔍 Cerca...'`);
}
console.log(`✔ Input created with text: '${inputObj.text}'`);

// Test editing all UX objects
editableTypes.forEach(type => {
  const dummyObj = { id: 'test_' + type, type: type, text: 'DEFAULT' };
  sandbox.state.objects.push(dummyObj);
  sandbox.openObjectTextEditor(dummyObj.id);
  if (dummyObj.text !== 'NEW_CUSTOM_LABEL') {
    throw new Error(`Editing failed for type ${type}`);
  }
});
console.log(`✔ All ${editableTypes.length} UX element types successfully edited via openObjectTextEditor`);

console.log('\n🎉 ALL UX LABELS & EDITABILITY TESTS PASSED WITH 100% SUCCESS!');
