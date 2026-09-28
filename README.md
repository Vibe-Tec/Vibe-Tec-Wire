# 🎮 VIBE-TEC WIRE (v3.9) — Cognitive UX Studio
> **Proprietà & Autore**: Leonardo Sorrentino  
> **Ruolo**: Lead UX/UI Product Designer & AI Systems Engineer  
> **Brand Source of Truth**: Vibe-Tec  
> **Portfolio Ufficiale**: [pip-folio.vercel.app](https://pip-folio.vercel.app)

---

## 🌌 Panoramica del Progetto
**Vibe-Tec Wire** è lo studio di wireframing, prototipazione rapida e validazione ergonomica cognitiva sviluppato su misura per Leonardo Sorrentino.  
Costruito in **puro SVG DOM** in un singolo file HTML, gira **offline** (CSS Tailwind compilato inline, nessun CDN).

---

## ⚡ Caratteristiche & Architettura Core (v3.9)
- **📐 Motore Vettoriale SVG DOM Puro**: selezione, spostamento, ridimensionamento e rotazione su nodi SVG.
- **✨ 52 Icone Vettoriali**: libreria inline (`ICONS_LIBRARY`); click sul canvas o sotto la selezione. `assets/icons/` è solo riferimento visivo.
- **🔲 Anteprima Tratteggiata**: durante il drag di creazione la forma è tratteggiata; al mouseup diventa solida.
- **🧭 Smart Guides Magnetiche stile Figma**: snap micro (oggetti, anche sul canvas mondo) e macro (artboard) — `#smart-guides-layer`.
- **📊 Stepper Colonne e Righe Indipendenti**: colonne blu e righe 8pt ciano, toggle ON/OFF per artboard.
- **⚡ Auto-Layout v1**: su `wire_component` (contenitore). Direzione V/H, padding 8/16/24, gap 8/12/16, figli con `parentId`. I container si possono **annidare**. Niente wrap.
- **▭ Frame libero**: canvas ridimensionabile (angoli, passo 8pt), senza maschera device.
- **🖱️ Marquee**: col tool Selezione, trascina sul vuoto per selezionare più oggetti (Shift aggiunge).
- **📦 Container UI Kit Grigio**: box `wire_component` per sezioni, card e moduli.
- **🖐️ Mappe Biomeccaniche Thumb-Zone** (solo **mobile**, ricerca Hoober & Clark):
  - Verde (zona naturale)
  - Ambra (estensione)
  - Rosso (Ow-Zone alta)
- **📷 Esportazione PNG**: schermo singolo a **3×**; lavagna intera **scalata** per entrare in 4000px (niente crop). Modalità Clean (handoff) o Heatmap (case study).
- **⚡ Design Tokens W3C** e **Inspector WCAG**: contrasto reale (luminanza relativa) e check griglia 8pt.

---

## 🚀 Avvio Rapido
Fai doppio clic su **`01 - Apri Vibe-Tec Wire.bat`** per aprire la lavagna nel browser predefinito. Non serve rete.

---
*Vibe-Tec Wire v3.9 · Ecosistema Vibe-Tec — Certificato per Leonardo Sorrentino*
