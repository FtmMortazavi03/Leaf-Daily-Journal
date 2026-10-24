# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

# پیدا کردن استایل‌های فعلی و تغییر اندازه‌ها
OLD_CSS = """.heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;-webkit-overflow-scrolling:touch;direction:ltr;}
.heatmap-wrapper{display:flex;flex-direction:row;gap:3px;min-width:max-content;direction:ltr;}
.heatmap-week-col{display:flex;flex-direction:column;gap:3px;align-items:center;}
.heatmap-cells-col{display:flex;flex-direction:column;gap:3px;}
.heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s;}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative;}"""

NEW_CSS = """.heatmap-scroll{overflow-x:hidden;overflow-y:hidden;padding-bottom:6px;direction:ltr;width:100%;}
.heatmap-wrapper{display:flex;flex-direction:row;gap:2px;width:100%;direction:ltr;justify-content:space-between;}
.heatmap-week-col{display:flex;flex-direction:column;gap:2px;align-items:center;flex:1;}
.heatmap-cells-col{display:flex;flex-direction:column;gap:2px;width:100%;}
.heatmap-cell{width:100%;aspect-ratio:1;border-radius:2px;background:var(--surface2);transition:transform .15s;}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative;}"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
        
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    if OLD_CSS not in text:
        print("[ABORT] Could not find the old heatmap CSS. Did you change it?")
        sys.exit(2)

    text = text.replace(OLD_CSS, NEW_CSS, 1)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("[DONE] Heatmap resized to fit screen (no scroll).")

if __name__ == "__main__":
    main()