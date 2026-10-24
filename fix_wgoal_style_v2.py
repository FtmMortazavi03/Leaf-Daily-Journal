# -*- coding: utf-8 -*-
import sys, os
import re

SRC = os.path.join("src", "index.html")

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # پیدا کردن از .wgoal{ تا قبل از .set-group{ (که بخش بعدی CSS هست)
    # اینطوری همه چیز مربوط به Weekly Goal رو یه جا می‌گیریم
    pattern = re.compile(r"\.wgoal\{.*?(?=\.set-group\{)", re.DOTALL)
    
    if not pattern.search(text):
        print("[ABORT] Could not find the Weekly Goal CSS block (from .wgoal to .set-group).")
        sys.exit(2)

    NEW_CSS = """.wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
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

    text = pattern.sub(NEW_CSS, text, count=1)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("[DONE] Weekly Goal CSS block replaced with a clean version.")

if __name__ == "__main__":
    main()