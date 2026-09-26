import os

html_path = 'Vibe-Tec_Wire.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

crlf = '\r\n' in content
if crlf:
    content = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. CSS Heatmap Colors: Ensure scientific green in .heatmap-overlap
# -----------------------------------------------------------------------------
target_css_heatmap = """    .heatmap-overlap {
      background: 
        radial-gradient(ellipse 65% 32% at 50% 82%, rgba(27, 253, 2, 0.6) 0%, rgba(16, 185, 129, 0.45) 45%, transparent 75%),
        radial-gradient(circle at 95% 95%, rgba(245, 158, 11, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 5% 95%, rgba(245, 158, 11, 0.35) 0%, transparent 45%),
        linear-gradient(to top, 
          rgba(16, 185, 129, 0.25) 0%, 
          rgba(16, 185, 129, 0.2) 50%, 
          rgba(245, 158, 11, 0.3) 65%, 
          rgba(244, 63, 94, 0.4) 85%, 
          rgba(225, 29, 72, 0.55) 100%);
    }"""

replacement_css_heatmap = """    .heatmap-overlap {
      background: 
        radial-gradient(ellipse 65% 32% at 50% 82%, rgba(16, 185, 129, 0.55) 0%, rgba(16, 185, 129, 0.4) 45%, transparent 75%),
        radial-gradient(circle at 95% 95%, rgba(245, 158, 11, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 5% 95%, rgba(245, 158, 11, 0.35) 0%, transparent 45%),
        linear-gradient(to top, 
          rgba(16, 185, 129, 0.25) 0%, 
          rgba(16, 185, 129, 0.2) 50%, 
          rgba(245, 158, 11, 0.3) 65%, 
          rgba(244, 63, 94, 0.4) 85%, 
          rgba(225, 29, 72, 0.55) 100%);
    }"""

assert target_css_heatmap in content, "Target 1 (CSS heatmap) not found"
content = content.replace(target_css_heatmap, replacement_css_heatmap, 1)

# -----------------------------------------------------------------------------
# 2. Guide Panel Biomechanics: Scientific Definitions, Citations & Clickable Links
# -----------------------------------------------------------------------------
target_guide_bio = """          <!-- 1. Biomechanics -->
          <div>
            <div class="text-[11px] font-bold text-[#1bfd02] uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <span>🎯</span> Biomeccanica delle Thumb-Zones (Hoober & Clark)
            </div>
            <div class="space-y-1.5 text-[11px] leading-relaxed text-slate-300">
              <div class="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
                <strong class="text-emerald-400">🟢 Verde (49% Zona Naturale del Pollice):</strong> Zero sforzo muscolare a una mano. Colloca qui CTA primarie (es. <em>Partecipa</em>), Bottom Sheet, form di input e swipe navigation.
              </div>
              <div class="p-2.5 rounded-xl bg-amber-950/40 border border-amber-800/40">
                <strong class="text-amber-400">🟡 Ambra (36% Estensione Asimmetrica):</strong> Raggiungibile ruotando o spostando leggermente la presa della mano. Ideale per filtri, caroselli orizzontali e schede secondarie.
              </div>
              <div class="p-2.5 rounded-xl bg-rose-950/40 border border-rose-800/40">
                <strong class="text-rose-400">🔴 Rosso (15% Ow-Zone Superiore):</strong> Zona ad alto attrito anatomico. Riservata ad avatar, switch impostazioni, breadcrumb o azioni distruttive per prevenire crampi e tap accidentali.
              </div>
            </div>
          </div>"""

replacement_guide_bio = """          <!-- 1. Biomechanics -->
          <div>
            <div class="text-[11px] font-bold text-[#1bfd02] uppercase tracking-wider mb-2 flex items-center justify-between">
              <span class="flex items-center gap-1.5"><span>🎯</span> Biomeccanica Thumb-Zones (Hoober & Clark)</span>
              <span class="text-[9px] text-slate-400 font-mono">Dati Scientifici Certificati</span>
            </div>
            <div class="space-y-2 text-[11px] leading-relaxed text-slate-300">
              <div class="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
                <div class="flex items-center justify-between mb-1">
                  <strong class="text-emerald-400 flex items-center gap-1"><span>🟢</span> Natural Zone (Verde Smeraldo - #10B981)</strong>
                  <span class="text-[9px] px-1.5 py-0.5 rounded bg-emerald-900/60 text-emerald-300 font-mono font-bold">Comfort / Zero Sforzo</span>
                </div>
                Arco naturale del pollice (adduzione/abduzione a 1 mano senza rotazione del polso). Colloca qui CTA primarie (es. <em>Partecipa</em>, <em>Salva</em>), Bottom Sheet, form di input e swipe navigation.
              </div>

              <div class="p-2.5 rounded-xl bg-amber-950/40 border border-amber-800/40">
                <div class="flex items-center justify-between mb-1">
                  <strong class="text-amber-400 flex items-center gap-1"><span>🟡</span> Stretch Zone (Ambra Dorata - #F59E0B)</strong>
                  <span class="text-[9px] px-1.5 py-0.5 rounded bg-amber-900/60 text-amber-300 font-mono font-bold">Estensione / Raggiungibile</span>
                </div>
                Raggiungibile allungando il pollice senza mutare l'impugnatura della mano. Ideale per filtri, caroselli orizzontali, controlli secondari e tab navigation.
              </div>

              <div class="p-2.5 rounded-xl bg-rose-950/40 border border-rose-800/40">
                <div class="flex items-center justify-between mb-1">
                  <strong class="text-rose-400 flex items-center gap-1"><span>🔴</span> Ow Zone (Rosso Carminio - #E11D48)</strong>
                  <span class="text-[9px] px-1.5 py-0.5 rounded bg-rose-900/60 text-rose-300 font-mono font-bold">Attrito / Sforzo Massimo</span>
                </div>
                Zona ad alto attrito anatomico (angolo opposto e top screen): richiede cambio di presa o uso di due mani. Riservata ad avatar, switch impostazioni, breadcrumb o azioni distruttive per scongiurare tap accidentali.
              </div>

              <!-- Riferimenti e Paper Scientifici Ufficiali Cliccabili -->
              <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 space-y-1.5">
                <div class="text-[10px] font-bold text-slate-200 uppercase tracking-wide flex items-center gap-1">
                  <span>📚</span> Paper & Ricerche Scientifiche Ufficiali:
                </div>
                <div class="text-[10px] text-slate-400 space-y-1 font-mono">
                  <div class="text-slate-300">
                    • <strong>49%</strong> Monomanuale (67% pollice destro, 33% sinistro) | <strong>36%</strong> A culla (Cradled) | <strong>15%</strong> Bimanuale (Two-handed)
                  </div>
                  <div class="flex flex-col gap-1 pt-1 font-sans">
                    <a href="https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php" target="_blank" rel="noopener noreferrer" class="text-[#1bfd02] hover:underline flex items-center gap-1">
                      <span>🔗</span> Steven Hoober (2013) — <em>How Do Users Really Hold Mobile Devices? (UXmatters)</em>
                    </a>
                    <a href="https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/" target="_blank" rel="noopener noreferrer" class="text-cyan-300 hover:underline flex items-center gap-1">
                      <span>🔗</span> Josh Clark (2015) — <em>Designing for Touch & The Thumb Zone (A Book Apart / Smashing Mag)</em>
                    </a>
                    <a href="https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-thumbs-and-people-part-1.php" target="_blank" rel="noopener noreferrer" class="text-amber-300 hover:underline flex items-center gap-1">
                      <span>🔗</span> Steven Hoober (2017) — <em>Design for Fingers, Thumbs, and People (UXmatters)</em>
                    </a>
                  </div>
                </div>
              </div>

            </div>
          </div>"""

assert target_guide_bio in content, "Target 2 (Guide Bio) not found"
content = content.replace(target_guide_bio, replacement_guide_bio, 1)

# -----------------------------------------------------------------------------
# 3. Canvas Tools Dock: Add ON/OFF buttons for Columns and Rows
# -----------------------------------------------------------------------------
target_canvas_steppers = """              <!-- Riga 1: Colonne Layout (Blu) e Righe Modulari (Ciano) con pieno respiro -->
              <div class="flex items-center justify-between gap-2">
                
                <!-- Stepper Colonne: Blu Cobalto -->
                <div class="flex-1 flex items-center justify-between bg-[#0B0E14] border border-blue-500/40 rounded-lg px-2 py-1 text-[11px] font-mono text-blue-300 shadow-sm" title="Colonne Layout: clicca + o - per impostare la griglia">
                  <span class="font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>Cols: <span class="text-white">${ab.gridCols !== undefined ? ab.gridCols : 4}</span></span>
                  <div class="flex items-center gap-1">
                    <button onclick="stepGridCols('${ab.id}', -1)" class="w-5 h-5 flex items-center justify-center rounded bg-blue-950/60 hover:bg-blue-800 text-blue-300 font-bold border border-blue-700/50 transition-colors">−</button>
                    <button onclick="stepGridCols('${ab.id}', 1)" class="w-5 h-5 flex items-center justify-center rounded bg-blue-950/60 hover:bg-blue-800 text-blue-300 font-bold border border-blue-700/50 transition-colors">+</button>
                  </div>
                </div>

                <!-- Stepper Righe: Azzurro / Cyan Modulari -->
                <div class="flex-1 flex items-center justify-between bg-[#0B0E14] border border-cyan-500/40 rounded-lg px-2 py-1 text-[11px] font-mono text-cyan-300 shadow-sm" title="Righe Modulari: clicca + o - per regolare le fasce orizzontali">
                  <span class="font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>Righe: <span class="text-white">${ab.gridRows !== undefined ? ab.gridRows : 8}</span></span>
                  <div class="flex items-center gap-1">
                    <button onclick="stepGridRows('${ab.id}', -1)" class="w-5 h-5 flex items-center justify-center rounded bg-cyan-950/60 hover:bg-cyan-800 text-cyan-300 font-bold border border-cyan-700/50 transition-colors">−</button>
                    <button onclick="stepGridRows('${ab.id}', 1)" class="w-5 h-5 flex items-center justify-center rounded bg-cyan-950/60 hover:bg-cyan-800 text-cyan-300 font-bold border border-cyan-700/50 transition-colors">+</button>
                  </div>
                </div>

              </div>"""

replacement_canvas_steppers = """              <!-- Riga 1: Colonne Layout (Blu) e Righe Modulari (Ciano) con Toggle ON/OFF Indipendenti -->
              <div class="flex items-center justify-between gap-2">
                
                <!-- Stepper Colonne: Blu Cobalto con Toggle ON/OFF -->
                <div class="flex-1 flex items-center justify-between bg-[#0B0E14] border border-blue-500/40 rounded-lg px-2 py-1 text-[11px] font-mono text-blue-300 shadow-sm" title="Colonne Layout: clicca ON/OFF per mostrare/nascondere o +/− per impostare la quantità">
                  <div class="flex items-center gap-1.5">
                    <button onclick="toggleGridCols('${ab.id}')" class="px-1.5 py-0.5 rounded text-[9px] font-bold transition-all shadow-sm ${ab.showCols !== false ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-500 hover:text-slate-300 border border-slate-700'}" title="Mostra o nascondi le Colonne di questo Artboard">${ab.showCols !== false ? 'ON' : 'OFF'}</button>
                    <span class="font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full ${ab.showCols !== false ? 'bg-blue-400' : 'bg-slate-600'}"></span>Cols: <span class="${ab.showCols !== false ? 'text-white' : 'text-slate-500'}">${ab.gridCols !== undefined ? ab.gridCols : 4}</span></span>
                  </div>
                  <div class="flex items-center gap-1">
                    <button onclick="stepGridCols('${ab.id}', -1)" class="w-5 h-5 flex items-center justify-center rounded bg-blue-950/60 hover:bg-blue-800 text-blue-300 font-bold border border-blue-700/50 transition-colors">−</button>
                    <button onclick="stepGridCols('${ab.id}', 1)" class="w-5 h-5 flex items-center justify-center rounded bg-blue-950/60 hover:bg-blue-800 text-blue-300 font-bold border border-blue-700/50 transition-colors">+</button>
                  </div>
                </div>

                <!-- Stepper Righe: Azzurro / Cyan Modulari con Toggle ON/OFF -->
                <div class="flex-1 flex items-center justify-between bg-[#0B0E14] border border-cyan-500/40 rounded-lg px-2 py-1 text-[11px] font-mono text-cyan-300 shadow-sm" title="Righe Modulari: clicca ON/OFF per mostrare/nascondere o +/− per regolare le fasce orizzontali">
                  <div class="flex items-center gap-1.5">
                    <button onclick="toggleGridRows('${ab.id}')" class="px-1.5 py-0.5 rounded text-[9px] font-bold transition-all shadow-sm ${ab.showRows !== false ? 'bg-cyan-600 text-white' : 'bg-slate-800 text-slate-500 hover:text-slate-300 border border-slate-700'}" title="Mostra o nascondi le Righe di questo Artboard">${ab.showRows !== false ? 'ON' : 'OFF'}</button>
                    <span class="font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full ${ab.showRows !== false ? 'bg-cyan-400' : 'bg-slate-600'}"></span>Righe: <span class="${ab.showRows !== false ? 'text-white' : 'text-slate-500'}">${ab.gridRows !== undefined ? ab.gridRows : 8}</span></span>
                  </div>
                  <div class="flex items-center gap-1">
                    <button onclick="stepGridRows('${ab.id}', -1)" class="w-5 h-5 flex items-center justify-center rounded bg-cyan-950/60 hover:bg-cyan-800 text-cyan-300 font-bold border border-cyan-700/50 transition-colors">−</button>
                    <button onclick="stepGridRows('${ab.id}', 1)" class="w-5 h-5 flex items-center justify-center rounded bg-cyan-950/60 hover:bg-cyan-800 text-cyan-300 font-bold border border-cyan-700/50 transition-colors">+</button>
                  </div>
                </div>

              </div>"""

assert target_canvas_steppers in content, "Target 3 (Canvas Steppers) not found"
content = content.replace(target_canvas_steppers, replacement_canvas_steppers, 1)

# -----------------------------------------------------------------------------
# 4. renderGridOverlaySVG(ab): Respect ab.showCols !== false and ab.showRows !== false
# -----------------------------------------------------------------------------
target_render_grid = """    function renderGridOverlaySVG(ab) {
      let svg = '';
      const cols = ab.gridCols !== undefined ? ab.gridCols : 4;
      const rows = ab.gridRows !== undefined ? ab.gridRows : 8;
      const w = ab.width;
      const h = ab.height;

      // 1. Colonne di Layout (Blu Cobalto, tratteggio nitido ad alto contrasto)
      if (cols > 0) {"""

replacement_render_grid = """    function renderGridOverlaySVG(ab) {
      let svg = '';
      const cols = ab.gridCols !== undefined ? ab.gridCols : 4;
      const rows = ab.gridRows !== undefined ? ab.gridRows : 8;
      const showCols = ab.showCols !== false;
      const showRows = ab.showRows !== false;
      const w = ab.width;
      const h = ab.height;

      // 1. Colonne di Layout (Blu Cobalto, tratteggio nitido ad alto contrasto)
      if (showCols && cols > 0) {"""

assert target_render_grid in content, "Target 4a (Grid Cols Render) not found"
content = content.replace(target_render_grid, replacement_render_grid, 1)

target_render_rows = """      // 2. Righe Modulari di Layout (Azzurro / Ciano, fasce orizzontali nitide ad alto contrasto)
      if (rows > 0) {"""

replacement_render_rows = """      // 2. Righe Modulari di Layout (Azzurro / Ciano, fasce orizzontali nitide ad alto contrasto)
      if (showRows && rows > 0) {"""

assert target_render_rows in content, "Target 4b (Grid Rows Render) not found"
content = content.replace(target_render_rows, replacement_render_rows, 1)

# -----------------------------------------------------------------------------
# 5. Add toggleGridCols & toggleGridRows, and auto-enable showCols/showRows in step functions
# -----------------------------------------------------------------------------
target_step_grid = """    function stepGridCols(abId, delta) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.gridCols = Math.max(0, Math.min(24, (ab.gridCols !== undefined ? ab.gridCols : 4) + delta));
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }

    function stepGridRows(abId, delta) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.gridRows = Math.max(0, Math.min(48, (ab.gridRows !== undefined ? ab.gridRows : 8) + delta));
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }"""

replacement_step_grid = """    function toggleGridCols(abId) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.showCols = ab.showCols === undefined ? false : !ab.showCols;
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }

    function toggleGridRows(abId) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.showRows = ab.showRows === undefined ? false : !ab.showRows;
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }

    function stepGridCols(abId, delta) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.showCols = true; // Auto-attiva quando l'utente modifica il numero
      ab.gridCols = Math.max(0, Math.min(24, (ab.gridCols !== undefined ? ab.gridCols : 4) + delta));
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }

    function stepGridRows(abId, delta) {
      const ab = state.artboards.find(a => a.id === abId);
      if (!ab) return;
      ab.showRows = true; // Auto-attiva quando l'utente modifica il numero
      ab.gridRows = Math.max(0, Math.min(48, (ab.gridRows !== undefined ? ab.gridRows : 8) + delta));
      rebuildArtboardDOM();
      renderAll();
      history.push();
    }"""

assert target_step_grid in content, "Target 5 (Step Grid functions) not found"
content = content.replace(target_step_grid, replacement_step_grid, 1)

# -----------------------------------------------------------------------------
# 6. drawHeatmapToCanvas(ctx, ab): Exact 1:1 match to scientific CSS
# -----------------------------------------------------------------------------
target_draw_heatmap = """        // 4. Dual Natural Crest (Golden Overlap at bottom-center)
        ctx.save();
        ctx.translate(w * 0.5, h * 0.82);
        ctx.scale(1.0, 0.5);
        const ovalGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, w * 0.45);
        ovalGrad.addColorStop(0, 'rgba(204, 255, 0, 0.6)');
        ovalGrad.addColorStop(0.45, 'rgba(16, 185, 129, 0.45)');
        ovalGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = ovalGrad;
        ctx.beginPath();
        ctx.arc(0, 0, w * 0.45, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();"""

replacement_draw_heatmap = """        // 4. Dual Natural Crest (Golden Overlap at bottom-center) - Exact 1:1 match to scientific CSS
        ctx.save();
        ctx.translate(w * 0.5, h * 0.82);
        ctx.scale(1.0, 0.49);
        const ovalGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, w * 0.45);
        ovalGrad.addColorStop(0, 'rgba(16, 185, 129, 0.55)');
        ovalGrad.addColorStop(0.45, 'rgba(16, 185, 129, 0.4)');
        ovalGrad.addColorStop(0.75, 'transparent');
        ovalGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = ovalGrad;
        ctx.beginPath();
        ctx.arc(0, 0, w * 0.45, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();"""

assert target_draw_heatmap in content, "Target 6 (Canvas Heatmap Match) not found"
content = content.replace(target_draw_heatmap, replacement_draw_heatmap, 1)

if crlf:
    content = content.replace('\n', '\r\n')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Scientific Comfort & Grid ON/OFF fixes applied cleanly!")
