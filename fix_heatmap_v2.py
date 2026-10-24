# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v2
- Move heatmap card to the END of Stats screen (after weekly goal)
- Fix RTL direction issues (force LTR grid, flip month order for RTL)
- Widen the scroll container so all 53 columns are reachable
- Cleaner month labels
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — Remove the old heatmap block from its wrong position
# ======================================================================
OLD_HEATMAP_HTML = """    <div class="heatmap-card">
      <div class="heatmap-head">
        <h3 id="heatmapTitle">Study heatmap</h3>
        <span class="sub" id="heatmapSub">Last 365 days</span>
      </div>
      <div class="heatmap-scroll">
        <div class="heatmap-months" id="heatmapMonths"></div>
        <div class="heatmap-grid" id="heatmapGrid"></div>
      </div>
      <div class="heatmap-legend">
        <span id="heatmapLess">Less</span>
        <span class="cell" data-lvl="0"></span>
        <span class="cell" data-lvl="1"></span>
        <span class="cell" data-lvl="2"></span>
        <span class="cell" data-lvl="3"></span>
        <span class="cell" data-lvl="4"></span>
        <span id="heatmapMore">More</span>
      </div>
    </div>

"""

# The weekly-goal card ends right before the footer. Insert heatmap AFTER it.
WGOAL_END = """    </div>

    <div class="footer">
      <div class="sig">
        <svg viewBox="0 0 24 24"><path d="M17 3a2.83 2.83 0 114 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
        <span id="footerText2">Made by Fatemehsadat Mortazavi</span>
      </div>
    </div>
  </div>

  <div class="screen" id="screen-settings">"""

# Same block but with the heatmap card inserted before the footer
WGOAL_END_WITH_HEATMAP = """    </div>

    <div class="heatmap-card">
      <div class="heatmap-head">
        <h3 id="heatmapTitle">Study heatmap</h3>
        <span class="sub" id="heatmapSub">Last 365 days</span>
      </div>
      <div class="heatmap-scroll">
        <div class="heatmap-months" id="heatmapMonths"></div>
        <div class="heatmap-grid" id="heatmapGrid"></div>
      </div>
      <div class="heatmap-legend">
        <span id="heatmapLess">Less</span>
        <span class="cell" data-lvl="0"></span>
        <span class="cell" data-lvl="1"></span>
        <span class="cell" data-lvl="2"></span>
        <span class="cell" data-lvl="3"></span>
        <span class="cell" data-lvl="4"></span>
        <span id="heatmapMore">More</span>
      </div>
    </div>

    <div class="footer">
      <div class="sig">
        <svg viewBox="0 0 24 24"><path d="M17 3a2.83 2.83 0 114 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
        <span id="footerText2">Made by Fatemehsadat Mortazavi</span>
      </div>
    </div>
  </div>

  <div class="screen" id="screen-settings">"""

# ======================================================================
# STEP 2 — CSS: fix grid direction and width
# ======================================================================
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr}
.heatmap-grid{display:grid;grid-template-rows:repeat(7, 12px);grid-auto-columns:12px;gap:3px;min-width:max-content}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s}
.heatmap-cell:hover{transform:scale(1.3);outline:1px solid var(--text);outline-offset:1px;cursor:pointer}
.heatmap-cell[data-lvl="0"]{background:var(--surface2)}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2))}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2))}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2))}
.heatmap-cell[data-lvl="4"]{background:var(--success)}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px}
.heatmap-months{display:grid;grid-auto-columns:12px;gap:3px;font-size:.65rem;color:var(--dim);margin-bottom:4px;direction:ltr;height:14px}
.heatmap-months span{grid-row:1}
"""

NEW_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
.heatmap-grid{display:grid;grid-template-rows:repeat(7, 12px);grid-auto-flow:column;grid-auto-columns:12px;gap:3px;min-width:max-content}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative}
.heatmap-cell[data-lvl="0"]{background:var(--surface2)}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2))}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2))}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2))}
.heatmap-cell[data-lvl="4"]{background:var(--success)}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px}
.heatmap-months{position:relative;height:16px;font-size:.65rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content}
.heatmap-months span{position:absolute;top:0;transform:translateX(-2px);white-space:nowrap}
"""

# ======================================================================
# STEP 3 — JS: fix month labels (absolute positioning), flip for RTL
# ======================================================================
OLD_JS_MONTHS = """    // Month label at the top of the first week of each new month
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const span = document.createElement('span');
      span.textContent = monthName(state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal, mIdx, state.user.lang).slice(0, 3);
      span.style.gridColumn = String(w + 1);
      months.appendChild(span);
      lastMonthShown = mIdx;
    }"""

NEW_JS_MONTHS = """    // Month label at the top of the first week of each new month
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const span = document.createElement('span');
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      span.textContent = monthName(cal, mIdx, state.user.lang).slice(0, 4);
      span.style.left = (w * 15) + 'px';   // 12px cell + 3px gap
      months.appendChild(span);
      lastMonthShown = mIdx;
    }"""


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
        ("remove old heatmap HTML", OLD_HEATMAP_HTML, ""),
        ("insert heatmap at end (after wgoal)", WGOAL_END, WGOAL_END_WITH_HEATMAP),
        ("CSS fixes", OLD_CSS, NEW_CSS),
        ("JS month labels", OLD_JS_MONTHS, NEW_JS_MONTHS),
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
    backup = f"{SRC}.heatmapv2-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v2 applied.")
    print("\nNEXT: If service worker is still active:")
    print("  - F12 -> Application -> Service workers -> Unregister")
    print("  - Ctrl+Shift+R")


if __name__ == "__main__":
    main()