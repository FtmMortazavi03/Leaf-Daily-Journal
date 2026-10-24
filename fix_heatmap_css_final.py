# -*- coding: utf-8 -*-
import sys, os
import re

SRC = os.path.join("src", "index.html")

# کد CSS جدید و تمیز (بدون اسکرول، پر کردن عرض، مربع‌های نسبی)
NEW_CSS = """/* Heatmap */
.heatmap-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
.heatmap-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.heatmap-head h3{font-size:.9rem;font-weight:600;color:var(--muted);margin:0}
.heatmap-head .sub{font-size:.75rem;color:var(--dim)}
.heatmap-scroll{overflow-x:hidden;width:100%;padding-bottom:6px;direction:ltr;}
.heatmap-wrapper{display:flex;flex-direction:row;gap:2px;width:100%;direction:ltr;justify-content:space-between;}
.heatmap-week-col{display:flex;flex-direction:column;gap:2px;align-items:center;flex:1;}
.heatmap-cells-col{display:flex;flex-direction:column;gap:2px;width:100%;}
.heatmap-cell{width:100%;aspect-ratio:1;border-radius:2px;background:var(--surface2);transition:transform .15s;}
.heatmap-cell:hover{transform:scale(1.4);outline:1px solid var(--text);outline-offset:1px;cursor:pointer;z-index:2;position:relative;}
.heatmap-cell[data-lvl="0"]{background:var(--surface2);}
.heatmap-cell[data-lvl="1"]{background:color-mix(in srgb, var(--success) 25%, var(--surface2));}
.heatmap-cell[data-lvl="2"]{background:color-mix(in srgb, var(--success) 50%, var(--surface2));}
.heatmap-cell[data-lvl="3"]{background:color-mix(in srgb, var(--success) 75%, var(--surface2));}
.heatmap-cell[data-lvl="4"]{background:var(--success);}
.heatmap-legend{display:flex;align-items:center;gap:6px;margin-top:12px;font-size:.72rem;color:var(--dim);justify-content:flex-end;}
.heatmap-legend .cell{width:12px;height:12px;border-radius:2px;}
"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
        
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # پیدا کردن بلوک CSS هیت‌مپ از کامنت /* Heatmap */ تا قبل از .toast یا هر چیز دیگه
    # با یه الگوی ساده: از /* Heatmap */ تا اولین خط خالی که بعدش یه کلاس جدید شروع می‌شه
    pattern = re.compile(r"/\* Heatmap \*/.*?(?=\n\.toast|\n\.mbg|\n\.footer|\Z)", re.DOTALL)
    
    if not pattern.search(text):
        print("[ABORT] Could not find the Heatmap CSS block.")
        sys.exit(2)

    # جایگزینی با CSS جدید
    new_text = pattern.sub(NEW_CSS, text, count=1)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    
    print("[DONE] Heatmap CSS completely replaced and fixed.")

if __name__ == "__main__":
    main()