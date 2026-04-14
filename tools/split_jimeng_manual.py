# -*- coding: utf-8 -*-
"""将「单页完整版」即梦AI操作说明.html 拆为目录入口 + 即梦AI操作说明手册/ 下多文件。

再次运行前：请先把根目录的 即梦AI操作说明.html 换回原 3794 行单页文件
（或改本脚本中的 SRC 指向你的备份路径），否则会按已拆分的短首页误切分。
"""
from __future__ import annotations

import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from manual_chapter_nav import chapter_nav_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "即梦AI操作说明.html")
OUT_DIR = os.path.join(ROOT, "即梦AI操作说明手册")
ENTRY = os.path.join(ROOT, "即梦AI操作说明.html")

# (文件名, 页面标题, 起始行, 结束行) — 行号与编辑器一致，1-based，闭区间
CHAPTERS: list[tuple[str, str, int, int]] = [
    ("ch01-平台简介.html", "第一章：即梦AI平台简介", 1040, 1116),
    ("ch02-快速上手.html", "第二章：快速上手", 1117, 1220),
    ("ch03-AI生图.html", "第三章：AI 生图功能-Seedream", 1221, 1584),
    ("ch04-AI视频.html", "第四章：AI视频生成全解", 1585, 1798),
    ("ch05-Agent.html", "第五章：Agent 模式", 1799, 1887),
    ("ch06-动作模仿.html", "第六章：动作模仿 — DreamActor", 1888, 1978),
    ("ch07-配音生成.html", "第七章：配音生成", 1979, 2092),
    ("ch08-数字人.html", "第八章：AI 数字人 — OmniHuman", 2093, 2221),
    ("ch09-智能画布.html", "第九章：智能画布-Canva", 2222, 2260),
    ("ch10-提示词与实战.html", "第十章：提示词 · 运镜与实战", 2261, 3036),
    ("ch11-字体设计.html", "第十一章：字体设计", 3037, 3218),
    ("ch12-信息引用.html", "第十二章：信息引用（含学习资源与附录）", 3219, 3559),
]


def fix_image_paths(html: str) -> str:
    return html.replace('src="image/', 'src="../image/')


FOOTER_LIGHTBOX = """
<!-- ===== FOOTER ===== -->
<div class="footer">
  <p>即梦AI操作说明手册 · 基于 Seedream 5.0 Lite &amp; Seedance 2.0 · 整理于 2026年4月13日</p>
  <p style="margin-top:6px">本手册总结资料来源于互联网，相关版权归原作者</p>
<footer>
  © 2026 runsheep0613保留所有权利。未经许可，禁止复制、转载或用于商业用途。
  <a href="../terms.html">使用条款</a> | <a href="../privacy.html">隐私政策</a>
</footer>
</div>

<!-- ===== IMAGE PREVIEW (LIGHTBOX) ===== -->
<div class="img-preview-backdrop" id="imgPreviewBackdrop" aria-hidden="true">
  <div class="img-preview-dialog" role="dialog" aria-modal="true" aria-label="图片预览">
    <div class="img-preview-toolbar">
      <div class="img-preview-title" id="imgPreviewTitle">图片预览</div>
      <button class="img-preview-close" type="button" id="imgPreviewClose" aria-label="关闭预览">关闭</button>
    </div>
    <div class="img-preview-body">
      <img class="img-preview-img" id="imgPreviewImg" alt="">
    </div>
  </div>
</div>
"""

def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(SRC, encoding="utf-8") as f:
        lines = f.readlines()

    # --- CSS ---
    css_lines = lines[7:979]  # 行 8-979（:root 到 img-preview-img 规则末）
    css_text = "".join(css_lines).rstrip() + "\n"
    css_path = os.path.join(OUT_DIR, "common.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_text)

    # --- JS：导航高亮仅在总目录页执行 ---
    script_block = "".join(lines[3586:3789])  # 文件第 3587–3789 行为 JS（不含 <script> 标签）
    script_block = script_block.replace(
        "  /* === 顶部导航：随滚动高亮当前章节 === */\n  (function () {",
        "  /* === 顶部导航：随滚动高亮当前章节（拆分后目录页无各章锚点，跳过） === */\n  (function () {\n"
        "    if (document.body && document.body.id === 'manual-home') return;\n",
        1,
    )
    js_path = os.path.join(OUT_DIR, "common.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(script_block.strip() + "\n")

    # --- 各章节页 ---
    base_href = "即梦AI操作说明手册/"
    for idx, (fname, title, a, b) in enumerate(CHAPTERS):
        chunk = "".join(lines[a - 1 : b])
        chunk = fix_image_paths(chunk)
        body = (
            chapter_nav_html(fname)
            + '<div class="container">\n'
            + chunk
            + "\n</div>\n"
            + FOOTER_LIGHTBOX
        )
        page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | 即梦 AI 操作说明</title>
  <link rel="stylesheet" href="common.css" />
</head>
<body class="manual-chapter">
{body}
<script src="common.js"></script>
</body>
</html>
"""
        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)

    # --- 入口页：即梦AI操作说明.html ---
    toc_items = []
    for idx, (fname, title, _, _) in enumerate(CHAPTERS):
        short = title.split("：", 1)[-1] if "：" in title else title
        toc_items.append(
            f'      <a href="{base_href}{fname}" class="toc-item"><span class="toc-num">{idx + 1}</span>{short}</a>'
        )
    toc_html = "\n".join(toc_items)

    nav_items = [
        ("目录", "即梦AI操作说明.html#s0"),
        ("平台简介", f"{base_href}ch01-平台简介.html"),
        ("快速上手", f"{base_href}ch02-快速上手.html"),
        ("AI生图", f"{base_href}ch03-AI生图.html"),
        ("AI视频", f"{base_href}ch04-AI视频.html"),
        ("Agent", f"{base_href}ch05-Agent.html"),
        ("动作模仿", f"{base_href}ch06-动作模仿.html"),
        ("配音生成", f"{base_href}ch07-配音生成.html"),
        ("数字人", f"{base_href}ch08-数字人.html"),
        ("智能画布", f"{base_href}ch09-智能画布.html"),
        ("提示词", f"{base_href}ch10-提示词与实战.html"),
        ("字体设计", f"{base_href}ch11-字体设计.html"),
        ("信息引用", f"{base_href}ch12-信息引用.html"),
    ]
    nav_lis = "\n".join(f'    <li><a href="{href}">{label}</a></li>' for label, href in nav_items)

    hero_and_nav = "".join(lines[983:998])  # 984-998：hero 与 <nav>…<div class="nav-inner">（不含旧 <ul>）
    # 重写 nav 内 ul
    entry_body = (
        hero_and_nav
        + "\n  <ul>\n"
        + nav_lis
        + "\n  </ul>\n  </div>\n</nav>\n\n<div class=\"container\">\n\n  <!-- ===== TOC ===== -->\n"
        + '  <div class="toc" id="s0">\n'
        + "    <h2>📚 手册目录</h2>\n"
        + '    <p style="color:var(--text-light);font-size:14px;margin:-8px 0 16px;line-height:1.6;">'
        + "以下为拆分章节，点击进入阅读（单页过长已拆分为多文件，样式与交互与原手册一致）。</p>\n"
        + '    <div class="toc-list">\n'
        + toc_html
        + "\n"
        + "    </div>\n  </div>\n\n</div>\n"
        + FOOTER_LIGHTBOX.replace("../terms.html", "terms.html").replace("../privacy.html", "privacy.html")
    )

    entry_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>即梦 AI 操作说明</title>
  <link rel="stylesheet" href="{base_href}common.css" />
</head>
<body id="manual-home">
{entry_body}
<script src="{base_href}common.js"></script>
</body>
</html>
"""
    with open(ENTRY, "w", encoding="utf-8") as f:
        f.write(entry_html)

    print("Written:", css_path, js_path, ENTRY)
    for fname, _, _, _ in CHAPTERS:
        print(" ", os.path.join(OUT_DIR, fname))


if __name__ == "__main__":
    main()
