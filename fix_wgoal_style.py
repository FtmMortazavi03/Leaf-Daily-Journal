# -*- coding: utf-8 -*-
import sys, os
import re

SRC = os.path.join("src", "index.html")

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # پیدا کردن بلوک CSS مربوط به wgoal
    # ما از کامنت /* STATS */ یا از خود .wgoal شروع می‌کنیم تا قبل از بخش بعدی
    # اما چون فایل بزرگه، بیایم و فقط استایل‌های wgoal رو با یه نسخه تمیز جایگزین کنیم.
    
    # الگوی پیدا کردن کلاس‌های wgoal، winput و wprog (حتی اگه بهم ریخته باشن)
    # ما دنبال .wgoal{...} تا .winput button:hover{...} می‌گردیم.
    
    pattern = re.compile(r"\.wgoal\{.*?\.winput button:hover\{[^}]*\}", re.DOTALL)
    
    # استایل جدید و تمیز (بر اساس کد اصلی خودت)
    NEW_CSS = """
.wgoal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
.wgoal h3{font-size:.9rem;font-weight:600;margin-bottom:14px;color:var(--muted)}
.winput{display:flex;gap:8px;align-items:center}
.winput input{flex:1;padding:12px 14px;border-radius:10px;border:1px solid var(--border2);background:var(--bg);color:var(--text);font-size:1rem;font-weight:700;text-align:center;font-variant-numeric:tabular-nums}
.winput input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.winput .unit{font-size:.82rem;color:var(--muted)}
.winput button{padding:12px 18px;border-radius:10px;background:var(--accent);color:var(--accent-text);font-weight:700;font-size:.85rem;transition:.2s}
.winput button:hover{opacity:.9;transform:translateY(-1px)}
"""

    if not pattern.search(text):
        print("[ABORT] Could not find the Weekly Goal CSS block.")
        sys.exit(2)

    # جایگزینی
    text = pattern.sub(NEW_CSS.strip(), text, count=1)

    # حالا یه چک بکنیم که آیا .wprog هم هست یا نه (چون توی الگو نبود)
    # در واقع .wprog باید بعد از .winput button:hover باشه، پس ما فقط بخش اول رو عوض کردیم.
    # برای اطمینان، بیایم و کل بلوک stats رو دوباره از اول بنویسیم.
    # این ساده‌تره.
    
    # پیدا کردن از /* STATS */ تا قبل از /* SETTINGS */
    pattern_stats = re.compile(r"/\* STATS \*/.*?(?=/\* SETTINGS \*/)", re.DOTALL)
    
    FULL_STATS_CSS = """/* STATS */
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:16px 12px;text-align:center;transition:.2s}
.stat:hover{border-color:var(--accent);transform:translateY(-2px)}
.stat .v{font-size:1.4rem;font-weight:800;font-variant-numeric:tabular-nums;line-height:1;color:var(--accent)}
.stat .l{font-size:.72rem;color:var(--muted);margin-top:6px}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:16px}
.chart-card h3{font-size:.9rem;font-weight:600;margin-bottom:16px;color:var(--muted)}
.chart-wrap{position:relative;height:220px;width:100%}
.chart-wrap.donut{height:200px}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;justify-content:center}
.litem{display:flex;align-items:center;gap:6px;font-size:.75rem;color:var(--muted)}
.litem .dot{width:8px;height:8px;border-radius:50%}

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

    if pattern_stats.search(text):
        text = pattern_stats.sub(FULL_STATS_CSS, text, count=1)
        print("[OK] Full STATS CSS block replaced with clean version.")
    else:
        print("[ABORT] Could not find the STATS block.")
        sys.exit(2)

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("[DONE] Weekly Goal UI fixed.")

if __name__ == "__main__":
    main()