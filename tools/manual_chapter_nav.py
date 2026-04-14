# -*- coding: utf-8 -*-
"""章节子页顶栏：与首页一致的 nav.nav（便于跨页跳转）。"""

# (显示文案, 同目录下的章节文件名；None 表示返回总目录)
MANUAL_NAV: list[tuple[str, str | None]] = [
    ("目录", None),
    ("平台简介", "ch01-平台简介.html"),
    ("快速上手", "ch02-快速上手.html"),
    ("AI生图", "ch03-AI生图.html"),
    ("AI视频", "ch04-AI视频.html"),
    ("Agent", "ch05-Agent.html"),
    ("动作模仿", "ch06-动作模仿.html"),
    ("配音生成", "ch07-配音生成.html"),
    ("数字人", "ch08-数字人.html"),
    ("智能画布", "ch09-智能画布.html"),
    ("提示词", "ch10-提示词与实战.html"),
    ("字体设计", "ch11-字体设计.html"),
    ("信息引用", "ch12-信息引用.html"),
]


def chapter_nav_html(active_chapter_file: str) -> str:
    """生成放在 body 下、container 上的 <nav class="nav">；当前章节 a 带 nav-link--active。"""
    lines = [
        "<!-- ===== NAV ===== -->",
        '<nav class="nav">',
        '  <div class="nav-inner">',
        "  <ul>",
    ]
    for label, fn in MANUAL_NAV:
        if fn is None:
            href = "../即梦AI操作说明.html#s0"
        else:
            href = fn
        active_attr = ' class="nav-link--active"' if fn == active_chapter_file else ""
        lines.append(f'    <li><a href="{href}"{active_attr}>{label}</a></li>')
    lines.extend(["  </ul>", "  </div>", "</nav>", ""])
    return "\n".join(lines)
