# -*- coding: utf-8 -*-
import sys, os
import re
import glob

SRC = os.path.join("src", "index.html")
CSS_OUT = os.path.join("src", "styles.css")

def main():
    # 1. پیدا کردن آخرین بکاپ index.html که قبل از جدا کردن CSS گرفته شده
    backups = sorted(glob.glob(os.path.join("src", "index.html.splitcss-*.bak")))
    if not backups:
        print("[ABORT] No splitcss backup found. Cannot restore CSS.")
        sys.exit(2)
    
    latest_backup = backups[-1]
    print(f"[INFO] Using backup: {latest_backup}")

    # 2. خواندن محتوای بکاپ
    with open(latest_backup, "r", encoding="utf-8") as f:
        backup_text = f.read()

    # 3. استخراج بلوک CSS از بکاپ
    pattern = re.compile(r"<style>\s*(.*?)\s*</style>", re.DOTALL)
    matches = pattern.findall(backup_text)
    if len(matches) != 1:
        print(f"[ABORT] Expected exactly 1 <style> block in backup, found {len(matches)}.")
        sys.exit(2)

    css_content = matches[0]
    print(f"[INFO] Extracted {len(css_content)} chars of CSS from backup")

    # 4. نوشتن کل CSS توی styles.css (جایگزینی کامل)
    with open(CSS_OUT, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"[OK] Overwrote {CSS_OUT} with the original CSS from backup")

    print("[DONE] Original CSS completely restored.")

if __name__ == "__main__":
    main()