---
name: jimeng-modular-refactor
overview: 将 3787 行的单文件 HTML 重构为模块化多文件结构：CSS/JS 分离 + 章节片段按需加载
---

## 用户需求（2026-04-13 更新）

1. **模块化重构**：将单 HTML 文件（3805行）拆分为 CSS/JS/Sections 分离结构
2. **整理第十二章顺序**：官方文档 → 图片参考链接 → 视频模型链接 → 提示词公式汇总
3. **整理文件夹**：清理零散文件，建立清晰目录结构

## 当前项目状态

- 主文件：`即梦AI操作说明.html`（3805 行）
- 当前文件夹零散：`index.html`、`push-to-github.bat`、大量图片在根目录

## 章节结构（12章 + 2附录）

| ID | 章节名称 | 起始行 |
| --- | --- | --- |
| s0 | 目录 | 1011 |
| s1 | 平台简介 | 1033 |
| s2 | 快速上手 | 1110 |
| s3 | AI生图-Seedream | 1214 |
| s4 | AI视频生成 | 1578 |
| s5 | Agent模式 | 1792 |
| s6 | 动作模仿-DreamActor | 1881 |
| s7 | 配音生成 | 1972 |
| s8 | AI数字人-OmniHuman | 2086 |
| s9 | 智能画布-Canva | 2215 |
| s10 | 提示词-运镜指南&实战案例 | 2258 |
| s11 | 字体设计 | 3030 |
| s12 | 信息引用（需重排） | 3212 |
| s-links | 教程链接资源 | 3327 |
| s-appendix | 提示词速查表 | 3531 |


## 目标目录结构

```
jimeng-tutorial/
├── index.html              # 主入口（原 index.html）
├── css/
│   └── style.css           # 提取的样式
├── js/
│   └── main.js             # 提取的脚本
├── sections/               # 章节片段
│   ├── s0-toc.html         # 目录
│   ├── s1-platform.html    # 平台简介
│   ├── s2-quickstart.html  # 快速上手
│   ├── s3-image.html       # AI生图
│   ├── s4-video.html       # AI视频
│   ├── s5-agent.html       # Agent模式
│   ├── s6-motion.html      # 动作模仿
│   ├── s7-voice.html       # 配音生成
│   ├── s8-digital.html     # 数字人
│   ├── s9-canvas.html      # 智能画布
│   ├── s10-prompt.html     # 提示词
│   ├── s11-font.html       # 字体设计
│   ├── s12-reference.html  # 信息引用（重排后）
│   ├── s-links.html        # 教程链接
│   └── s-appendix.html     # 提示词速查
├── image/                  # 图片资源
│   └── 1~12/              # 按章节分类
├── docs/                   # [NEW] 文档目录
│   ├── 官方文档/          # 飞书官方手册
│   └── 教程资源/          # 外部链接整理
└── scripts/               # [NEW] 自动化脚本
    └── push-to-github.bat # 推送脚本
```

## 实施步骤

### 步骤1：整理文件夹结构

- 创建 `css/`、`js/`、`sections/`、`docs/`、`scripts/` 目录
- 移动 `push-to-github.bat` → `scripts/`

### 步骤2：整理第十二章内容顺序

**当前顺序**：官方账号 → 官方知识库 → 视频教程 → 图片教程 → 公式汇总
**目标顺序**：官方文档 → 图片教程 → 视频教程 → 公式汇总

### 步骤3：CSS/JS 提取

- 从 HTML 提取 `<style>` → `css/style.css`
- 从 HTML 提取 `<script>` → `js/main.js`
- 更新 HTML 引入外部文件

### 步骤4：章节拆分

- 将 14 个区块拆分为独立 HTML 文件
- 每个 section 文件只含内容，引入全局 CSS/JS

### 步骤5：创建主入口

- 精简 `index.html`，保留头部/导航/容器
- 通过 fetch 按需加载 sections/*.html

## 产品概述

即梦AI操作说明手册是一个静态教程页面，包含13个章节（平台简介、快速上手、AI生图、AI视频、Agent模式等），图片资源按章节组织在image/目录下。

## 核心功能

- 单页应用导航（锚点跳转）
- 图片预览灯箱功能
- 横向轮播卡片展示
- 响应式布局设计

## 技术栈

- 纯 HTML/CSS/JavaScript（无框架依赖）
- CSS3 + Flexbox 布局
- Vanilla JavaScript（轮播、灯箱控制）
- fetch API（章节动态加载）

## 目录结构

```
jimeng-tutorial/
├── index.html              # [NEW] 主入口文件（精简版）
├── css/
│   └── style.css           # [NEW] 提取所有样式
├── js/
│   └── main.js             # [NEW] 提取所有脚本
├── sections/               # [NEW] 章节片段
│   ├── toc.html            # 目录 (s0)
│   ├── s1-platform.html    # 平台简介
│   ├── s2-quickstart.html  # 快速上手
│   ├── s3-image.html       # AI生图
│   ├── s4-video.html       # AI视频
│   ├── s5-agent.html       # Agent模式
│   ├── s6-motion.html      # 动作模仿
│   ├── s7-audio.html       # 配音生成
│   ├── s8-digital.html     # 数字人
│   ├── s9-canvas.html      # 智能画布
│   ├── s10-prompt.html     # 提示词
│   ├── s11-font.html       # 字体设计
│   └── s12-reference.html  # 信息引用
└── image/                  # [保留] 现有图片目录
```

## 实施策略

### 1. CSS 提取

- 提取 `