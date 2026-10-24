# -*- coding: utf-8 -*-
"""
Leaf — Annual heatmap (GitHub-style contribution grid)
- Adds a 7x53 grid in Stats showing the last 365 days
- Color scale based on daily minutes
- Tooltip on hover with localized date + minutes
- Week starts Saturday (matches app convention)
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — i18n strings
# ======================================================================
I18N_EN_OLD = """    noteTooLong:'Note must be 200 characters or less.',"""
I18N_EN_NEW = """    noteTooLong:'Note must be 200 characters or less.',
    heatmapTitle:'Study heatmap',
    heatmapSub:'Last 365 days',
    heatmapLess:'Less',
    heatmapMore:'More',
    heatmapTooltip:(d,m)=>`${d} — ${m} min`,"""

I18N_FA_OLD = """    noteTooLong:'یادداشت باید حداکثر ۲۰۰ کاراکتر باشد.',"""
I18N_FA_NEW = """    noteTooLong:'یادداشت باید حداکثر ۲۰۰ کاراکتر باشد.',
    heatmapTitle:'نقشه حرارتی مطالعه',
    heatmapSub:'۳۶۵ روز اخیر',
    heatmapLess:'کمتر',
    heatmapMore:'بیشتر',
    heatmapTooltip:(d,m)=>`${d} — ${m} دقیقه`,"""

I18N_AR_OLD = """    noteTooLong:'يجب ألا تتجاوز الملاحظة ٢٠٠ حرف.',"""
I18N_AR_NEW = """    noteTooLong:'يجب ألا تتجاوز الملاحظة ٢٠٠ حرف.',
    heatmapTitle:'خريطة حرارية للدراسة',
    heatmapSub:'آخر ٣٦٥ يوماً',
    heatmapLess:'أقل',
    heatmapMore:'أكثر',
    heatmapTooltip:(d,m)=>`${d} — ${m} دقيقة`,"""

# ======================================================================
# STEP 2 — CSS for heatmap
# ======================================================================
CSS_ANCHOR = """.wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}"""
CSS_NEW = """.wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}

/* Heatmap */
.heatmap-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
.heatmap-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.heatmap-head h3{font-size:.9rem;font-weight:600;color:var(--muted);margin:0}
.heatmap-head .sub{font-size:.75rem;color:var(--dim)}
.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr}
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

# ======================================================================
# STEP 3 — HTML: add card in Stats screen (after trend chart)
# ======================================================================
HTML_ANCHOR = """    <div class="chart-card">
      <h3 id="donutLbl">Subject share (this month)</h3>
      <div class="chart-wrap donut"><canvas id="donutChart"></canvas></div>
      <div class="legend" id="donutLegend"></div>
    </div>"""
HTML_NEW = """    <div class="heatmap-card">
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

    <div class="chart-card">
      <h3 id="donutLbl">Subject share (this month)</h3>
      <div class="chart-wrap donut"><canvas id="donutChart"></canvas></div>
      <div class="legend" id="donutLegend"></div>
    </div>"""

# ======================================================================
# STEP 4 — JS: render heatmap after renderDonut()
# ======================================================================
JS_ANCHOR = """function renderWeek() {
  const wk = weekKey();"""
JS_NEW = """function renderHeatmap() {
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
      span.textContent = monthName(state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal, mIdx, state.user.lang).slice(0, 3);
      span.style.gridColumn = String(w + 1);
      months.appendChild(span);
      lastMonthShown = mIdx;
    }
  }
}

function renderWeek() {
  const wk = weekKey();"""

# ======================================================================
# STEP 5 — call renderHeatmap() inside renderAll()
# ======================================================================
RENDERALL_OLD = """  renderStats(); renderTrend(); renderDonut(); renderWeek();"""
RENDERALL_NEW = """  renderStats(); renderTrend(); renderDonut(); renderHeatmap(); renderWeek();"""


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
        ("i18n en", I18N_EN_OLD, I18N_EN_NEW),
        ("i18n fa", I18N_FA_OLD, I18N_FA_NEW),
        ("i18n ar", I18N_AR_OLD, I18N_AR_NEW),
        ("CSS heatmap", CSS_ANCHOR, CSS_NEW),
        ("HTML heatmap", HTML_ANCHOR, HTML_NEW),
        ("JS renderHeatmap", JS_ANCHOR, JS_NEW),
        ("renderAll call", RENDERALL_OLD, RENDERALL_NEW),
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
    backup = f"{SRC}.heatmap-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap added.")


if __name__ == "__main__":
    main()