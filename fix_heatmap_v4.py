# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v4
- Vertical month labels (writing-mode: vertical-rl)
- Taller months container so full names fit
- Show full month names (no truncation)
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — CSS: vertical month labels
# ======================================================================
OLD_CSS = """.heatmap-months{position:relative;height:16px;font-size:.65rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content}
.heatmap-months span{position:absolute;top:0;transform:translateX(-2px);white-space:nowrap}
"""

NEW_CSS = """.heatmap-months{position:relative;height:70px;font-size:.68rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content}
.heatmap-months span{position:absolute;bottom:4px;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;line-height:1;letter-spacing:.2px}
"""

# ======================================================================
# STEP 2 — JS: show full month name (no slice)
# ======================================================================
OLD_JS = """      span.textContent = monthName(cal, mIdx, state.user.lang).slice(0, 4);
      span.style.left = (w * 15) + 'px';   // 12px cell + 3px gap"""

NEW_JS = """      span.textContent = monthName(cal, mIdx, state.user.lang);
      span.style.left = (w * 15) + 'px';   // 12px cell + 3px gap"""


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
        ("CSS vertical months", OLD_CSS, NEW_CSS),
        ("JS full month name", OLD_JS, NEW_JS),
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
    backup = f"{SRC}.heatmapv4-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v4 applied — vertical month labels.")


if __name__ == "__main__":
    main()