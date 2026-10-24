# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
        
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # پیدا کردن آخرین خط CSS هیت‌مپ (که ممکنه آکولادش جا افتاده باشه)
    # ما به جای دست زدن به کدهای قبلی، فقط مطمئن می‌شیم که قبل از .bnav یه آکولاد بسته باشه
    old_snippet = """.heatmap-legend .cell{width:12px;height:12px;border-radius:2px;}
.bnav{position:fixed;bottom:0;left:0;right:0;z-index:50;"""

    new_snippet = """.heatmap-legend .cell{width:12px;height:12px;border-radius:2px;}
}

.bnav{position:fixed;bottom:0;left:0;right:0;z-index:50;"""

    if old_snippet in text:
        text = text.replace(old_snippet, new_snippet, 1)
        print("[OK] Missing closing brace added before .bnav")
    else:
        # اگه دقیقاً این نبود، شاید یه جای دیگه باشه. بذار یه بک‌آپ ساده کنیم:
        print("[WARN] Could not find exact .bnav snippet. Attempting generic fix...")
        # یه راه دیگه: پیدا کردن .bnav و اضافه کردن } قبلش
        idx = text.find(".bnav{position:fixed")
        if idx != -1:
            # چک کن آیا قبلش } هست یا نه
            before = text[max(0, idx-10):idx]
            if "}" not in before:
                text = text[:idx] + "}\n" + text[idx:]
                print("[OK] Inserted missing brace before .bnav")
            else:
                print("[SKIP] .bnav already preceded by brace.")
        else:
            print("[ABORT] .bnav not found at all.")
            sys.exit(2)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    
    print("[DONE] Nav bar fix applied.")

if __name__ == "__main__":
    main()