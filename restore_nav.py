# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

# کد CSS نوار پایین (از روی عکس و کدهای اصلی)
NAV_CSS = """
.bnav{position:fixed;bottom:0;left:0;right:0;z-index:50;background:color-mix(in srgb,var(--surface) 92%,transparent);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-top:1px solid var(--border);display:flex;justify-content:space-around;padding:8px 0 14px;max-width:720px;margin:0 auto}
.nav-btn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:8px 4px;color:var(--muted);font-size:.68rem;font-weight:500;transition:.2s;position:relative}
.nav-btn .ico{width:22px;height:22px}
.nav-btn.active{color:var(--accent)}
.nav-btn.active::after{content:'';position:absolute;bottom:-2px;width:16px;height:2px;border-radius:2px;background:var(--accent)}
"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
        
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # پیدا کردن جایی که باید اضافه بشه
    # ما کد رو قبل از کلاس .toast یا .mbg اضافه می‌کنیم
    if ".bnav" in text:
        print("[SKIP] .bnav already exists in file. No changes.")
        sys.exit(0)

    marker = ".toast{"
    if marker in text:
        text = text.replace(marker, NAV_CSS + "\n" + marker, 1)
        print("[OK] .bnav CSS restored before .toast")
    else:
        # اگه .toast هم نبود، بذار یه جای دیگه
        marker = "</style>"
        text = text.replace(marker, NAV_CSS + "\n" + marker, 1)
        print("[OK] .bnav CSS restored before </style>")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("[DONE] Nav bar CSS restored.")

if __name__ == "__main__":
    main()