---
name: tomabc-deck
description: 'TomABC 视频幻灯片标准化模板。用于 T Agent 开发纪实 vlog 系列 / 论文精读系列 / AI 每日简报播报系列 / 专题调查系列的视频幻灯片制作（1920×1080 全屏、固定 16 步标准结构、6 Phase 管线：研究→gen_deck.py 幻灯片→narrations.json 口播稿→本地 Qwen3-TTS 音频→静帧画面采集→飞书发布）。内置六种模板，**视频生成默认用 dbs（DBS 毛玻璃风，templates/dbs/）**：默认 TomABC 品牌暖白风 + hand-draw2 doodle 手绘风（templates/hand-draw2/，EP59 实战样式）+ notebook 学霸笔记本手写纸风（templates/notebook/，学习/论文精读内容）+ news 演播室电视风（templates/news/，2026-09 起退为备选）+ dbs DBS 毛玻璃风（templates/dbs/，粉紫渐变底 + 半透明白玻璃卡 + DBS 红点缀，克制杂志感）+ tomabc TomABC 毛玻璃风（templates/tomabc/，与 dbs 逐像素同源，换 TomABC 红 #C8161D 与像素猫 logo，对外科普/品牌向内容用）。当用户要做视频幻灯片、论文精读/学习笔记视频、每日简报/新闻播报视频、专题调查视频、T Agent vlog 分镜、EP 幻灯片，或提到 tomabc-deck、hand-draw2、doodle 手绘风、notebook 模板、学霸笔记风、news 模板、演播室风、dbs 模板、tomabc 模板、毛玻璃风/玻璃拟态时使用。'
metadata:
  version: 3.2.0
---

# TomABC Deck — 视频幻灯片标准化模板

> 用于 T Agent 开发纪实 vlog 系列的视频幻灯片制作。
> 风格：1920×1080 全屏幻灯片，代码走读 + 问题驱动叙事。
> 本文档以 2026-08 最新产线（EP53 / EP54 深度思考课、EP59 DSH 拆解）为基准校准；旧版 12 步 / edge-tts / tomabc-engine 网站发布流程已废弃。

---

## 模板系统

技能内置五种模板，按内容气质选用：

| 模板 | 位置 | 视觉 | 适用场景 | 来源 |
|------|------|------|----------|------|
| **默认（品牌暖白风）** | 本文件下面这套 | 暖白 `#F4F2EC` + 品牌红 + 深色封面 | 品牌系 / 深度思考课 | EP53/54 |
| **hand-draw2（doodle 手绘风）** | `templates/hand-draw2/` | 纯白底 + 墨蓝描边 + 手绘卡片 + ZCOOL 标题字体 | 拆解 / 手绘风内容 | EP59 实战样式 |
| **notebook（学霸笔记本手写纸风）** | `templates/notebook/` | 米黄横线纸 + 孔环装订线 + 毛笔 MaShanZheng 标题 + 荧光笔批注 + 便签卡 | 论文精读 / 学习笔记 / 知识讲解 | 与 note-skill Style A 同源（2026-09） |
| **news（演播室电视风）** | `templates/news/` | 深藏青演播室底 + 红白大头条 + 板块色条（行业蓝/安全红/工具绿/观察琥珀）+ 下第三屏快讯条 + 幽灵英文板块页 | **每日简报播报 / 新闻速览视频**（6-7 分钟短播报） | 2026-09 每日简报系列 br01 |
| **dbs（DBS 毛玻璃风）· 视频默认** | `templates/dbs/` | 粉紫渐变底 + 三彩色光斑（blur 90px）+ 半透明白玻璃卡（backdrop-filter）+ **唯一点缀色 DBS 红 `#E50014`** + 顶部玻璃导航（DBS 字标图） | **视频生成默认样式**（2026-09-13 起）：每日简报 br 系列、克制留白 / 杂志感内容；也可给已有期次**同内容换皮**（br04 → br04dbs） | tomabc-html / dbs-html 的 DBS Glass（2026-09） |
| **tomabc（TomABC 毛玻璃风）** | `templates/tomabc/` | **与 dbs 同源、毛玻璃效果逐像素一致**（已用像素差分验证），只有两处不同：点缀色换成 **TomABC 红 `#C8161D`**、顶栏换成 **像素猫 logo**（取自 ai.tomabc.com） | 想用毛玻璃那套观感、但**该署 TomABC 自己名**的片子：对外科普 / 讲解 / 品牌向内容 | dbs 模板的 TomABC 品牌版（2026-09-13） |

**选模板**：**默认走 dbs（DBS 毛玻璃风）**——2026-09-13 起它是**视频生成的默认样式**，每日简报 br 系列与多数单集直接用它。**要毛玻璃那套观感、但该署 TomABC 自己名（对外科普 / 讲解 / 品牌向）就走 tomabc**——它与 dbs 同源、毛玻璃逐像素一致，只换点缀色与 logo。品牌系内容可回默认模板（本文件主体）；拆解、想用手绘纸面感的用 hand-draw2；**论文精读 / 学习笔记类内容用 notebook**（与学霸笔记 HTML 同一视觉语言）。**news（演播室电视风）自 2026-09-13 起退为备选**，只在明确要「演播室／电视新闻」气质时才选（br01–br05 用的是它）。news / dbs / tomabc 的**组件 class 完全同名**，三套模板的 slides 可整体平移、只换 CSS 与壳。各模板完整用法见 [Phase 2](#phase-2--幻灯片gen_deckpy约-20-min) 对应小节，色板 / 字体 / class 清单见各模板 `README.md`。

---

## 文件规范

工作区根：`/home/nvidia/workspace/Twork/`（旧 `grok/tomabc-engine/` 已废弃）

```
docs/html/video-{NN}-{topic}.html   ← 幻灯片产出（gen_deck.py 生成）
video/ep{NN}/                        ← 每期工程目录（脚本 + 音频 + 成品）
```

| 部分 | 规则 |
|------|------|
| `NN` | 两位数字：EP01 → `01`，EP05 → `05` |
| `topic` | 英文连字符：隐写术深度思考课 → `steganography` |

---

## 标准结构（16 步）

每期固定 16 步（`gen_deck.py` 会校验 `data-step` 必须是 1..16）。深度思考课叙事节奏为 **概念 → 历史 → 转折 → 案例 → 实测 → 深度思考 ×4 → 防范 → 总结**：

| Step | 类型 | 内容 | 时长参考 |
|:----:|:----|:------|:--------:|
| 1 | **封面** | 深色渐变封面：金色眉题 + 大标题 + 标签 + 底部关键数字 | 36-39s |
| 2 | **概念 / 起点** | 区分核心概念（三卡片 + issue 结论，如 加密/水印/隐写） | ~35s |
| 3 | **形式全景** | 分类 grid（载体大类，标注最危险方向） | ~36s |
| 4 | **历史** | 时间线（三十年老手艺 + 实战常态化） | ~38s |
| 5 | **转折** | AI 带来的新武器（三卡片 + 叠加 issue） | ~38s |
| 6 | **核心案例** | 攻击链 flow（五步 + 指令原文） | ~40s |
| 7 | **实测数据** | 对比卡片 + 转折点结论 | ~38s |
| 8 | **深度思考 ①** | 第一层洞察（三卡片 + 验收标准） | ~38s |
| 9 | **研究线 / 延伸** | 相关研究时间线（一年比一年凶） | ~40s |
| 10 | **最前沿** | 前沿技术深挖（三卡片 + 状态） | ~37s |
| 11 | **隐患 / 信道** | 结构性失效或隐蔽信道（三卡片 + 实测） | ~36s |
| 12 | **深度思考 ②** | 第二层洞察（两卡片 + 结论） | ~38s |
| 13 | **深度思考 ③** | 第三层洞察（三卡片 + 不对称 issue） | ~36s |
| 14 | **深度思考 ④** | 第四层洞察（三卡片 + 推论） | ~37s |
| 15 | **防范 / 行动** | 防范三件套（三卡片 + 原则） | ~38s |
| 16 | **总结** | 深色渐变收尾：结论大标题 + 三要点 + 下期预告 | ~39s |

总时长 ≈ 9.5-10.5 分钟（16 步 × 35-40s）。

> 步数由 `narrations.json` 驱动：`capture_stills.cjs` 自动从 narrations 推导步数与每步时长，JS 导航自动统计 `.slide` 数量（deck 步数少于口播稿段数会直接报错）。若做 12 步短版（EP52 及以前），需同步修改 narrations、gen_deck.py 的校验范围与口播节奏。

---

## HTML 模板框架

> 下面这套是**默认（品牌暖白风）**模板。要用手绘风的话别从这里改——直接走 `templates/hand-draw2/`（见 Phase 2）。

**不要从零写**：复制上一期 / 最近一期最接近的 deck HTML 作模板（品牌顶栏、导航、CSS、JS 全部复用，只换标题与内容）。EP53/EP54 均从 `video-45-ds4-pricing.html` 复制而来。

```html
<!DOCTYPE html>
<!--
═══════════════════════════════════════════════════════════════════════════════
  EP{NN} · {标题}
═══════════════════════════════════════════════════════════════════════════════
  用法：
    1. 复制本文件 → 重命名为 video-<期号>-<主题>.html
    2. 修改 <title>、sticky-top 的 page-label、Step 1 封面内容
    3. 按需复制 Step 2 内容页，替换为你的内容
    4. 步数自适应：JS 自动统计 .slide 数量，增删页无需改代码
    5. 采集：Playwright 打开本文件，ffprobe 音频时长 + 段间 GAP 推进 nextStep()，逐点定格入场动画
-->
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920,initial-scale=0.5">
  <title>EP{NN} {标题} — TomABC</title>
  <style>
    /* ── TomABC 品牌变量（不要改动）── */
    :root {
      --ground: #F4F2EC;      /* 暖白背景 */
      --surface: #FFF;         /* 卡片白 */
      --ink: #2A2A28;          /* 墨黑文字 */
      --ink-soft: #5C5B56;     /* 柔和文字 */
      --ink-quiet: #8A8984;    /* 浅灰 */
      --hairline: #D9D6CD;     /* 分割线 */
      --red: #C8161D;          /* 品牌红 */
      --code-bg: #EDEAE0;      /* 代码背景 */
      --font: system-ui,...;   /* 系统字体栈 */
      --mono: 'SF Mono',...;   /* 等宽字体栈 */
    }
    /* ── 标准布局（不要改动）── */
    * { margin:0; padding:0; box-sizing:border-box; }
    html,body { width:1920px; height:1080px; overflow:hidden; }
    body { background:var(--ground); color:var(--ink); font:28px/1.8 var(--font); }
    .slide { display:none; width:1920px; height:1080px; padding:60px 80px; position:relative; }
    .slide.active { display:flex; flex-direction:column; justify-content:center; }
    /* ── 导航栏（不要改动）── */
    .nav { position:fixed; bottom:32px; left:50%; transform:translateX(-50%);
           display:flex; gap:20px; align-items:center; z-index:100;
           background:var(--ground); padding:8px 24px; border:1px solid var(--hairline); }
    .nav button { background:var(--ink); color:#fff; border:none;
                  padding:10px 24px; font:18px var(--font); cursor:pointer; }
    .nav button:hover { background:var(--red); }
    .nav button:disabled { opacity:.3; }
    .nav .step-indicator { font-size:16px; color:var(--ink-quiet); min-width:80px; text-align:center; }
    /* ── 品牌顶栏（不要改动）── */
    .sticky-top { position:fixed; top:0; left:0; right:0; z-index:99;
                  background:var(--ground); border-bottom:1px solid var(--hairline);
                  padding:16px 36px; display:flex; align-items:center; gap:16px; }
    .sticky-top .logo { display:flex; align-items:center; gap:14px; text-decoration:none; color:inherit; }
    .sticky-top .logo-top { font-size:36px; line-height:1.2; }
    .sticky-top .logo-sub { font-size:20px; letter-spacing:0.18em; color:var(--ink-quiet); }
    .sticky-top .page-label { margin-left:auto; font-size:22px; color:var(--ink-quiet); }
    /* ── 内容组件（按需使用）── */
    .kicker { font-family:var(--mono); font-size:20px; letter-spacing:0.2em;
              text-transform:uppercase; color:var(--ink-quiet);
              display:flex; align-items:center; gap:10px; margin-bottom:8px; }
    .kicker::before { content:""; width:12px; height:12px; background:var(--red); }
    h1 { font-size:56px; font-weight:700; line-height:1.2; margin-bottom:16px; letter-spacing:-0.02em; }
    h2 { font-size:42px; font-weight:600; margin-bottom:20px; }
    p { font-size:24px; color:var(--ink-soft); line-height:1.9; margin-bottom:14px; }
    .card { background:var(--surface); padding:24px 28px; border:1px solid var(--hairline); margin:10px 0; font-size:20px; }
    .card .num { font-size:36px; font-weight:700; color:var(--red); }
    .grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin:14px 0; }
    .grid-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin:12px 0; }
    .grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:16px 0; }
    .flow { display:flex; align-items:center; gap:12px; margin:16px 0; flex-wrap:wrap; }
    .flow-box { background:var(--ink); color:#fff; padding:10px 18px; font-size:18px; font-weight:500; }
    pre { background:var(--code-bg); padding:18px 24px; font-family:var(--mono);
          font-size:17px; line-height:1.6; border:1px solid var(--hairline); margin:10px 0; overflow-x:auto; }
    .tag { display:inline-block; font-size:14px; padding:3px 12px; margin:2px; border:1px solid var(--hairline); }
    .tag-red { border-color:var(--red); color:var(--red); }
    .issue { background:#FFF3E0; border-left:4px solid #FF9800; padding:12px 16px; margin:8px 0; font-size:20px; }
    .issue .id { font-weight:600; color:#E65100; }
    .timeline { position:relative; padding-left:28px; margin:14px 0; }
    .timeline::before { content:''; position:absolute; left:8px; top:0; bottom:0; width:1px; background:var(--hairline); }
    .timeline-item { position:relative; margin-bottom:12px; padding-left:16px; font-size:20px; }
    .timeline-item::before { content:''; position:absolute; left:-22px; top:12px; width:8px; height:8px; background:var(--red); }
  </style>
</head>
<body>
  <!-- stikcy-top: TomABC 猫头 SVG + 品牌文字 + 页码 -->
  <!-- nav: ← → 按钮 + step 指示器 -->
  <!-- 16 个 slide，data-step="1" ~ data-step="16" -->
  <!-- 底部 JS 导航脚本（步数自适应） -->
</body>
</html>
```

---

## 品牌顶栏（每页固定）

```html
<div class="sticky-top">
  <a class="logo" href="https://tomabc.com">
    <svg viewBox="0 0 36 36" width="80" height="80" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
      <rect width="36" height="36" fill="#F4F2EC"/>
      <g shape-rendering="crispEdges">
        <polygon points="6,10 10,2 14,10" fill="#C8161D"/>
        <polygon points="22,10 26,2 30,10" fill="#C8161D"/>
        <rect x="4" y="10" width="28" height="18" rx="3" fill="#2A2A28"/>
        <circle cx="13" cy="18" r="3" fill="#F4F2EC"/>
        <circle cx="23" cy="18" r="3" fill="#F4F2EC"/>
        <circle cx="13" cy="18" r="1.5" fill="#2A2A28"/>
        <circle cx="23" cy="18" r="1.5" fill="#2A2A28"/>
        <polygon points="18,22 16,24 20,24" fill="#C8161D"/>
        <path d="M14 27 Q18 30 22 27" stroke="#F4F2EC" stroke-width="1.2" fill="none" stroke-linecap="round"/>
      </g>
    </svg>
    <div>
      <div class="logo-top"><span style="font-weight:500">Tom</span><span style="font-weight:600;color:var(--red)">ABC</span></div>
      <div class="logo-sub">Always Be Curious</div>
    </div>
  </a>
  <div class="page-label">T Agent 开发纪实 · {系列名}</div>
</div>
```

## 导航控件（每页固定）

```html
<div class="nav">
  <button id="prevBtn" onclick="prevStep()">&larr;</button>
  <span class="step-indicator" id="stepIndicator"></span>
  <button id="nextBtn" onclick="nextStep()">&rarr;</button>
</div>
```

## JS 导航脚本（每页固定，步数自适应）

```html
<script>
  // 步数自适应：增删 .slide 无需改这里
  var step = 1, total = document.querySelectorAll('.slide').length;
  function update() {
    document.querySelectorAll('.slide').forEach(function(s){s.classList.remove('active');});
    document.querySelector('.slide[data-step="'+step+'"]').classList.add('active');
    document.getElementById('stepIndicator').textContent = step+'/'+total;
    document.getElementById('prevBtn').disabled = step===1;
    document.getElementById('nextBtn').disabled = step===total;
  }
  function nextStep(){if(step<total){step++;update()}}
  function prevStep(){if(step>1){step--;update()}}
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();nextStep()}
    if(e.key==='ArrowLeft'){e.preventDefault();prevStep()}
  });
  update();
</script>
```

---

## 封面风格（EP30 同款，深色渐变）

Step 1 封面与 Step 16 总结页用深色底（区别于暖白内容页），要素：

- 深色渐变背景：`linear-gradient(140deg,#1C1B19 0%,#2A2A28 55%,#12314A 100%)`（暖色调收尾可用 `#3A1D12`）
- 金色眉题：`#F2C14E, letter-spacing:.3em`（如 "T AGENT 开发纪实 · 深度思考课"）
- 大标题：68px `#F4F2EC`，可用 `<br>` 换行
- 副题段：26px `#CFCCC4`
- 标签行：`tag-row` + 首标签金色描边，其余红/灰
- 底部数字行：44px 金色数字 + 20px `#CFCCC4` 说明，`flex gap:60px`

---

## 内容写作规范（vlog 风格）

### 每期叙事弧线（深度思考课式）

```
"上一期我们做了 X。这期把一个问题讲透：
概念先分清 → 这不是新敌人（历史）→ 为什么现在危险（转折）→
真实案例 → 实测数据 → 四个深度思考 → 防范三件套 → 总结 + 下期预告。"
```

### 口播规则（narrations.json）

- 每步 35-40s，文本 140-160 字（~4 字/秒）
- **数字读全称**：「百分之七十三」而非「73%」
- 技术词口语化：「点 env 文件」而非「.env 文件」
- 每步以承上启下开头（"先分清三个概念。" / "问题来了：…"）

### 代码引用规则

- 只展示**关键代码片段**（5-20 行），完整文件在 GitHub
- 不需要展示的代码用 `…` 省略
- 错误示例用 `// 修复前：` 标注
- 修复后示例用 `// 修复后：` 标注

### 问题记录规则

```html
<div class="issue">
  <span class="id">关键:</span> 一句话结论
</div>
```

### 验证数据规则

```html
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">
  <div style="background:var(--surface);padding:20px;border:1px solid var(--hairline);text-align:center">
    <div style="font-size:48px;font-weight:700;color:var(--red)">{数字}</div>
    <div style="font-size:16px;color:var(--ink-quiet)">{说明}</div>
  </div>
</div>
```

---

## 完整管线（6 Phase，文件级落地）

每期 EP 在 `docs/html/` 和 `video/ep{NN}/` 两个目录下产生结构化文件：

```
docs/html/video-{NN}-{topic}.html    ← Phase 2 产出：幻灯片
video/ep{NN}/
├── gen_deck.py                       ← Phase 2 脚本：模板复用 + 生成幻灯片
├── narrations.json                   ← Phase 3 产出：口播稿（16 步）
├── tts_batch.py                      ← Phase 4 脚本：本地 TTS 合成
├── audio/                            ← Phase 4 产出：音频
│   ├── 1.wav … 16.wav               ← 逐步音频（24kHz PCM_16）
│   └── full.wav                      ← 拼接音频（段间 0.4s 静音）
├── build.sh                          ← Phase 5 入口：转发到 br-cron/build.sh
├── output/
│   ├── frames/ + frames.txt          ← Phase 5 中间产物：无损静帧 + concat 清单（出片后自动清理）
│   ├── raw.webm                      ← 仅回退录屏路径才有
│   └── video-{NN}-final.mp4          ← Phase 5 产出：成品视频
└── （发布无脚本）                    ← Phase 6：走 feishu-send CLI
```

---

## Phase 0 — 项目初始化

```bash
mkdir -p video/ep{NN}/audio video/ep{NN}/output
```

---

## Phase 1 — 内容研究

- 阅读对应章节源码 / 调研材料（论文、报告、实测数据）
- 产出本期叙事主线（16 步对应内容），直接落到 `narrations.json` 文本
- 不强制生成 `research.md`（EP53/54 目录无此文件）

---

## Phase 2 — 幻灯片（gen_deck.py，约 20 min）

按模板分两条路：

### 默认模板（品牌暖白风）

**模板复用**：把上一期 / 最近一期最接近的 deck 复制为模板，只换标题与 slides 块，品牌系统零改动。

在 `video/ep{NN}/` 写 `gen_deck.py`（参考 `video/ep54/gen_deck.py`），改动 4 处：

```python
SRC = "/home/nvidia/workspace/Twork/docs/html/video-{NN-1}-{topic}.html"
DST = "/home/nvidia/workspace/Twork/docs/html/video-{NN}-{topic}.html"

html = open(SRC, encoding="utf-8").read()
# 1. <title>
html = html.replace("<title>EP{NN-1} …</title>", "<title>EP{NN} {标题} — TomABC</title>")
# 2. header 大标题行（可选）
html = html.replace("  EP{NN-1} · …", "  EP{NN} · …")
# 3. sticky-top 的 page-label
html = html.replace('<div class="page-label">…</div>', '<div class="page-label">T Agent 开发纪实 · {系列名}</div>')
```

然后整块替换 slides：

```python
start = html.index('<div class="slide active" data-step="1"')
end = html.index('<!-- 导航控件 -->')
html = html[:start] + slides + html[end:]

# 4. 校验：必须恰好 16 步
steps = re.findall(r'data-step="(\d+)"', html)
print("steps:", steps)
print("OK" if steps == [str(i) for i in range(1, 17)] else "FAIL")
```

运行：`python3 gen_deck.py` → 打印 `steps: [...]` 与 `OK`。产出 `docs/html/video-{NN}-{topic}.html`。

### hand-draw2 模板（doodle 手绘风）

模板包在技能目录 `templates/hand-draw2/`（shell.html + hand-draw2.css + gen_deck.py + logo.html + 16 步示例 + 字体）。EP59 即该模板产线。

```bash
# 1. 建目录并复制模板（slides 示例复制为正式文件）
mkdir -p video/ep{NN}/audio video/ep{NN}/output
cp -r /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/{gen_deck.py,logo.html,hand-draw2.css,shell.html} video/ep{NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/slides_example_part1.html video/ep{NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/slides_example_part2.html video/ep{NN}/slides_part2.html

# 2. 改 gen_deck.py 顶部常量：SERIES / EP_NN / EP_NAME / TOPIC / DST
# 3. 逐页替换 slides_part1.html（第 1-8 步）/ slides_part2.html（第 9-16 步）的占位内容
# 4. 生成 + 校验（自动复制字体、校验 16 步 + class 检查）
cd video/ep{NN}
python3 gen_deck.py
```

要点：
- `gen_deck.py` 自动把模板 `fonts/`（ZCOOL KuaiLe + Ma Shan Zheng）复制到 `video/ep{NN}/fonts/`，deck 内 `@font-face` 相对路径引用，无需手工处理
- 校验输出三行：`fonts: ...`、`slides: s1 s2 … s16`、`class check: OK`，任何一行异常先修再继续
- 组件 class 速查与色板见 `templates/hand-draw2/README.md`

### notebook 模板（学霸笔记本手写纸风）

模板包在技能目录 `templates/notebook/`（shell.html + notebook.css + gen_deck.py + logo.html + 16 步示例 + 4 个手写字体）。视觉与 note-skill「学霸笔记 Style A」同源（米黄纸 #fdf6e3 + 孔环装订线 + 毛笔 MaShanZheng 标题 + LongCang 手写点缀 + Kalam 数字 + 荧光笔 .mark / 便签卡 .card/.sticker）。2026-09 论文精读系列首用于 pr01（Visual Primitives）。

```bash
# 1. 建目录并复制模板
mkdir -p video/{EP_NN}/audio video/{EP_NN}/output     # EP_NN 见下方期号规则
cp -r /home/nvidia/.claude/skills/tomabc-deck/templates/notebook/{gen_deck.py,logo.html,notebook.css,shell.html} video/{EP_NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/notebook/slides_example_part1.html video/{EP_NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/notebook/slides_example_part2.html video/{EP_NN}/slides_part2.html

# 2. 改 gen_deck.py 顶部常量（SERIES / SERIES_NO / EP_NN / EP_NAME / TOPIC）
# 3. 逐页替换 slides_part1.html（1-8 步）/ slides_part2.html（9-16 步）
# 4. 生成 + 校验
cd video/{EP_NN} && python3 gen_deck.py
```

**notebook 期号规则（双系列）**：`EP_NN = "83"`（全数字）→ 工程目录 `video/ep83/`，字体路径 `…/ep83/fonts/`，与 hand-draw2 一致；`EP_NN = "pr01"`（带前缀系列号）→ 工程目录**就叫** `video/pr01/`，字体路径 `…/pr01/fonts/`。页标展示文案由 `SERIES_NO` 控制（如「第 1 期」）。

要点：
- 每页自动带孔环/装订线装饰（纯 CSS），封面/总结页加 `cover` class 去装饰全幅居中
- 切页逐级 write-in 淡入（.slide.active 自动，无需手写动画 class）
- 校验三行同 hand-draw2：`fonts:`（4 个 TTF）/ `slides: s1…s16` / `class check: OK`
- 组件 class 速查与色板见 `templates/notebook/README.md`

### news 模板（演播室电视风 · 备选）

> **2026-09-13 起退为备选**：每日简报的默认样式已改为 dbs（见上）。news 用于 br01–br05，以及明确要「演播室／电视新闻」气质时。

模板包在技能目录 `templates/news/`（shell.html + news.css + gen_deck.py + logo.html + 16 步示例）。深藏青演播室底 + 红白大头条 + 板块色条（行业蓝 `#5ac8fa` / 安全红 `#ff4d3e` / 工具绿 `#4cd964` / 观察琥珀 `#ffd166`）+ 每页下第三屏快讯条 `.ticker` + 板块转场页幽灵英文。**全用系统黑体 Noto Sans CJK SC——无 fonts/ 目录**，gen_deck.py 已无字体复制步骤。2026-09 AI 每日简报系列首用于 br01；br02 起 step 数随条数浮动（10 条无工具板块 → 14 步）。

```bash
# 1. 建目录并复制模板（news 模板无字体目录）
mkdir -p video/{EP_NN}/audio video/{EP_NN}/output
cp /home/nvidia/.claude/skills/tomabc-deck/templates/news/{gen_deck.py,logo.html,news.css,shell.html} video/{EP_NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/news/slides_example_part1.html video/{EP_NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/news/slides_example_part2.html video/{EP_NN}/slides_part2.html

# 2. 改 gen_deck.py 顶部常量；建议 EP_NN 用 "brNN"（每日简报第 N 期）、EP_NAME 带日期（"09-02 新闻播报"）
# 3. 逐页替换 slides_part1.html / slides_part2.html
# 4. 生成 + 校验（校验两行：slides: s1…s16 / class check: OK）
cd video/{EP_NN} && python3 gen_deck.py
```

**news 期号规则**：与 notebook 同款双规则（全数字 → `video/epNN/`；带前缀如 `"br01"` → 目录就叫 `video/br01/`）。news 无字体引用，目录名无 404 风险，但仍保持一致习惯。

要点：
- 播报脚本由原始新闻**改写总结**（勿照抄原文）：12 条新闻 → 封面 + 快报头条速览页 + 深度页 + 板块转场页 + 今日观察 + 收尾 ≈ 16 步、每步口播 24-26s ≈ 6-7 分钟
- 分类标签用 `safety` / `tools` class 上色（`.chip` / `.flash-row` / `.item` / `.panel .no` 变体）
- .nav 定位 bottom:86px（让出快讯条），.ticker 每页一条静态 chyron 文案
- 组件 class 速查与色板见 `templates/news/README.md`

### dbs 模板（DBS 毛玻璃风）· 视频默认

> **2026-09-13 起，dbs 是视频生成的默认样式**——新建任何视频幻灯片（尤其每日简报 br 系列）默认用它，不必再问「选哪套」。只有内容明确要别的气质时才切走。

模板包在技能目录 `templates/dbs/`（shell.html + dbs-deck.css + gen_deck.py + logo.html + 16 步示例）。设计系统来自 `tomabc-html` / `dbs-html` 的 **DBS Glass**，`dbs-deck.css` 是它的 **1920×1080 定尺改造版**（网页那套是流式布局）。粉紫渐变底 + 三个彩色光斑（`filter:blur(90px)`）+ 半透明白玻璃卡（`backdrop-filter:blur(20px)`）+ **唯一点缀色 DBS 红 `#E50014`**，分类色走低饱和 `--sec-*`（行业 `#3B7DD8` / 安全 `#E50014` / 工具 `#2A8A5A` / 观察 `#D97706`）。顶部是 sticky 玻璃导航，只放完整 DBS logo（64px）。**全用系统黑体 Noto Sans CJK SC——无 fonts/ 目录**。

```bash
# 1. 建目录并复制模板（dbs 模板无字体目录）
mkdir -p video/{EP_NN}/audio video/{EP_NN}/output
cp /home/nvidia/.claude/skills/tomabc-deck/templates/dbs/{gen_deck.py,logo.html,dbs-deck.css,shell.html} video/{EP_NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/dbs/slides_example_part1.html video/{EP_NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/dbs/slides_example_part2.html video/{EP_NN}/slides_part2.html

# 2. 改 gen_deck.py 顶部常量；建议 EP_NN 用 "brNN"（或换皮版 "brNNdbs"）、EP_NAME 带日期
# 3. 逐页替换 slides_part1.html / slides_part2.html（可从 news 版整体平移，class 同名）
# 4. 生成 + 校验（校验三行：slides: s1…s16 / class check: OK，且无 FAIL - CSS）
cd video/{EP_NN} && python3 gen_deck.py
```

**dbs 期号规则**：与 notebook / news 同款双规则（全数字 → `video/epNN/`；带前缀如 `"br01"` → 目录就叫 `video/br01/`）。**同内容换皮**用 `EP_NN = "br04dbs"` → 目录 `video/br04dbs/`，产物 `docs/html/video-br04dbs-daily-brief.html`。换皮时音频可直接复用原期次的 `audio/`（只换视觉，`narrations.json` 不动，时间轴完全一致）。

要点：
- **先跑 QC 再录屏**：光斑 blur + backdrop-filter 渲染比 news 重得多，必须确认不掉帧
- 页面里**不要自己加背景色**——玻璃卡的透视感来自壳里的 `.bg` 层，卡片上盖不透明底色会把玻璃做死；分类标记走 `.chip` / `.flash-row` 的 `sec-*` 变体
- 别沿用 news 的荧光四色（在浅玻璃底上会脏）；板块转场页 `.bar` 用 inline style 给 `--sec-*` 的色值
- `.nav` 定位 `bottom:100px`（让出快讯条）
- **CSS 注释陷阱（真踩过）**：注释正文里出现「星号紧跟斜杠」（如写通配类名）会让注释提前闭合，解析器一路吞到下一个 `{`，把 `:root` 令牌块整块丢掉 → 全站颜色退回黑、玻璃卡全透明，而文件看起来完全正常。`gen_deck.py` 的 `lint_css()` 会在生成前拦住
- 组件 class 速查与色板见 `templates/dbs/README.md`

---

### tomabc 模板（TomABC 毛玻璃风）

> 与 dbs **同源**：`tomabc-deck.css` 是 `dbs-deck.css` 的 TomABC 品牌版，**毛玻璃效果逐像素一致**（粉紫渐变 / 三光斑 / 玻璃卡透明度 / blur 半径 / 动效时长全部原样），只有两处不同。**选它还是选 dbs，只看这段片子该署谁的名。**

| | dbs | tomabc |
|---|---|---|
| 点缀色 | `#E50014`（DBS 红） | **`#C8161D`**（TomABC 红，取自 ai.tomabc.com 的 `--red`） |
| 顶栏 logo | 横向 DBS 字标图（内联 base64 PNG 486×352） | **像素猫 SVG + `Tom`/`ABC` 字标 + `Always Be Curious` 副标**（取自 ai.tomabc.com 顶栏） |

「逐像素一致」不是形容词，是**验过的**：把 dbs 的 CSS 副本只做 `#E50014→#C8161D` 换色，与 tomabc 渲染同 slides 逐像素差分，**正文区 0 像素不同**，仅顶栏 logo 区（约 6000 px）不同。回归方法：

```bash
diff <(sed 's/#C8161D/#E50014/g; s/rgba(200,22,29,/rgba(229,0,20,/g' tomabc-deck.css) ../dbs/dbs-deck.css
# 除装饰性注释外应当无输出
```

```bash
mkdir -p video/{EP_NN}/audio video/{EP_NN}/output
cp /home/nvidia/.claude/skills/tomabc-deck/templates/tomabc/{gen_deck.py,logo.html,tomabc-deck.css,shell.html} video/{EP_NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/tomabc/slides_example_part1.html video/{EP_NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/tomabc/slides_example_part2.html video/{EP_NN}/slides_part2.html
# 改 gen_deck.py 顶部常量 → 逐页替换 slides → 生成
cd video/{EP_NN} && python3 gen_deck.py
```

**tomabc 期号规则**：与 dbs 同款。换皮用 `EP_NN = "br04tomabc"` → 目录 `video/br04tomabc/`。**从 dbs 换到 tomabc（或反向）时，音频与 `narrations.json` 可以完全不动**——视觉换了、时间轴一模一样（已验证逐像素一致，只差 logo）。

要点（与 dbs 完全一致，不再重复）：背景色别自己加、别用 news 荧光四色、先跑 QC 再录屏、`.nav` 在 `bottom:100px`、CSS 注释陷阱。**顶栏 92px 高**（不是 64px——64px 是 dbs 那张 logo 图的 `img` 高度；tomabc 是 56px 猫 + 两行字标，需要 92px 才排得下）。

**tomabc 专属注意**：
- **像素猫底板别照抄站点原样** —— ai.tomabc.com 上那只猫底下有块 `#F4F2EC` 米白方板，是为贴合站点自己的米白底画的；直接搬过来会变成玻璃条上一块硬边方片。模板里已改成透明的圆角玻璃托，猫本体一个像素未动
- logo 是**纯矢量、无 base64**（`logo.html` 只有 1KB 出头，dbs 那张是 76KB PNG）；放大要同步改 `svg` 的 `width/height` 与 `.logo-top` / `.logo-sub` 的 `font-size` 三处，否则猫和字标的视觉重量会失衡
- 组件 class 速查与色板见 `templates/tomabc/README.md`

---

## Phase 3 — 口播稿（narrations.json，约 10 min）

模板：

```json
[
  {
    "step": 1,
    "text": "大家好，欢迎回到 T Agent 开发纪实。今天是一堂调研后的分析课……",
    "duration_sec": 39
  }
]
```

规则：
- 16 条记录，`step` 1-16 对应幻灯片
- `duration_sec` 按口播文本估算：~4 字/秒，每步 35-40s / 140-160 字
- 数字读全称（"百分之七十三"），技术词口语化（"点 env 文件"）
- 总时长 ≈ 9.5-10.5 分钟

---

## Phase 4 — 音频合成（tts_batch.py，本地 Qwen3-TTS，约 5 min）

```bash
cd video/ep{NN}
HF_HUB_OFFLINE=1 /home/nvidia/workspace/grok/speech-to-speech/.venv/bin/python tts_batch.py
```

要点（参考 `video/ep54/tts_batch.py`）：
- 本地模型：`Qwen3-TTS-12Hz-1.7B-CustomVoice`（`faster_qwen3_tts`，`device="cuda"`、`bfloat16`、`local_files_only=True`）
- 音色 `serena`、语言 `chinese`、段间静音 `GAP = 0.4`
- 输出：`audio/{1..16}.wav`（24kHz PCM_16）+ `audio/full.wav`（全段拼接，段间 0.4s 静音）
- 每段打印时长 / 生成耗时 / RTF；模型加载约 1 分钟，之后每段秒级合成

---

## Phase 5 — 画面采集 + 合成（静帧，约 1 分钟）

**标准做法：只跑统一入口，不要自己写录屏或 ffmpeg 参数。**

```bash
bash /home/nvidia/workspace/Twork/video/br-cron/build.sh /path/to/video/br{NN}
```

它串两件事（都接受 `<EPDIR>` 参数，各期的 `build.sh` 只是转发壳）：

1. **`capture_stills.cjs`** —— Playwright 打开 deck，用 Web Animations API 把入场动画逐点定格
   （`getAnimations()` → `pause()` → 设 `currentTime`），逐帧存无损 PNG 到 `output/frames/`，
   并按音频时长生成带 `duration` 的 `output/frames.txt`（concat 清单）。全场约 35 秒，
   对比录屏是「与视频时长等长的实时录制」。
2. **`encode_stills.sh`** —— 按 `frames.txt` 编 CRF（16→18→20→22→24 阶梯，28MiB 交付预算兜底），
   出片后清理静帧中间产物（约 600KB/帧，日更不清会撑满盘）。

产物：`video/br{NN}/output/video-br{NN}-final.mp4`。`run.sh` 第 7-8 步走同一条路。

### 为什么不用 Playwright 录屏

Chromium `recordVideo` 走内置 VP8，1080p 实测只有 **~770kbps 且码率不可调**；后级 H.264 是
「忠实抄下源的噪声」（成片 vs 源 51dB），**所以加码率救不回来**。更要命的是接上两遍 ABR 后
会「切页即糊、约 3 秒才回稳」——ABR 缓冲区被切页的大画面变化抽干，而观众正是从那一刻开始
读新页标题：

| 切页后 | 录屏 ABR | 静帧 CRF |
|---|---|---|
| 0.6s | 15.0 dB | 32.1 dB（该页入场未走完）|
| 1s | 18.4 dB | **42.5 dB** |
| 2s / 3s | 38.3 / 40.2 dB | 42.5 dB（恒定，无爬坡）|

（br05 实测，9 分钟片，静帧档位 CRF 20。ts01b 同口径：切页前 6 秒 32.2→41.7dB。）

### 三个坑（都踩过）

- **入场时长不能写死**：模板的入场是**分级错开**的（`.slide.active > *:nth-child(n)` 各加 .08s
  延迟），整段入场 = 最大延迟 + 动画时长，实测逐页 0.55 / 0.79 / 0.87s 不等（不是 .55s）。
  写死 .55s 会让靠后的子元素只淡入到九成——成片里永远差一口气（实测底部来源行墨迹少 7.9%）。
  一律用 `a.effect.getComputedTiming().endTime` 向浏览器要真实结束时刻，模板改了也不会再错。
- **concat 分配器的末条 `duration` 不生效**，必须把末文件再列一次。漏掉时成片短掉整个末步
  停留时长（实测 299.92s → 259.72s），而且**不报错**。
- **QC 截图带 `:hover`**：`qc_shots.cjs` 用 `click("#nextBtn")` 翻页，鼠标停在按钮上，导航胶囊
  的「→」在 QC 图里是实心红圆（`.nav button:hover`）。拿 QC 图当基准比像素时必须掩掉导航区，
  否则会误判成内容缺失（实测该带 −89%）。**比像素用 PSNR，不要用「墨迹计数」这类阈值法**——
  阈值法对 3px 亚像素位移极敏感，会把编码噪声报成内容缺失。

### 回退路径（仅静帧不可用时）

`build.sh` 会在静帧采集失败时自动回退 `record.cjs` → `encode.sh`（无人值守产线宁可出一支
画质退回旧水平的片子，也不能当天没有片子）。手工录屏要点（参考 `video/ep54/record.cjs`）：
步数与每步时长自动推导（`ffprobe audio/{i}.wav` 时长 + 段间 GAP），用页面内 `nextStep()`
推进（同步 DOM 操作，无点击延迟累积）。

---

## Phase 6 — 发布（feishu-send CLI，飞书，约 2 min）

发飞书一律用通用 CLI 工具 `feishu-send`（凭据自动从 `~/.openclaw/openclaw.json` 读取），不再每期内嵌脚本。

```bash
# 文本简介（一句话 + 要点）
feishu-send text "EP{NN} {标题} 已出片：…" [--chat]

# 成品视频文件
feishu-send file video/ep{NN}/output/EP{NN}-final.mp4 [--chat]
```

要点（参考 `feishu-send` 技能）：
- 目标：**成品 / 报告 → 群聊**（加 `--chat`）；用户说「发我」→ 个人 DM（默认不加参数）
- 工具输出 `✅ 已发送到飞书 群聊/个人` 即成功（code 0）；失败会打印错误码（19001 参数错 / 19002 签名失败 / 19024 bot 不在群里等）
- 发布前先展示将发送的内容与目标（群/私聊），用户点头再发；用户已明确指令时直接发

> 旧版 tomabc-engine 网站发布（build.py `tagent_episodes` + `deploy.sh demo`）已停用：build.py 无 `tagent_episodes` 列表，网站内容停留在 2026-08 初。如需同步官网，走 `tomabc-html` 技能流程。

---

## 文件清单检查

每期完成后检查以下文件全部存在：

```
docs/html/video-{NN}-{topic}.html       ← 幻灯片（gen_deck.py 产出）
video/ep{NN}/gen_deck.py                ← 幻灯片生成脚本
video/ep{NN}/narrations.json            ← 口播稿（16 步）
video/ep{NN}/tts_batch.py               ← 本地 TTS 合成脚本
video/ep{NN}/audio/{1..16}.wav          ← 逐步音频
video/ep{NN}/audio/full.wav             ← 拼接音频
video/ep{NN}/build.sh                   ← 出片入口（转发壳）
video/ep{NN}/output/frames/ + frames.txt ← 静帧中间产物（出片后自动清理；回退录屏时改为 raw.webm）
video/ep{NN}/output/EP{NN}-final.mp4    ← 成品视频
```

hand-draw2 模板额外检查：`video/ep{NN}/fonts/`（两个 TTF，gen_deck.py 自动复制）；发布走 `feishu-send` CLI，无脚本文件。

---

## 已出版期数

| EP | 文件 | 状态 |
|:--|:-----|:----:|
| EP01 | `video-01-dev-process.html` | ✅ 已发布 |
| EP02 | `video-02-tools-security.html` | ✅ 已发布 |
| EP03 | `video-03-multi-agent.html` | ✅ 已发布 |
| EP04 | `video-04-system-prompt.html` | ✅ 幻灯片完成 |
| EP05 | `video-05-cli-session.html` | ✅ 幻灯片完成 |
| EP45-52 | `video-45-ds4-pricing.html` … `video-52-anthropic-watermark.html` | ✅ deck 已生成 |
| EP53 | `video-53-encrypted-reasoning.html` | ✅ 已发布（飞书 · 16 步深度思考课） |
| EP54 | `video-54-steganography.html` | ✅ 已发布（飞书 · 16 步深度思考课） |
| EP59 | `video-59-dsh-architecture.html` | ✅ 已出片（hand-draw2 模板来源 · 16 步） |
| pr01 | `video-pr01-visual-primitives.html` | ✅ 已发布（飞书个人 · 论文精读第 1 期 · notebook 模板首发，2026-09-02） |
| br01 | `video-br01-daily-brief.html` | ✅ 已发布（飞书个人 · AI 每日简报第 1 期 · news 演播室模板首发，2026-09-02，6:07） |
| br02 | `video-br02-daily-brief.html` | ✅ 已发布（飞书个人 · AI 每日简报第 2 期，2026-09-03，6:37） |
| br03 | `video-br03-daily-brief.html` | ✅ 已发布（飞书个人 · AI 每日简报第 3 期，2026-09-11，8:01） |
| br04 | `video-br04-daily-brief.html` | ✅ 已发布（飞书个人 · AI 每日简报第 4 期，2026-09-12，7:55） |
| br04dbs | `video-br04dbs-daily-brief.html` | ✅ 已出片（br04 内容的 DBS 毛玻璃换皮版 · dbs 模板首发，2026-09-12） |
| br05 | `video-br05-daily-brief.html` | ✅ 已发布（飞书个人 · AI 每日简报第 5 期 · **dbs 成为默认样式后首期**，2026-09-13，9:02） |
