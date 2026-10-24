# -*- coding: utf-8 -*-
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# --- کد CSS دقیقاً به همون شکلی که توی فایل تو هست ---
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;-webkit-overflow-scrolling:touch;direction:ltr;}
.heatmap-wrapper{display:flex;flex-direction:row;gap:3px;min-width:max-content;direction:ltr;}
.heatmap-week-col{display:flex;flex-direction:column;gap:3px;align-items:center;}
.heatmap-month-label{height:65px;font-size:.68rem;color:var(--dim);writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;display:flex;align-items:flex-end;justify-content:center;}
.heatmap-cells-col{display:flex;flex-direction:column;gap:3px;}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s;}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative;}
.heatmap-cell[data-lvl="0"]{background:var(--surface2);}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2));}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2));}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2));}
.heatmap-cell[data-lvl="4"]{background:var(--success);}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end;}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px;}"""

# --- ما کد CSS رو اصلا تغییر نمی‌دیم، چون کدهای تو از قبل درست هستن! ---
# فقط کدهای JS رو درست می‌کنیم که مربع‌ها و ماه‌ها رو با هم هماهنگ کنه.

OLD_JS = """  grid.innerHTML = '';

  // Create the flex container that holds all weeks
  const flexContainer = document.createElement('div');
  flexContainer.className = 'heatmap-flex-container';
  grid.appendChild(flexContainer);

  // Iterate week by week, starting Saturday
  const totalDays = Math.floor((new Date(now.getFullYear(), now.getMonth(), now.getDate()) - start) / 86400000) + 1;
  const weeks = Math.ceil(totalDays / 7);
  let lastMonthShown = -1;

  for (let w = 0; w < weeks; w++) {
    const weekDiv = document.createElement('div');
    weekDiv.className = 'heatmap-week';

    // --- Month label (only if the month changed since last week) ---
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const label = document.createElement('div');
      label.className = 'heatmap-week-label';
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      label.textContent = monthName(cal, mIdx, state.user.lang);
      weekDiv.appendChild(label);
      lastMonthShown = mIdx;
    } else {
      // Add an empty spacer for alignment
      const spacer = document.createElement('div');
      spacer.className = 'heatmap-week-label';
      spacer.style.visibility = 'hidden';
      weekDiv.appendChild(spacer);
    }

    // --- 7 day cells ---
    const cellsDiv = document.createElement('div');
    cellsDiv.className = 'heatmap-week-cells';
    for (let d = 0; d < 7; d++) {
      const dayOffset = w * 7 + d;
      const dt = new Date(start.getFullYear(), start.getMonth(), start.getDate() + dayOffset);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      if (dt > now) {
        cell.style.visibility = 'hidden';
      } else {
        const key = dateKey(dt);
        const mins = totals[key] || 0;
        const lvl = level(mins);
        cell.setAttribute('data-lvl', lvl);
        cell.setAttribute('title', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
        cell.setAttribute('aria-label', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
        cell.tabIndex = 0;
      }
      cellsDiv.appendChild(cell);
    }
    weekDiv.appendChild(cellsDiv);
    flexContainer.appendChild(weekDiv);
  }
}"""

NEW_JS = """  grid.innerHTML = '';

  // Create the wrapper that holds all week columns
  const wrapper = document.createElement('div');
  wrapper.className = 'heatmap-wrapper';
  grid.appendChild(wrapper);

  const totalDays = Math.floor((new Date(now.getFullYear(), now.getMonth(), now.getDate()) - start) / 86400000) + 1;
  const weeks = Math.ceil(totalDays / 7);
  let lastMonthShown = -1;

  for (let w = 0; w < weeks; w++) {
    const col = document.createElement('div');
    col.className = 'heatmap-week-col';

    // 1. Month Label
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    const labelDiv = document.createElement('div');
    labelDiv.className = 'heatmap-month-label';
    
    if (mIdx !== lastMonthShown) {
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      labelDiv.textContent = monthName(cal, mIdx, state.user.lang);
      lastMonthShown = mIdx;
    } else {
      labelDiv.style.visibility = 'hidden';
    }
    col.appendChild(labelDiv);

    // 2. Day Cells (7 squares)
    const cellsCol = document.createElement('div');
    cellsCol.className = 'heatmap-cells-col';
    for (let d = 0; d < 7; d++) {
      const dayOffset = w * 7 + d;
      const dt = new Date(start.getFullYear(), start.getMonth(), start.getDate() + dayOffset);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      if (dt > now) {
        cell.style.visibility = 'hidden';
      } else {
        const key = dateKey(dt);
        const mins = totals[key] || 0;
        const lvl = level(mins);
        cell.setAttribute('data-lvl', lvl);
        cell.setAttribute('title', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
        cell.setAttribute('aria-label', L.heatmapTooltip(fmtDate(dt, state.user.lang, state.user.cal), num(mins, state.user.lang)));
        cell.tabIndex = 0;
      }
      cellsCol.appendChild(cell);
    }
    col.appendChild(cellsCol);
    wrapper.appendChild(col);
  }
}"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    
    # جایگزینی فقط کد JS (چون کد CSS تو الان از قبل درست و به‌روزه)
    if text.count(OLD_JS) == 0:
        print("[ABORT] Old JS block not found. Did you change it?")
        sys.exit(2)
    
    text = text.replace(OLD_JS, NEW_JS, 1)
    
    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("[DONE] Heatmap Final applied perfectly.")

if __name__ == "__main__":
    main()