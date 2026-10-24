# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v7
- Force dir="ltr" directly on the grid element in HTML (not just CSS)
- This overrides the inherited RTL from <html dir="rtl">
- Guarantees that column 1 = leftmost, column N = rightmost
- Month labels and day cells then align perfectly
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — HTML: add dir="ltr" to the grid
# ======================================================================
OLD_HTML = """      <div class="heatmap-scroll">
        <div class="heatmap-grid" id="heatmapGrid"></div>
      </div>"""

NEW_HTML = """      <div class="heatmap-scroll" dir="ltr">
        <div class="heatmap-grid" id="heatmapGrid" dir="ltr"></div>
      </div>"""

# ======================================================================
# STEP 2 — CSS: ensure direction is LTR, remove any RTL inheritance
# ======================================================================
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
.heatmap-grid{display:grid;grid-template-rows:70px repeat(7, 12px);grid-auto-flow:column;grid-auto-columns:12px;gap:3px;min-width:max-content;direction:ltr}
.heatmap-month{grid-row:1;font-size:.68rem;color:var(--dim);writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px;align-self:end;justify-self:start;direction:ltr}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s;direction:ltr}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative}
.heatmap-cell[data-lvl="0"]{background:var(--surface2)}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2))}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2))}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2))}
.heatmap-cell[data-lvl="4"]{background:var(--success)}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end;direction:ltr}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px}
"""

NEW_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;-webkit-overflow-scrolling:touch}
.heatmap-grid{display:grid;grid-template-rows:70px repeat(7, 12px);grid-auto-flow:column;grid-auto-columns:12px;gap:3px;min-width:max-content}
.heatmap-month{grid-row:1;font-size:.68rem;color:var(--dim);writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px;align-self:end;justify-self:start}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative}
.heatmap-cell[data-lvl="0"]{background:var(--surface2)}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2))}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2))}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2))}
.heatmap-cell[data-lvl="4"]{background:var(--success)}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px}
"""

# ======================================================================
# STEP 3 — JS: no change needed, but keep a robust fallback
# ======================================================================
OLD_JS_HEAD = """function renderHeatmap() {
  const grid = $('heatmapGrid');
  if (!grid) return;"""
NEW_JS_HEAD = """function renderHeatmap() {
  const grid = $('heatmapGrid');
  if (!grid) return;
  // Force LTR on the grid element itself (in case a parent forces RTL)
  grid.setAttribute('dir', 'ltr');
  grid.style.direction = 'ltr';"""


def apply(text, label, old, new):
    count = text.count(old)
    if count == 0:
        print(f"[ABORT] Not found: {label}")
        return None
    if count > 1:
        print(f"[ABORT] Ambiguous ({count}x): {label}")
        return None
    print(f"[OK] {label}")
    return text.replace(old, new, 1)


def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    original_len = len(text)
    print(f"[INFO] Loaded {SRC} ({original_len} chars)")

    steps = [
        ("HTML dir=ltr on scroll+grid", OLD_HTML, NEW_HTML),
        ("CSS remove inherited direction", OLD_CSS, NEW_CSS),
        ("JS force dir on render", OLD_JS_HEAD, NEW_JS_HEAD),
    ]

    for label, old, new in steps:
        result = apply(text, label, old, new)
        if result is None:
            print("\n[ABORT] No changes written.")
            sys.exit(2)
        text = result

    if "</html>" not in text or "})();" not in text:
        print("[ABORT] Result incomplete. Nothing written."); sys.exit(3)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{SRC}.heatmapv7-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v7 applied — forced LTR at HTML, CSS, and JS levels.")


if __name__ == "__main__":
    main()