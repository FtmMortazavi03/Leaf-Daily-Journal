# -*- coding: utf-8 -*-
"""
Leaf — Split step 1: extract CSS into styles.css
- Finds the <style>...</style> block inside <head>
- Writes its contents to src/styles.css
- Replaces the block with <link rel="stylesheet" href="./styles.css">
- Keeps everything else untouched
"""
import sys, os, shutil, re
from datetime import datetime

SRC = os.path.join("src", "index.html")
CSS_OUT = os.path.join("src", "styles.css")


def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    original_len = len(text)
    print(f"[INFO] Loaded {SRC} ({original_len} chars)")

    # Find <style>...</style> — there should be exactly one in <head>
    pattern = re.compile(r"<style>\s*(.*?)\s*</style>", re.DOTALL)
    matches = pattern.findall(text)
    if len(matches) != 1:
        print(f"[ABORT] Expected exactly 1 <style> block, found {len(matches)}.")
        sys.exit(2)

    css_content = matches[0]
    print(f"[INFO] Extracted CSS: {len(css_content)} chars")

    # Write styles.css
    with open(CSS_OUT, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"[OK] Wrote {CSS_OUT}")

    # Replace <style>...</style> with <link rel="stylesheet">
    new_text = pattern.sub('<link rel="stylesheet" href="./styles.css">', text, count=1)

    # Backup index.html (timestamped)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{SRC}.splitcss-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"[INFO] Backup saved: {backup}")

    # Write index.html
    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print(f"[OK] Wrote {SRC} ({len(new_text)} chars, delta {len(new_text) - original_len})")
    print("[DONE] Step 1 (CSS split) complete.")


if __name__ == "__main__":
    main()