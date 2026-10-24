# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v5
- Force the month labels to align with the grid columns (both LTR)
- Fix the mismatch where labels were positioned from the right while cells flowed from the left
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — CSS: fix month label positioning (force LTR, use left)
# ======================================================================
OLD_CSS = """.heatmap-months{position:relative;height:70px;font-size:.68rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content}
.heatmap-months span{position:absolute;bottom:4px;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px}
"""

NEW_CSS = """.heatmap-months{position:relative;height:70px;font-size:.68rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content;text-align:left}
.heatmap-months span{position:absolute;bottom:4px;left:0;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px;direction:ltr;text-align:left}
"""

# ======================================================================
# STEP 2 — JS: use a wrapper element to fix positioning once and for all
# ======================================================================
OLD_JS = """    // Month label at the top of the first week of each new month
    const firstDayOfWeek = new Date(start.getFullYear(), start.getMonth(), start.getDate() + w * 7);
    const mIdx = firstDayOfWeek.getMonth();
    if (mIdx !== lastMonthShown) {
      const span = document.createElement('span');
      const cal = state.user.cal === 'gregorian' ? 'gregorian' : state.user.cal;
      span.textContent = monthName(cal, mIdx, state.user.lang);
      span.style.left = (w * 15) + 'px';   // 12px cell + 3px gap
      months.appendChild(span);
      lastMonthShown = mIdx;
    }"""

NEW_JS = """    // Month label at the top of the first week of each new month
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
        ("CSS months LTR fix", OLD_CSS, NEW_CSS),
        ("JS months left override", OLD_JS, NEW_JS),
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
    backup = f"{SRC}.heatmapv5-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v5 applied.")


if __name__ == "__main__":
    main()