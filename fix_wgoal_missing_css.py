# -*- coding: utf-8 -*-
import sys, os

SRC = os.path.join("src", "index.html")

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # خط اول wgoal که توی فایل هست
    OLD_LINE = ".wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}"

    if OLD_LINE not in text:
        print("[ABORT] Could not find the .wgoal line.")
        sys.exit(2)

    # استایل‌های گم‌شده که باید بعد از خط اول اضافه بشن
    MISSING_CSS = """
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

    # اضافه کردن استایل‌ها بلافاصله بعد از خط اول
    new_text = text.replace(OLD_LINE, OLD_LINE + "\n" + MISSING_CSS, 1)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print("[DONE] Missing Weekly Goal CSS restored.")

if __name__ == "__main__":
    main()