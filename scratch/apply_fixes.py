import os
import re

html_path = 'Vibe-Tec_Wire.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings to \n for consistent replacement
crlf = '\r\n' in content
if crlf:
    content = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. Right dock #selection-controls: add Scala buttons and W / H inputs
# -----------------------------------------------------------------------------
target_sel_controls = """          <button id="btn-straighten-arrow" onclick="straightenSelectedArrow()" class="hidden w-full py-1 px-1.5 rounded bg-sky-950 hover:bg-sky-900 text-sky-300 border border-sky-700/50 font-mono text-[10px] flex items-center justify-center gap-1" title="Raddrizza Freccia / Curva">
            <span>📏</span> Raddrizza
          </button>"""

replacement_sel_controls = """          <button id="btn-straighten-arrow" onclick="straightenSelectedArrow()" class="hidden w-full py-1 px-1.5 rounded bg-sky-950 hover:bg-sky-900 text-sky-300 border border-sky-700/50 font-mono text-[10px] flex items-center justify-center gap-1" title="Raddrizza Freccia / Curva">
            <span>📏</span> Raddrizza
          </button>

          <!-- Dimensione / Scala Rapida -->
          <div class="w-full flex items-center justify-between border-b border-slate-800 pb-1 mt-0.5">
            <span class="text-[9px] text-[#1bfd02] font-bold uppercase tracking-wider">Scala</span>
            <div class="flex items-center gap-1">
              <button onclick="scaleSelected(0.9)" class="w-6 h-5 flex items-center justify-center rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs shadow-sm transition-colors" title="Rimpicciolisci (-10%)">−</button>
              <button onclick="scaleSelected(1.1)" class="w-6 h-5 flex items-center justify-center rounded bg-slate-800 hover:bg-slate-700 text-[#1bfd02] font-bold text-xs shadow-sm transition-colors" title="Ingrandisci (+10%)">+</button>
            </div>
          </div>

          <!-- Dimensioni W / H Esatte in Pixel -->
          <div class="w-full grid grid-cols-2 gap-1 text-[10px] font-mono">
            <div class="flex items-center bg-slate-900/90 border border-slate-700/80 rounded px-1.5 py-0.5">
              <span class="text-slate-500 mr-0.5 font-bold">W:</span>
              <input type="number" id="sel-obj-w" onchange="updateSelectedDimension('width', this.value)" class="w-full bg-transparent text-white outline-none text-right font-mono text-[10px]" min="10" title="Larghezza in pixel" />
            </div>
            <div class="flex items-center bg-slate-900/90 border border-slate-700/80 rounded px-1.5 py-0.5">
              <span class="text-slate-500 mr-0.5 font-bold">H:</span>
              <input type="number" id="sel-obj-h" onchange="updateSelectedDimension('height', this.value)" class="w-full bg-transparent text-white outline-none text-right font-mono text-[10px]" min="10" title="Altezza in pixel" />
            </div>
          </div>
          
          <div class="w-full border-t border-slate-800 my-0.5"></div>"""

assert target_sel_controls in content, "Target 1 not found"
content = content.replace(target_sel_controls, replacement_sel_controls, 1)

# -----------------------------------------------------------------------------
# 2. window drag_artboard mousemove & mouseup: call renderAll()
# -----------------------------------------------------------------------------
target_drag_ab_move = """        if (elem) {
          elem.style.left = state.activeDraggingArtboard.x + 'px';
          elem.style.top = state.activeDraggingArtboard.y + 'px';
        }
        return;"""

replacement_drag_ab_move = """        if (elem) {
          elem.style.left = state.activeDraggingArtboard.x + 'px';
          elem.style.top = state.activeDraggingArtboard.y + 'px';
        }
        renderAll();
        return;"""

assert target_drag_ab_move in content, "Target 2 not found"
content = content.replace(target_drag_ab_move, replacement_drag_ab_move, 1)

target_drag_ab_up = """      if (state.transformType === 'drag_artboard') {
        state.transformType = null;
        state.activeDraggingArtboard = null;
        history.push();
      }"""

replacement_drag_ab_up = """      if (state.transformType === 'drag_artboard') {
        state.transformType = null;
        state.activeDraggingArtboard = null;
        renderAll();
        history.push();
      }"""

assert target_drag_ab_up in content, "Target 3 not found"
content = content.replace(target_drag_ab_up, replacement_drag_ab_up, 1)

# -----------------------------------------------------------------------------
# 3. Add updatePenBounds(obj) above updateArrowBounds(obj)
# -----------------------------------------------------------------------------
target_arrow_bounds = """    function updateArrowBounds(obj) {"""

replacement_arrow_bounds = """    function updatePenBounds(obj) {
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

    function updateArrowBounds(obj) {"""

assert target_arrow_bounds in content, "Target 4 not found"
content = content.replace(target_arrow_bounds, replacement_arrow_bounds, 1)

# -----------------------------------------------------------------------------
# 4. In handleGlobalMouseMove: handle drag_obj for pen points + add resize_obj handler
# -----------------------------------------------------------------------------
target_drag_obj_move = """        if (obj.x1 !== undefined) {
          obj.x1 = Math.round(state.initialObjState.x1 + dx);
          obj.y1 = Math.round(state.initialObjState.y1 + dy);
          obj.x2 = Math.round(state.initialObjState.x2 + dx);
          obj.y2 = Math.round(state.initialObjState.y2 + dy);
          obj.cx1 = Math.round(state.initialObjState.cx1 + dx);
          obj.cy1 = Math.round(state.initialObjState.cy1 + dy);
          obj.cx2 = Math.round(state.initialObjState.cx2 + dx);
          obj.cy2 = Math.round(state.initialObjState.cy2 + dy);
          updateArrowBounds(obj);
        } else {
          obj.x = Math.round(state.initialObjState.x + dx);
          obj.y = Math.round(state.initialObjState.y + dy);
        }
        renderAll();
      }"""

replacement_drag_obj_move = """        if (obj.points && state.initialObjState.points) {
          for (let i = 0; i < obj.points.length; i++) {
            obj.points[i].x = Math.round(state.initialObjState.points[i].x + dx);
            obj.points[i].y = Math.round(state.initialObjState.points[i].y + dy);
          }
          obj.x = Math.round(state.initialObjState.x + dx);
          obj.y = Math.round(state.initialObjState.y + dy);
        } else if (obj.x1 !== undefined) {
          obj.x1 = Math.round(state.initialObjState.x1 + dx);
          obj.y1 = Math.round(state.initialObjState.y1 + dy);
          obj.x2 = Math.round(state.initialObjState.x2 + dx);
          obj.y2 = Math.round(state.initialObjState.y2 + dy);
          obj.cx1 = Math.round(state.initialObjState.cx1 + dx);
          obj.cy1 = Math.round(state.initialObjState.cy1 + dy);
          obj.cx2 = Math.round(state.initialObjState.cx2 + dx);
          obj.cy2 = Math.round(state.initialObjState.cy2 + dy);
          updateArrowBounds(obj);
        } else {
          obj.x = Math.round(state.initialObjState.x + dx);
          obj.y = Math.round(state.initialObjState.y + dy);
        }
        renderAll();
      }

      if (state.transformType === 'resize_obj' && state.selectedObjectId) {
        const obj = state.objects.find(o => o.id === state.selectedObjectId);
        if (!obj || !state.initialObjState) return;

        const curWorld = obj.frameId ? getPointerArtboardPos(e, obj.frameId) : getPointerWorldPos(e);
        let dx = curWorld.x - state.dragStartX;
        let dy = curWorld.y - state.dragStartY;

        // If the object is rotated, project dx and dy onto the object's local rotated axis
        if (state.initialObjState.rotation) {
          const rad = -(state.initialObjState.rotation * Math.PI / 180);
          const cos = Math.cos(rad);
          const sin = Math.sin(rad);
          const rdx = dx * cos - dy * sin;
          const rdy = dx * sin + dy * cos;
          dx = rdx;
          dy = rdy;
        }

        const init = state.initialObjState;
        let newW = init.width;
        let newH = init.height;
        let localShiftX = 0;
        let localShiftY = 0;

        const lockAspect = e.shiftKey || obj.type === 'square' || obj.type === 'circle' || obj.type === 'wire_avatar' || obj.type === 'badge';
        const hId = state.resizeHandle;

        if (hId === 'se') {
          newW = Math.max(10, init.width + dx);
          newH = Math.max(10, init.height + dy);
          if (lockAspect) {
            const side = Math.max(newW, newH);
            newW = side; newH = side;
          }
        } else if (hId === 'sw') {
          newW = Math.max(10, init.width - dx);
          newH = Math.max(10, init.height + dy);
          if (lockAspect) {
            const side = Math.max(newW, newH);
            newW = side; newH = side;
          }
          localShiftX = init.width - newW;
        } else if (hId === 'ne') {
          newW = Math.max(10, init.width + dx);
          newH = Math.max(10, init.height - dy);
          if (lockAspect) {
            const side = Math.max(newW, newH);
            newW = side; newH = side;
          }
          localShiftY = init.height - newH;
        } else if (hId === 'nw') {
          newW = Math.max(10, init.width - dx);
          newH = Math.max(10, init.height - dy);
          if (lockAspect) {
            const side = Math.max(newW, newH);
            newW = side; newH = side;
          }
          localShiftX = init.width - newW;
          localShiftY = init.height - newH;
        } else if (hId === 'e') {
          newW = Math.max(10, init.width + dx);
        } else if (hId === 'w') {
          newW = Math.max(10, init.width - dx);
          localShiftX = init.width - newW;
        } else if (hId === 's') {
          newH = Math.max(10, init.height + dy);
        } else if (hId === 'n') {
          newH = Math.max(10, init.height - dy);
          localShiftY = init.height - newH;
        }

        // Apply shift back considering rotation
        if (init.rotation) {
          const radF = init.rotation * Math.PI / 180;
          const cosF = Math.cos(radF);
          const sinF = Math.sin(radF);
          obj.x = Math.round(init.x + localShiftX * cosF - localShiftY * sinF);
          obj.y = Math.round(init.y + localShiftX * sinF + localShiftY * cosF);
        } else {
          obj.x = Math.round(init.x + localShiftX);
          obj.y = Math.round(init.y + localShiftY);
        }
        obj.width = Math.round(newW);
        obj.height = Math.round(newH);

        // If pen stroke, scale all points proportionally
        if (obj.type === 'pen' && obj.points && init.points) {
          const scaleX = init.width > 0 ? newW / init.width : 1;
          const scaleY = init.height > 0 ? newH / init.height : 1;
          for (let i = 0; i < obj.points.length; i++) {
            const initPt = init.points[i];
            obj.points[i].x = Math.round(obj.x + (initPt.x - init.x) * scaleX);
            obj.points[i].y = Math.round(obj.y + (initPt.y - init.y) * scaleY);
          }
        }

        if (obj.type === 'text') {
          const ratio = newH / init.height;
          obj.fontSize = Math.max(10, Math.round((init.fontSize || 14) * ratio));
        }

        if (obj.type === 'postit') {
          obj.isCustomSized = true;
        }

        updateSelectionControlsInputs(obj);
        renderAll();
        return;
      }"""

assert target_drag_obj_move in content, "Target 5 not found"
content = content.replace(target_drag_obj_move, replacement_drag_obj_move, 1)

# -----------------------------------------------------------------------------
# 5. In handleGlobalMouseUp:
#    - pen handling & exclude from < 6px fallback
#    - resize_obj history push
#    - drag_obj reparenting for pen points and arrows
# -----------------------------------------------------------------------------
target_mouse_up = """          // Single-click fallback (< 6px drag)
          if ((drawnObj.width || 0) < 6 && (drawnObj.height || 0) < 6) {
            if (drawnObj.type === 'arrow' || drawnObj.type === 'double_arrow' || drawnObj.type === 'line') {
              drawnObj.x2 = drawnObj.x1 + 100;
              drawnObj.y2 = drawnObj.y1;
              drawnObj.cx1 = drawnObj.x1 + 33;
              drawnObj.cy1 = drawnObj.y1;
              drawnObj.cx2 = drawnObj.x1 + 67;
              drawnObj.cy2 = drawnObj.y1;
              updateArrowBounds(drawnObj);
            } else {
              const defW = (drawnObj.type === 'square' || drawnObj.type === 'circle') ? 90 : 120;
              const defH = (drawnObj.type === 'square' || drawnObj.type === 'circle') ? 90 : 80;
              drawnObj.x = Math.round(drawnObj.x - defW / 2);
              drawnObj.y = Math.round(drawnObj.y - defH / 2);
              drawnObj.width = defW;
              drawnObj.height = defH;
            }
          }

          selectObject(drawnObj.id);
          setTool('select'); // Automatically switch to Select so shape doesn't follow cursor or duplicate
          renderAll();
          history.push();
        } else if (state.transformType === 'drag_obj') {
          if (state.hasActuallyDragged) {
            const obj = state.objects.find(o => o.id === state.selectedObjectId);
            if (obj && obj.x1 === undefined) {
              // Calculate world position
              let worldX, worldY;
              if (obj.frameId) {
                const curAb = state.artboards.find(a => a.id === obj.frameId);
                worldX = (curAb ? curAb.x : 0) + obj.x;
                worldY = (curAb ? curAb.y : 0) + obj.y;
              } else {
                worldX = obj.x;
                worldY = obj.y;
              }

              const centerX = worldX + (obj.width || 40) / 2;
              const centerY = worldY + (obj.height || 40) / 2;

              // Check if center is inside any artboard
              const targetAb = state.artboards.find(a => 
                centerX >= a.x && centerX <= (a.x + a.width) &&
                centerY >= a.y && centerY <= (a.y + a.height)
              );

              if (targetAb) {
                obj.frameId = targetAb.id;
                obj.x = Math.round(worldX - targetAb.x);
                obj.y = Math.round(worldY - targetAb.y);
              } else {
                obj.frameId = null;
                obj.x = Math.round(worldX);
                obj.y = Math.round(worldY);
              }
              renderAll();
            }
            history.push();
          }
          state.hasActuallyDragged = false;
        } else if (state.transformType === 'rotate_obj' || (state.transformType && state.transformType.startsWith('drag_arrow_'))) {"""

replacement_mouse_up = """          if (drawnObj.type === 'pen') {
            updatePenBounds(drawnObj);
          } else if ((drawnObj.width || 0) < 6 && (drawnObj.height || 0) < 6) {
            // Single-click fallback (< 6px drag) for shapes
            if (drawnObj.type === 'arrow' || drawnObj.type === 'double_arrow' || drawnObj.type === 'line') {
              drawnObj.x2 = drawnObj.x1 + 100;
              drawnObj.y2 = drawnObj.y1;
              drawnObj.cx1 = drawnObj.x1 + 33;
              drawnObj.cy1 = drawnObj.y1;
              drawnObj.cx2 = drawnObj.x1 + 67;
              drawnObj.cy2 = drawnObj.y1;
              updateArrowBounds(drawnObj);
            } else {
              const defW = (drawnObj.type === 'square' || drawnObj.type === 'circle') ? 90 : 120;
              const defH = (drawnObj.type === 'square' || drawnObj.type === 'circle') ? 90 : 80;
              drawnObj.x = Math.round(drawnObj.x - defW / 2);
              drawnObj.y = Math.round(drawnObj.y - defH / 2);
              drawnObj.width = defW;
              drawnObj.height = defH;
            }
          }

          selectObject(drawnObj.id);
          setTool('select'); // Automatically switch to Select so shape doesn't follow cursor or duplicate
          renderAll();
          history.push();
        } else if (state.transformType === 'resize_obj') {
          history.push();
        } else if (state.transformType === 'drag_obj') {
          if (state.hasActuallyDragged) {
            const obj = state.objects.find(o => o.id === state.selectedObjectId);
            if (obj) {
              const oldFrameId = obj.frameId;
              // Calculate world position
              let worldX, worldY;
              if (obj.frameId) {
                const curAb = state.artboards.find(a => a.id === obj.frameId);
                worldX = (curAb ? curAb.x : 0) + obj.x;
                worldY = (curAb ? curAb.y : 0) + obj.y;
              } else {
                worldX = obj.x;
                worldY = obj.y;
              }

              const centerX = worldX + (obj.width || 40) / 2;
              const centerY = worldY + (obj.height || 40) / 2;

              // Check if center is inside any artboard
              const targetAb = state.artboards.find(a => 
                centerX >= a.x && centerX <= (a.x + a.width) &&
                centerY >= a.y && centerY <= (a.y + a.height)
              );

              const newFrameId = targetAb ? targetAb.id : null;
              if (oldFrameId !== newFrameId) {
                const oldWorldX = oldFrameId ? (state.artboards.find(a => a.id === oldFrameId)?.x || 0) : 0;
                const oldWorldY = oldFrameId ? (state.artboards.find(a => a.id === oldFrameId)?.y || 0) : 0;
                const newWorldX = targetAb ? targetAb.x : 0;
                const newWorldY = targetAb ? targetAb.y : 0;
                const shiftX = oldWorldX - newWorldX;
                const shiftY = oldWorldY - newWorldY;

                if (obj.points && Array.isArray(obj.points)) {
                  obj.points.forEach(pt => {
                    pt.x = Math.round(pt.x + shiftX);
                    pt.y = Math.round(pt.y + shiftY);
                  });
                  updatePenBounds(obj);
                }
                if (obj.x1 !== undefined && obj.x2 !== undefined) {
                  obj.x1 = Math.round(obj.x1 + shiftX);
                  obj.y1 = Math.round(obj.y1 + shiftY);
                  obj.x2 = Math.round(obj.x2 + shiftX);
                  obj.y2 = Math.round(obj.y2 + shiftY);
                  if (obj.cx1 !== undefined) obj.cx1 = Math.round(obj.cx1 + shiftX);
                  if (obj.cy1 !== undefined) obj.cy1 = Math.round(obj.cy1 + shiftY);
                  if (obj.cx2 !== undefined) obj.cx2 = Math.round(obj.cx2 + shiftX);
                  if (obj.cy2 !== undefined) obj.cy2 = Math.round(obj.cy2 + shiftY);
                  updateArrowBounds(obj);
                }
              }

              if (targetAb) {
                obj.frameId = targetAb.id;
                obj.x = Math.round(worldX - targetAb.x);
                obj.y = Math.round(worldY - targetAb.y);
              } else {
                obj.frameId = null;
                obj.x = Math.round(worldX);
                obj.y = Math.round(worldY);
              }
              renderAll();
            }
            history.push();
          }
          state.hasActuallyDragged = false;
        } else if (state.transformType === 'rotate_obj' || (state.transformType && state.transformType.startsWith('drag_arrow_'))) {"""

assert target_mouse_up in content, "Target 6 not found"
content = content.replace(target_mouse_up, replacement_mouse_up, 1)

# -----------------------------------------------------------------------------
# 6. Preserve manual resize in updateNoteAutoBounds(obj)
# -----------------------------------------------------------------------------
target_note_bounds = """    function updateNoteAutoBounds(obj) {
      if (!obj || obj.type !== 'postit') return;"""

replacement_note_bounds = """    function updateNoteAutoBounds(obj) {
      if (!obj || obj.type !== 'postit') return;
      if (obj.isCustomSized && obj.width && obj.height) return; // Preserve manual resizing"""

assert target_note_bounds in content, "Target 7 not found"
content = content.replace(target_note_bounds, replacement_note_bounds, 1)

# -----------------------------------------------------------------------------
# 7. Add scaleSelected, updateSelectedDimension and updateSelectionControlsInputs
# -----------------------------------------------------------------------------
target_select_obj = """    function selectObject(id) {
      state.selectedObjectId = id;
      const obj = state.objects.find(o => o.id === id);
      selectionControls.classList.remove('hidden');"""

replacement_select_obj = """    function updateSelectionControlsInputs(obj) {
      const wIn = document.getElementById('sel-obj-w');
      const hIn = document.getElementById('sel-obj-h');
      if (wIn && obj && obj.width !== undefined) wIn.value = obj.width;
      if (hIn && obj && obj.height !== undefined) hIn.value = obj.height;
    }

    function scaleSelected(factor) {
      if (!state.selectedObjectId) return;
      const obj = state.objects.find(o => o.id === state.selectedObjectId);
      if (!obj) return;

      if (obj.x1 !== undefined && obj.x2 !== undefined) {
        const cx = (obj.x1 + obj.x2) / 2;
        const cy = (obj.y1 + obj.y2) / 2;
        obj.x1 = Math.round(cx + (obj.x1 - cx) * factor);
        obj.y1 = Math.round(cy + (obj.y1 - cy) * factor);
        obj.x2 = Math.round(cx + (obj.x2 - cx) * factor);
        obj.y2 = Math.round(cy + (obj.y2 - cy) * factor);
        if (obj.cx1 !== undefined) obj.cx1 = Math.round(cx + (obj.cx1 - cx) * factor);
        if (obj.cy1 !== undefined) obj.cy1 = Math.round(cy + (obj.cy1 - cy) * factor);
        if (obj.cx2 !== undefined) obj.cx2 = Math.round(cx + (obj.cx2 - cx) * factor);
        if (obj.cy2 !== undefined) obj.cy2 = Math.round(cy + (obj.cy2 - cy) * factor);
        updateArrowBounds(obj);
      } else {
        const oldW = obj.width || 10;
        const oldH = obj.height || 10;
        const newW = Math.max(10, Math.round(oldW * factor));
        const newH = Math.max(10, Math.round(oldH * factor));

        obj.x = Math.round(obj.x - (newW - oldW) / 2);
        obj.y = Math.round(obj.y - (newH - oldH) / 2);
        obj.width = newW;
        obj.height = newH;

        if (obj.type === 'pen' && obj.points) {
          const scaleX = newW / oldW;
          const scaleY = newH / oldH;
          obj.points.forEach(pt => {
            pt.x = Math.round(obj.x + (pt.x - (obj.x + (newW - oldW) / 2)) * scaleX);
            pt.y = Math.round(obj.y + (pt.y - (obj.y + (newH - oldH) / 2)) * scaleY);
          });
        }
        if (obj.type === 'text') {
          obj.fontSize = Math.max(10, Math.round((obj.fontSize || 14) * factor));
        }
        if (obj.type === 'postit') {
          obj.isCustomSized = true;
        }
      }
      updateSelectionControlsInputs(obj);
      renderAll();
      history.push();
    }

    function updateSelectedDimension(prop, val) {
      if (!state.selectedObjectId) return;
      const obj = state.objects.find(o => o.id === state.selectedObjectId);
      if (!obj) return;
      const num = Math.max(10, parseInt(val, 10) || 10);
      const oldW = obj.width || 10;
      const oldH = obj.height || 10;
      obj[prop] = num;

      if (obj.type === 'pen' && obj.points) {
        const scaleX = prop === 'width' ? num / oldW : 1;
        const scaleY = prop === 'height' ? num / oldH : 1;
        obj.points.forEach(pt => {
          pt.x = Math.round(obj.x + (pt.x - obj.x) * scaleX);
          pt.y = Math.round(obj.y + (pt.y - obj.y) * scaleY);
        });
      }
      if (obj.type === 'postit') {
        obj.isCustomSized = true;
      }
      renderAll();
      history.push();
    }

    function selectObject(id) {
      state.selectedObjectId = id;
      const obj = state.objects.find(o => o.id === id);
      selectionControls.classList.remove('hidden');
      updateSelectionControlsInputs(obj);"""

assert target_select_obj in content, "Target 8 not found"
content = content.replace(target_select_obj, replacement_select_obj, 1)

# -----------------------------------------------------------------------------
# 8. In g.addEventListener('mousedown'): save points & width/height in initialObjState
# -----------------------------------------------------------------------------
target_g_mousedown = """          state.initialObjState = { 
            x: obj.x, 
            y: obj.y,
            x1: obj.x1,
            y1: obj.y1,
            x2: obj.x2,
            y2: obj.y2,
            cx1: obj.cx1,
            cy1: obj.cy1,
            cx2: obj.cx2,
            cy2: obj.cy2
          };"""

replacement_g_mousedown = """          state.initialObjState = { 
            x: obj.x, 
            y: obj.y,
            width: obj.width || 10,
            height: obj.height || 10,
            rotation: obj.rotation || 0,
            fontSize: obj.fontSize || 14,
            x1: obj.x1,
            y1: obj.y1,
            x2: obj.x2,
            y2: obj.y2,
            cx1: obj.cx1,
            cy1: obj.cy1,
            cx2: obj.cx2,
            cy2: obj.cy2,
            points: obj.points ? obj.points.map(pt => ({ x: pt.x, y: pt.y })) : null
          };"""

assert target_g_mousedown in content, "Target 9 not found"
content = content.replace(target_g_mousedown, replacement_g_mousedown, 1)

# -----------------------------------------------------------------------------
# 9. In renderAll(): calculate dynamic subpixel offset for artboard selection overlay
# -----------------------------------------------------------------------------
target_render_all_off = """          let offX = 0, offY = 0;
          if (selObj.frameId) {
            const ab = state.artboards.find(a => a.id === selObj.frameId);
            if (ab) { offX = ab.x; offY = ab.y; }
          }
          renderSelectionHandles(selectionOverlayGroup, selObj, offX, offY);"""

replacement_render_all_off = """          let offX = 0, offY = 0;
          if (selObj.frameId) {
            const abSvg = document.getElementById('svg-' + selObj.frameId);
            const worldSvg = document.getElementById('svg-world');
            if (abSvg && worldSvg) {
              const rAb = abSvg.getBoundingClientRect();
              const rWorld = worldSvg.getBoundingClientRect();
              offX = (rAb.left - rWorld.left) / state.zoom;
              offY = (rAb.top - rWorld.top) / state.zoom;
            } else {
              const ab = state.artboards.find(a => a.id === selObj.frameId);
              if (ab) { offX = ab.x; offY = ab.y; }
            }
          }
          renderSelectionHandles(selectionOverlayGroup, selObj, offX, offY);"""

assert target_render_all_off in content, "Target 10 not found"
content = content.replace(target_render_all_off, replacement_render_all_off, 1)

# -----------------------------------------------------------------------------
# 10. In renderShapeElement: text font-size & baseline support
# -----------------------------------------------------------------------------
target_text_shape = """      else if (type === 'text') {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x); text.setAttribute('y', y + 16);
        text.setAttribute('font-size', '14'); text.setAttribute('font-weight', '700');
        text.setAttribute('fill', color); text.setAttribute('font-family', '-apple-system, sans-serif');
        text.textContent = obj.text || 'Testo';
        g.appendChild(text);
      }"""

replacement_text_shape = """      else if (type === 'text') {
        const fSize = obj.fontSize || 14;
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x); text.setAttribute('y', y + fSize * 1.15);
        text.setAttribute('font-size', fSize); text.setAttribute('font-weight', '700');
        text.setAttribute('fill', color); text.setAttribute('font-family', '-apple-system, sans-serif');
        text.textContent = obj.text || 'Testo';
        g.appendChild(text);
      }"""

assert target_text_shape in content, "Target 11 not found"
content = content.replace(target_text_shape, replacement_text_shape, 1)

# -----------------------------------------------------------------------------
# 11. In renderSelectionHandles: render 8 interactive resize handles
# -----------------------------------------------------------------------------
target_sel_handles = """      // 3. Rotation handle knob
      const knob = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      knob.setAttribute('cx', cx); knob.setAttribute('cy', y - 24);
      knob.setAttribute('r', '6.5'); knob.setAttribute('fill', '#1bfd02');
      knob.setAttribute('stroke', '#000000'); knob.setAttribute('stroke-width', '2');
      knob.setAttribute('class', 'rotation-handle');
      knob.setAttribute('title', 'Trascina per ruotare l\\'oggetto');
      
      knob.addEventListener('mousedown', (e) => {
        e.stopPropagation();
        state.isTransforming = true;
        state.transformType = 'rotate_obj';
      });

      hGroup.appendChild(knob);
      containerGroup.appendChild(hGroup);
    }"""

replacement_sel_handles = """      // 3. Rotation handle knob
      const knob = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      knob.setAttribute('cx', cx); knob.setAttribute('cy', y - 24);
      knob.setAttribute('r', '6.5'); knob.setAttribute('fill', '#1bfd02');
      knob.setAttribute('stroke', '#000000'); knob.setAttribute('stroke-width', '2');
      knob.setAttribute('class', 'rotation-handle');
      knob.setAttribute('title', 'Trascina per ruotare l\\'oggetto');
      
      knob.addEventListener('mousedown', (e) => {
        e.stopPropagation();
        state.isTransforming = true;
        state.transformType = 'rotate_obj';
      });

      hGroup.appendChild(knob);

      // 4. Eight Interactive Resize Handles (Corners & Midpoints)
      const handleSize = 8;
      const halfH = handleSize / 2;
      const handles = [
        { id: 'nw', x: x - 4 - halfH, y: y - 4 - halfH, cursor: 'nwse-resize', title: 'Ridimensiona Alto-Sinistra' },
        { id: 'n',  x: cx - halfH, y: y - 4 - halfH, cursor: 'ns-resize', title: 'Ridimensiona Alto' },
        { id: 'ne', x: x + w + 4 - halfH, y: y - 4 - halfH, cursor: 'nesw-resize', title: 'Ridimensiona Alto-Destra' },
        { id: 'e',  x: x + w + 4 - halfH, y: cy - halfH, cursor: 'ew-resize', title: 'Ridimensiona Destra' },
        { id: 'se', x: x + w + 4 - halfH, y: y + h + 4 - halfH, cursor: 'nwse-resize', title: 'Ridimensiona Basso-Destra' },
        { id: 's',  x: cx - halfH, y: y + h + 4 - halfH, cursor: 'ns-resize', title: 'Ridimensiona Basso' },
        { id: 'sw', x: x - 4 - halfH, y: y + h + 4 - halfH, cursor: 'nesw-resize', title: 'Ridimensiona Basso-Sinistra' },
        { id: 'w',  x: x - 4 - halfH, y: cy - halfH, cursor: 'ew-resize', title: 'Ridimensiona Sinistra' }
      ];

      handles.forEach(hSpec => {
        const handleRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        handleRect.setAttribute('x', hSpec.x);
        handleRect.setAttribute('y', hSpec.y);
        handleRect.setAttribute('width', handleSize);
        handleRect.setAttribute('height', handleSize);
        handleRect.setAttribute('fill', '#FFFFFF');
        handleRect.setAttribute('stroke', '#000000');
        handleRect.setAttribute('stroke-width', '1.5');
        handleRect.setAttribute('rx', '1.5');
        handleRect.setAttribute('class', 'resize-handle');
        handleRect.style.cursor = hSpec.cursor;
        handleRect.setAttribute('title', hSpec.title);

        handleRect.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          state.isTransforming = true;
          state.transformType = 'resize_obj';
          state.resizeHandle = hSpec.id;
          state.resizeStartClient = { x: e.clientX, y: e.clientY };
          state.initialObjState = {
            x: obj.x,
            y: obj.y,
            width: obj.width || 10,
            height: obj.height || 10,
            rotation: obj.rotation || 0,
            fontSize: obj.fontSize || 14,
            points: obj.points ? obj.points.map(pt => ({ x: pt.x, y: pt.y })) : null
          };
          const p = obj.frameId ? getPointerArtboardPos(e, obj.frameId) : getPointerWorldPos(e);
          state.dragStartX = p.x;
          state.dragStartY = p.y;
        });

        hGroup.appendChild(handleRect);
      });

      containerGroup.appendChild(hGroup);
    }"""

assert target_sel_handles in content, "Target 12 not found"
content = content.replace(target_sel_handles, replacement_sel_handles, 1)

# -----------------------------------------------------------------------------
# 12. In loadProjectJSON: calibrate pen bounds & single canvas position
# -----------------------------------------------------------------------------
target_load_json = """          if (data.artboards && Array.isArray(data.artboards)) {
            // Full Project JSON
            state.artboards = data.artboards;
            state.objects = data.objects || [];
            rebuildArtboardDOM();
            renderAll();
            history.push();
            alert('Progetto caricato con successo!');
          } else if (data.artboard && data.objects) {
            // Single Canvas Component JSON
            const newAb = JSON.parse(JSON.stringify(data.artboard));
            newAb.id = 'ab_' + Date.now();
            newAb.x = 80;
            newAb.y = 80;
            state.artboards.push(newAb);
            data.objects.forEach(o => {
              const newObj = JSON.parse(JSON.stringify(o));
              newObj.id = 'obj_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);
              newObj.frameId = newAb.id;
              state.objects.push(newObj);
            });"""

replacement_load_json = """          if (data.artboards && Array.isArray(data.artboards)) {
            // Full Project JSON
            state.artboards = data.artboards;
            state.objects = data.objects || [];
            state.objects.forEach(o => {
              if (o.type === 'pen') updatePenBounds(o);
            });
            rebuildArtboardDOM();
            renderAll();
            history.push();
            alert('Progetto caricato con successo!');
          } else if (data.artboard && data.objects) {
            // Single Canvas Component JSON
            const newAb = JSON.parse(JSON.stringify(data.artboard));
            newAb.id = 'ab_' + Date.now();
            const maxX = state.artboards.reduce((max, a) => Math.max(max, a.x + a.width), 0);
            newAb.x = maxX > 0 ? maxX + 60 : 80;
            newAb.y = 80;
            state.artboards.push(newAb);
            data.objects.forEach(o => {
              const newObj = JSON.parse(JSON.stringify(o));
              newObj.id = 'obj_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);
              newObj.frameId = newAb.id;
              if (newObj.type === 'pen') updatePenBounds(newObj);
              state.objects.push(newObj);
            });"""

assert target_load_json in content, "Target 13 not found"
content = content.replace(target_load_json, replacement_load_json, 1)

# Write back preserving CRLF if originally present
if crlf:
    content = content.replace('\n', '\r\n')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: All 12 patch targets applied cleanly!")
