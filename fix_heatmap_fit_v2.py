# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
        
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # ۱. حذف اسکرول افقی و پر کردن عرض
    text = text.replace(
        ".heatmap-scroll{overflow-x:auto;overflow-y:hidden;padding-bottom:6px;-webkit-overflow-scrolling:touch;direction:ltr;}",
        ".heatmap-scroll{overflow-x:hidden;overflow-y:hidden;padding-bottom:6px;direction:ltr;width:100%;}"
    )
    # در صورتی که کلاس اسکرول کمی فرق داشت
    if "overflow-x:auto" in text:
        text = text.replace("overflow-x:auto", "overflow-x:hidden")

    # ۲. فاصله بین ستون‌ها و مربع‌ها رو کم کن
    text = text.replace("gap:3px;min-width:max-content;", "gap:2px;width:100%;")
    
    # ۳. عرض ستون‌ها رو تقسیم کن
    text = text.replace(
        ".heatmap-week-col{display:flex;flex-direction:column;gap:3px;align-items:center;}",
        ".heatmap-week-col{display:flex;flex-direction:column;gap:2px;align-items:center;flex:1;}"
    )

    # ۴. مربع‌ها رو نسبی کن تا همیشه مربع بمونن
    text = text.replace(
        ".heatmap-cell{width:12px;height:12px;border-radius:2px;background:var(--surface2);transition:transform .15s;}",
        ".heatmap-cell{width:100%;aspect-ratio:1;border-radius:2px;background:var(--surface2);transition:transform .15s;}"
    )

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    
    print("[DONE] Heatmap resized to fit screen.")

if __name__ == "__main__":
    main()