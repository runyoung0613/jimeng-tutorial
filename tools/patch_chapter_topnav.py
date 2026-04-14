# -*- coding: utf-8 -*-
"""将已生成的章节页顶部的 manual-chapter-bar 换成与首页一致的 nav.nav。"""
from __future__ import annotations

import os
import re
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from manual_chapter_nav import MANUAL_NAV, chapter_nav_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "即梦AI操作说明手册")

PAT = re.compile(
    r"<body class=\"manual-chapter\">\s*<div class=\"manual-chapter-bar\">[\s\S]*?</div>\s*\n",
    re.MULTILINE,
)


def main() -> None:
    for _label, fn in MANUAL_NAV:
        if fn is None:
            continue
        path = os.path.join(OUT_DIR, fn)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        nav = chapter_nav_html(fn)
        new_text, n = PAT.subn(f'<body class="manual-chapter">\n{nav}\n', text, count=1)
        if n != 1:
            raise SystemExit(f"未匹配到旧顶栏，跳过或已改写过: {fn} (n={n})")
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("patched", fn)


if __name__ == "__main__":
    main()
