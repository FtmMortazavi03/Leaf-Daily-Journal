# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v6
- Put month labels INSIDE the grid's header row, using grid-column
- This guarantees perfect alignment in both LTR and RTL
- No more manual left/right pixel math
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — HTML: unify months + grid into a single grid container
# ======================================================================
OLD_HTML = """      <div class="heatmap-scroll">
        <div class="heatmap-months" id="heatmapMonths"></div>
        <div class="heatmap-grid" id="heatmapGrid"></div>
      </div>"""

NEW_HTML = """      <div class="heatmap-scroll">
        <div class="heatmap-grid" id="heatmapGrid"></div>
      </div>"""

# ======================================================================
# STEP 2 — CSS: months become part of the grid (row 1), cells start at row 2
# ======================================================================
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
.heatmap-grid{display:grid;grid-template-rows:repeat(7, 12px);grid-auto-flow:column;grid-auto-columns:12px;gap:3px;min-width:max-content;direction:ltr}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s;direction:ltr}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative}
.heatmap-cell[data-lvl="0"]{background:var(--surface2)}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2))}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2))}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2))}
.heatmap-cell[data-lvl="4"]{background:var(--success)}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end;direction:ltr}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px}
.heatmap-months{position:relative;height:70px;font-size:.68rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content;text-align:left}
.heatmap-months span{position:absolute;bottom:4px;left:0;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px;direction:ltr;text-align:left}
"""

NEW_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
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

# ======================================================================
# STEP 3 — JS: build everything in one loop, using explicit grid-row/column
# ======================================================================
OLD_JS_BLOCK = """function renderHeatmap() {
  const grid = $('heatmapGrid');
  const months = $('heatmapMonths');
  if (!grid) return;
  const L = t();
  $('heatmapTitle').textContent = L.heatmapTitle;
  $('heatmapSub').textContent = L.heatmapSub;
  $('heatmapLess').textContent = L.heatmapLess;
  $('heatmapMore').textContent = L.heatmapMore;

  // Build per-day totals map for the last 365 days
  const totals = {};
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  start.setDate(start.getDate() - 364);
  // Align start to Saturday (week start)
  const offset = (start.getDay() - SATURDAY_DOW + 7) % 7;
  start.setDate(start.getDate() - offset);

  state.sessions.forEach(s => {
    if (s.date >= dateKey(start) && s.date <= today()) {
      totals[s.date] = (totals[s.date] || 0) + s.durationMinutes;
    }
  });

  // Determine thresholds (quartiles of nonzero days)
  const vals = Object.values(totals).filter(v => v > 0).sort((a,b) => a-b);
  const t1 = vals.length ? vals[Math.floor(vals.length * 0.25)] : 15;
  const t2 = vals.length ? vals[Math.floor(vals.length * 0.50)] : 45;
  const t3 = vals.length ? vals[Math.floor(vals.length * 0.75)] : 90;
  const level = (m) => {
    if (!m) return 0;
    if (m <= t1) return 1;
    if (m <= t2) return 2;
    if (m <= t3) return 3;
    return 4;
  };

  grid.innerHTML = '';
  months.innerHTML = '';

  // Iterate 7 rows x N columns (week by week, starting Saturday)
  const totalDays = Math.floor((new Date(now.getFullYear(), now.getMonth(), now.getDate()) - start) / 86400000) + 1;
  const weeks = Math.ceil(totalDays / 7);
  let lastMonthShown = -1;
  for (let w = 0; w < weeks; w++) {
    for (let d = 0; d < 7; d++) {
      const dayOffset = w * 7 + d;
      const dt = new Date(start.getFullYear(), start.getMonth(), start.getDate() + dayOffset);
      if (dt > now) {
        // future cell: empty placeholder to keep grid rectangular
        const cell = document.createElement('div');
        cell.className = 'heatmap-cell';
        cell.style.visibility = 'hidden';
        grid.appendChild(cell);
        continue;
      }
      const key = dateKey(dt);
      const mins = totals[key] || 0;
      const lvl = level(mins);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      cell.setAttribute('data-lvl', lvl);
      cell.setAttribute('title', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
      cell.setAttribute('aria-label', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
      cell.tabIndex = 0;
      grid.appendChild(cell);
    }
    // Month label at the top of the first week of each new month
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const span = document.createElement('span');
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      span.textContent = monthName(cal, mIdx, state.user.lang);
      span.style.left = (w * 15) + 'px';   // 12px cell + 3px gap
      span.style.right = 'auto';           // explicit override in case of RTL
      months.appendChild(span);
      lastMonthShown = mIdx;
    }
  }
}"""

NEW_JS_BLOCK = """function renderHeatmap() {
  const grid = $('heatmapGrid');
  if (!grid) return;
  const L = t();
  $('heatmapTitle').textContent = L.heatmapTitle;
  $('heatmapSub').textContent = L.heatmapSub;
  $('heatmapLess').textContent = L.heatmapLess;
  $('heatmapMore').textContent = L.heatmapMore;

  // Build per-day totals map for the last 365 days
  const totals = {};
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  start.setDate(start.getDate() - 364);
  // Align start to Saturday (week start)
  const offset = (start.getDay() - SATURDAY_DOW + 7) % 7;
  start.setDate(start.getDate() - offset);

  state.sessions.forEach(s => {
    if (s.date >= dateKey(start) && s.date <= today()) {
      totals[s.date] = (totals[s.date] || 0) + s.durationMinutes;
    }
  });

  // Determine thresholds (quartiles of nonzero days)
  const vals = Object.values(totals).filter(v => v > 0).sort((a,b) => a-b);
  const t1 = vals.length ? vals[Math.floor(vals.length * 0.25)] : 15;
  const t2 = vals.length ? vals[Math.floor(vals.length * 0.50)] : 45;
  const t3 = vals.length ? vals[Math.floor(vals.length * 0.75)] : 90;
  const level = (m) => {
    if (!m) return 0;
    if (m <= t1) return 1;
    if (m <= t2) return 2;
    if (m <= t3) return 3;
    return 4;
  };

  grid.innerHTML = '';

  // Iterate 7 rows x N columns (week by week, starting Saturday)
  const totalDays = Math.floor((new Date(now.getFullYear(), now.getMonth(), now.getDate()) - start) / 86400000) + 1;
  const weeks = Math.ceil(totalDays / 7);
  let lastMonthShown = -1;

  for (let w = 0; w < weeks; w++) {
    // --- Month label (row 1, column w+1) ---
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const span = document.createElement('div');
      span.className = 'heatmap-month';
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      span.textContent = monthName(cal, mIdx, state.user.lang);
      span.style.gridColumn = String(w + 1);
      grid.appendChild(span);
      lastMonthShown = mIdx;
    }
    // --- 7 day cells (rows 2..8, column w+1) ---
    for (let d = 0; d < 7; d++) {
      const dayOffset = w * 7 + d;
      const dt = new Date(start.getFullYear(), start.getMonth(), start.getDate() + dayOffset);
      if (dt > now) continue;
      const key = dateKey(dt);
      const mins = totals[key] || 0;
      const lvl = level(mins);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      cell.setAttribute('data-lvl', lvl);
      cell.setAttribute('title', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
      cell.setAttribute('aria-label', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
      cell.tabIndex = 0;
      cell.style.gridColumn = String(w + 1);
      cell.style.gridRow = String(d + 2);
      grid.appendChild(cell);
    }
  }
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
        ("HTML unify", OLD_HTML, NEW_HTML),
        ("CSS unified grid", OLD_CSS, NEW_CSS),
        ("JS rebuild", OLD_JS_BLOCK, NEW_JS_BLOCK),
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
    backup = f"{SRC}.heatmapv6-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v6 applied — labels and cells share the same grid.")


if __name__ == "__main__":
    main()