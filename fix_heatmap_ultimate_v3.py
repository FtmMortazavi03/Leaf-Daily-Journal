# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

NEW_FUNC = """function renderHeatmap() {
  const grid = $('heatmapGrid');
  if (!grid) return;
  
  const L = t();
  $('heatmapTitle').textContent = L.heatmapTitle;
  $('heatmapSub').textContent = L.heatmapSub;
  $('heatmapLess').textContent = L.heatmapLess;
  $('heatmapMore').textContent = L.heatmapMore;

  const totals = {};
  const now = new Date();
  
  // ===== بازه: از اول همین ماه، سال قبل =====
  const start = new Date(now.getFullYear() - 1, now.getMonth(), 1);
  // تراز با شنبه (اول هفته)
  const offset = (start.getDay() - SATURDAY_DOW + 7) % 7;
  start.setDate(start.getDate() - offset);

  state.sessions.forEach(s => {
    if (s.date >= dateKey(start) && s.date <= today()) {
      totals[s.date] = (totals[s.date] || 0) + s.durationMinutes;
    }
  });

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
  
  const wrapper = document.createElement('div');
  wrapper.className = 'heatmap-wrapper';
  grid.appendChild(wrapper);

  const totalDays = Math.floor((new Date(now.getFullYear(), now.getMonth(), now.getDate()) - start) / 86400000) + 1;
  const weeks = Math.ceil(totalDays / 7);
  let lastMonthShown = -1;

  const cols = [];

  for (let w = 0; w < weeks; w++) {
    const col = document.createElement('div');
    col.className = 'heatmap-week-col';

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
    cols.push(col);
  }

  // تشخیص خودکار RTL/LTR
  const isRTL = document.documentElement.getAttribute('dir') === 'rtl';
  if (isRTL) {
    for (let i = cols.length - 1; i >= 0; i--) wrapper.appendChild(cols[i]);
  } else {
    for (let i = 0; i < cols.length; i++) wrapper.appendChild(cols[i]);
  }
}"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "function renderHeatmap() {"
    end_marker = "\nfunction renderWeek() {" 
    
    start_idx = text.find(start_marker)
    if start_idx == -1:
        print("[ABORT] Could not find start of renderHeatmap."); sys.exit(2)
        
    end_idx = text.find(end_marker, start_idx)
    if end_idx == -1:
        print("[ABORT] Could not find end of renderHeatmap."); sys.exit(2)

    new_text = text[:start_idx] + NEW_FUNC + text[end_idx:]
    
    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print("[DONE] Heatmap v3 applied (1-year-same-month range + auto RTL/LTR).")

if __name__ == "__main__":
    main()