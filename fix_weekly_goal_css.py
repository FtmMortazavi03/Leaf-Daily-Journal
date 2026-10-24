# -*- coding: utf-8 -*-
import sys, os

CSS_FILE = os.path.join("src", "styles.css")

# استایل‌های اصلی بخش هدف هفتگی (بر اساس اسکرین‌شات و کد اولیه)
WGOAL_CSS = """
.wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
.wgoal h3{font-size:.9rem;font-weight:600;margin-bottom:14px;color:var(--muted)}
.winput{display:flex;gap:8px;align-items:center}
.winput input{flex:1;padding:12px 14px;border-radius:10px;border:1px solid var(--border2);background:var(--bg);color:var(--text);font-size:1rem;font-weight:700;text-align:center;font-variant-numeric:tabular-nums}
.winput input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.winput .unit{font-size:.82rem;color:var(--muted)}
.winput button{padding:12px 18px;border-radius:10px;background:var(--accent);color:var(--accent-text);font-weight:700;font-size:.85rem;transition:.2s}
.winput button:hover{opacity:.9;transform:translateY(-1px)}
.wprog{margin-top:14px}
.wrow{display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:6px;font-variant-numeric:tabular-nums}
"""

def main():
    if not os.path.isfile(CSS_FILE):
        print(f"[ERROR] File not found: {CSS_FILE}"); sys.exit(1)

    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # چک کن که آیا این استایل‌ها از قبل وجود دارن یا نه
    if ".wgoal{" in css:
        print("[SKIP] Weekly goal CSS already exists. No changes needed.")
        sys.exit(0)

    # پیدا کردن جای مناسب برای اضافه کردن (قبل از استایل‌های هیت‌مپ)
    marker = "/* Heatmap */"
    if marker in css:
        css = css.replace(marker, WGOAL_CSS + "\n" + marker, 1)
        print("[OK] Weekly goal CSS restored before Heatmap CSS")
    else:
        # اگه هیت‌مپ نبود، به انتهای فایل اضافه کن
        css += "\n" + WGOAL_CSS
        print("[OK] Weekly goal CSS appended to the end of styles.css")

    with open(CSS_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(css)

    print("[DONE] Weekly goal CSS fixed.")

if __name__ == "__main__":
    main()