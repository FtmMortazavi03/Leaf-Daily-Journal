# -*- coding: utf-8 -*-
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

SW_SNIPPET = """<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js').catch(() => {});
  });
}
</script>
"""

SW_COMMENTED = """<!-- SW disabled for dev — run enable_sw.py to restore -->
<script>
// if ('serviceWorker' in navigator) {
//   window.addEventListener('load', () => {
//     navigator.serviceWorker.register('./service-worker.js').catch(() => {});
//   });
// }
</script>
"""


def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    if SW_COMMENTED in text:
        print("[SKIP] SW already disabled.")
        sys.exit(0)

    if SW_SNIPPET not in text:
        print("[ABORT] SW snippet not found. Nothing changed.")
        sys.exit(2)

    text = text.replace(SW_SNIPPET, SW_COMMENTED, 1)
    print("[OK] SW disabled")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{SRC}.disablesw-{stamp}.bak"
    shutil.copy2(SRC, backup)
    print(f"[INFO] Backup: {backup}")

    with open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"[INFO] Wrote {SRC}")
    print("[NEXT] In browser: F12 -> Application -> Service workers -> Unregister")
    print("[NEXT] Then Ctrl+Shift+R")


if __name__ == "__main__":
    main()