# -*- coding: utf-8 -*-
"""按 manual_chapter_nav.MANUAL_NAV 重写各章节页中的 <nav class="nav"> 块。"""
from __future__ import annotations

import os
import re
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from manual_chapter_nav import MANUAL_NAV, chapter_nav_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "charpter")

NAV_PAT = re.compile(r"<!-- ===== NAV ===== -->[\s\S]*?</nav>\s*\n", re.MULTILINE)


def main() -> None:
    for _label, fn in MANUAL_NAV:
        if fn is None:
            continue
        path = os.path.join(OUT_DIR, fn)
        if not os.path.isfile(path):
            print("skip missing", fn)
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        nav = chapter_nav_html(fn)
        new_text, n = NAV_PAT.subn(nav + "\n", text, count=1)
        if n != 1:
            raise SystemExit(f"nav 替换失败: {fn} (n={n})")
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("nav ok", fn)


if __name__ == "__main__":
    main()
