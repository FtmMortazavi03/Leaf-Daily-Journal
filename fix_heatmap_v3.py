# -*- coding: utf-8 -*-
"""
Leaf — Heatmap v3
- Force LTR on grid (so columns go left-to-right in all languages)
- Fix month label alignment (use inset-inline-start for RTL safety)
- Minor spacing tweaks
"""
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

# ======================================================================
# STEP 1 — CSS: force LTR on grid and cells, fix legend
# ======================================================================
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
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

NEW_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;direction:ltr;-webkit-overflow-scrolling:touch}
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
.heatmap-months{position:relative;height:16px;font-size:.65rem;color:var(--dim);margin-bottom:4px;direction:ltr;min-width:max-content}
.heatmap-months span{position:absolute;top:0;transform:translateX(-2px);white-space:nowrap}
"""


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

    result = apply(text, "CSS LTR fix", OLD_CSS, NEW_CSS)
    if result is None:
        print("\n[ABORT] No changes written.")
        sys.exit(2)
    text = result

    if "</html>" not in text or "})();" not in text:
        print("[ABORT] Result incomplete. Nothing written."); sys.exit(3)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{SRC}.heatmapv3-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"\n[INFO] Backup saved: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC} ({len(text)} chars, delta +{len(text) - original_len})")
    print("[DONE] Heatmap v3 applied.")


if __name__ == "__main__":
    main()