# -*- coding: utf-8 -*-
"""
Leaf — Build tests.html
Extracts pure functions from index.html and generates a standalone test page.
Does NOT modify index.html.
"""
import sys, os, re

SRC = os.path.join("src", "index.html")
OUT = os.path.join("src", "tests.html")

# ============================================================================
# توابعی که می‌خوایم از index.html استخراج کنیم
# ============================================================================
FUNCTIONS_TO_EXTRACT = [
    "toJalali",
    "toHijri",
    "dateKey",
    "daysAgo",
    "saturdayStartOfWeek",
    "weekKeyFor",
    "weekKey",
    "nextWeekKey",
    "weekRangeFor",
    "isFriday",
    "faNum",
    "arNum",
    "num",
    "clamp",
    "toInt",
    "fmtS",
    "fmtHM",
    "fmtMin",
    "hexToRgb",
    "isLight",
]

# ثابت‌هایی که توابع بهشون نیاز دارن
CONSTANTS = """
const SATURDAY_DOW = 6;
const FRIDAY_DOW = 5;
const MAX_DAILY_MINUTES = 24 * 60;
const PM = ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند'];
const EM = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const HM = ['محرم','صفر','ربيع الأول','ربيع الآخر','جمادى الأولى','جمادى الآخرة','رجب','شعبان','رمضان','شوال','ذو القعدة','ذو الحجة'];
const FW = ['یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه','شنبه'];
const EW = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const AW = ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت'];
"""


def extract_function(text, name):
    """Extract a function body from the source text."""
    # Try both `function name(...)` and `const name = (...)` forms
    pattern = re.compile(
        r"(?:function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{)", re.DOTALL
    )
    m = pattern.search(text)
    if m:
        start = m.start()
        # Count braces to find the end
        depth = 0
        i = m.end() - 1
        while i < len(text):
            if text[i] == '{': depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
            i += 1
    return None


def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] {SRC} not found"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        src = f.read()

    extracted = []
    missing = []
    for fn in FUNCTIONS_TO_EXTRACT:
        body = extract_function(src, fn)
        if body:
            extracted.append(body)
            print(f"[OK] extracted: {fn}")
        else:
            missing.append(fn)
            print(f"[WARN] not found: {fn}")

    if not extracted:
        print("[ABORT] Nothing extracted."); sys.exit(2)

    # ============================================================================
    # تست‌ها
    # ============================================================================
    TESTS = """
const results = [];
function assert(name, cond, detail) {
  results.push({ name, ok: !!cond, detail: detail || '' });
}
function eq(name, actual, expected) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  results.push({ name, ok, detail: ok ? '' : `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}` });
}

// ---------- toJalali ----------
eq('toJalali: 2026-10-24 → 1405-08-02', toJalali(2026, 10, 24), [1405, 8, 2]);
eq('toJalali: 2024-03-20 → 1403-01-01', toJalali(2024, 3, 20), [1403, 1, 1]);
eq('toJalali: 2025-03-21 → 1404-01-01', toJalali(2025, 3, 21), [1404, 1, 1]);

// ---------- toHijri ----------
const [hy, hm, hd] = toHijri(2026, 10, 24);
assert('toHijri: year reasonable', hy >= 1447 && hy <= 1449, `got ${hy}`);
assert('toHijri: month 1-12', hm >= 1 && hm <= 12, `got ${hm}`);
assert('toHijri: day 1-30', hd >= 1 && hd <= 30, `got ${hd}`);

// ---------- dateKey ----------
eq('dateKey: Jan 1 2026', dateKey(new Date(2026, 0, 1)), '2026-01-01');
eq('dateKey: Dec 31 2026', dateKey(new Date(2026, 11, 31)), '2026-12-31');
eq('dateKey: single-digit padding', dateKey(new Date(2026, 0, 5)), '2026-01-05');

// ---------- saturdayStartOfWeek ----------
// شنبه = 6 در getDay()
const sat = saturdayStartOfWeek(new Date(2026, 9, 24)); // این یه شنبه است
eq('saturdayStart: same day', dateKey(sat), '2026-10-24');
const sun = saturdayStartOfWeek(new Date(2026, 9, 25)); // یکشنبه
eq('saturdayStart: Sunday → prev Sat', dateKey(sun), '2026-10-24');

// ---------- num ----------
eq('num en', num(123, 'en'), '123');
eq('num fa', num(123, 'fa'), '۱۲۳');
eq('num ar', num(123, 'ar'), '١٢٣');

// ---------- faNum / arNum ----------
eq('faNum', faNum(456), '۴۵۶');
eq('arNum', arNum(789), '٧٨٩');

// ---------- clamp ----------
eq('clamp below', clamp(-5, 0, 10), 0);
eq('clamp above', clamp(15, 0, 10), 10);
eq('clamp inside', clamp(5, 0, 10), 5);

// ---------- toInt ----------
eq('toInt "42"', toInt('42'), 42);
eq('toInt "abc"', toInt('abc'), 0);
eq('toInt null', toInt(null), 0);

// ---------- fmtS ----------
eq('fmtS 15 en', fmtS(15, 'en'), '15m');
eq('fmtS 90 en', fmtS(90, 'en'), '1:30');
eq('fmtS 60 en', fmtS(60, 'en'), '1h');
eq('fmtS 15 fa', fmtS(15, 'fa'), '۱۵د');
eq('fmtS 90 fa', fmtS(90, 'fa'), '۱:۳۰');
eq('fmtS 90 ar', fmtS(90, 'ar'), '١:٣٠');

// ---------- fmtHM ----------
eq('fmtHM 0 en', fmtHM(0, 'en'), '0:00');
eq('fmtHM 90 en', fmtHM(90, 'en'), '1:30');
eq('fmtHM 5 en', fmtHM(5, 'en'), '0:05');
eq('fmtHM 90 fa', fmtHM(90, 'fa'), '۱:۳۰');
eq('fmtHM 5 fa', fmtHM(5, 'fa'), '۰:۰۵');

// ---------- isLight / hexToRgb ----------
eq('isLight white', isLight('#ffffff'), true);
eq('isLight black', isLight('#000000'), false);
eq('hexToRgb', hexToRgb('#ff8800'), { r: 255, g: 136, b: 0 });

// ============================================================================
// رندر نتایج
// ============================================================================
const passed = results.filter(r => r.ok).length;
const failed = results.filter(r => !r.ok).length;

document.getElementById('summary').innerHTML = `
  <span class="pass">${passed} passed</span>
  ${failed ? `<span class="fail">${failed} failed</span>` : ''}
  <span class="total">${results.length} total</span>
`;

const container = document.getElementById('results');
results.forEach(r => {
  const row = document.createElement('div');
  row.className = 'test ' + (r.ok ? 'ok' : 'nok');
  row.innerHTML = `
    <span class="icon">${r.ok ? '✅' : '❌'}</span>
    <span class="name">${r.name}</span>
    ${r.detail ? `<span class="detail">${r.detail}</span>` : ''}
  `;
  container.appendChild(row);
});

// Expose for console
window.__testResults = results;
console.log(`Tests: ${passed} passed, ${failed} failed`);
"""

    # ============================================================================
    # قالب HTML
    # ============================================================================
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Leaf — Test Suite</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; background: #fafafa; color: #18181b; margin: 0; padding: 24px; line-height: 1.6; }}
  .wrap {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .sub {{ color: #71717a; margin-bottom: 24px; }}
  #summary {{ display: flex; gap: 12px; margin-bottom: 16px; font-weight: 700; }}
  #summary .pass {{ color: #16a34a; }}
  #summary .fail {{ color: #dc2626; }}
  #summary .total {{ color: #71717a; }}
  .test {{ display: flex; align-items: flex-start; gap: 8px; padding: 8px 12px; border-radius: 8px; margin-bottom: 4px; font-size: .88rem; }}
  .test.ok {{ background: rgba(22,163,74,.06); }}
  .test.nok {{ background: rgba(220,38,38,.08); }}
  .test .icon {{ flex-shrink: 0; }}
  .test .name {{ flex: 1; }}
  .test .detail {{ color: #dc2626; font-size: .78rem; font-family: monospace; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🌿 Leaf — Test Suite</h1>
  <p class="sub">Pure-function tests. Open this file in any browser.</p>
  <div id="summary">Running…</div>
  <div id="results"></div>
</div>

<script>
// ثابت‌ها
{CONSTANTS}

// توابع استخراج‌شده از index.html
{chr(10).join(extracted)}

// تست‌ها
{TESTS}
</script>
</body>
</html>
"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[DONE] Wrote {OUT}")
    if missing:
        print(f"[NOTE] Missing functions (skipped): {', '.join(missing)}")


if __name__ == "__main__":
    main()