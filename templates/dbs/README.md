# dbs 模板 · DBS 毛玻璃风（tomabc-deck 第 5 套）

> **2026-09-13 起：本模板是「视频生成的默认样式」。** 每日简报 br 系列（br-cron 无人值守产线）默认走 dbs，新建视频幻灯片默认走 dbs，不必再问选哪套。news 退为备选（br01–br05 用的是它）。

**用途**：需要「克制、留白、杂志感」的场景 —— 每日简报的视频版可以用它换皮（同内容、换模板），也适合访谈、观察类、深度解读类单集。

**设计系统来源**：`tomabc-html` / `dbs-html` 技能的 **DBS Glass**。`dbs-deck.css` 是那套设计的 **1920×1080 定尺改造版**；网页那套是流式布局，本模板所有尺寸写死 px（录制画布恒定，不需要 clamp/vw/vh）。

**风格要点**：
- 粉紫渐变底 + **三个彩色光斑**（`filter:blur(90px)`）：粉 `#F2B8C4` / 紫 `#C9BCE8` / 暖橙 `#F4D3B0`
- **半透明白玻璃卡**：`--glass:rgba(255,255,255,.55)` + `backdrop-filter:blur(20px)` + 1px 白描边 + 内高光
- **唯一点缀色是 DBS 红 `#E50014`**（`.red` / `.lede-red` / `.kicker::before` 红条）；分类色只用低饱和的 `--sec-*`
- 顶部 **sticky 玻璃导航**：`rgba(255,255,255,.45)` + `backdrop-filter:blur(18px) saturate(160%)`，只放完整 DBS logo，**高度 64px**（1080 高下取 `clamp(48px,7vh,64px)` 的上限）
- 底部玻璃导航胶囊 + `.ticker` 快讯条；进场 `.slide.active > *` 逐项 `glassIn`（上浮淡入）

**与 news 模板的关系（重要）**：**组件 class 完全同名** —— `.kicker .h1 .h2 .lead .flash-list .flash-row .panel .item .observe .section-bar .section-ghost .ticker .cover-* .end-*` 等。两套模板的 slides **可以整体平移**，只换 CSS 与壳，内容几乎不用改。差异只有：

| | news | dbs |
|---|---|---|
| 背景 | 画在 `.slide::after` 上的深藏青 + 光效 | 壳里独立的固定 `.bg` 层（渐变 + 三光斑），玻璃卡透视它 |
| 尺寸 | clamp/vw/vh 流式 | 定尺 px |
| 主色 | 头条红 `#FF4D3E` + 板块四荧光色 | DBS 红 `#E50014` + 低饱和分类色 |
| 渲染 | 轻 | **重**（blur 光斑 + backdrop-filter）—— 出片前先跑 QC 截图确认版面（静帧采集不受帧率影响，QC 是用来看溢出/错位的）|

**字体**：系统黑体栈 `Noto Sans CJK SC`（Linux 已装）→ **无 fonts/ 目录、无 @font-face、无 404 风险**。英文/编号同 news。

**期号规则**（与 notebook / news 同）：
- `EP_NN = "83"` → 目录 `video/ep83/`
- `EP_NN = "br01"` → 目录 `video/br01/`
- **同内容换皮肤**：`EP_NN = "br04dbs"`（br04 的 DBS 版）→ 目录 `video/br04dbs/`，产物 `docs/html/video-br04dbs-daily-brief.html`

**用法**：
```bash
cp -r /home/nvidia/.claude/skills/tomabc-deck/templates/dbs ~/workspace/Twork/video/<期号>/
cd ~/workspace/Twork/video/<期号>/
# 改 gen_deck.py 顶部 ① 期信息 + 写 slides_part1/2.html
python3 gen_deck.py        # → docs/html/video-<EP_NN>-<TOPIC>.html
# TTS 合成 audio/full.wav（见 SKILL.md Phase 4）
bash build.sh              # 静帧采集 + CRF 编码（一步到底，约 1 分钟）
```

**gen_deck 契约**：16 步默认（`EXPECTED_STEPS`，做 12 步短版时同步改）；slides 拆 `slides_part1.html`（1-8）+ `slides_part2.html`（9-16）；壳内替换点与 news 相同（`<a class="logo"` → `</a>`、page-label、`<!-- 导航控件 -->` 前拼接）。校验：**步数 + class 检查 + CSS 注释陷阱 lint**。`.nav` 定位在 `bottom:100px`（让出快讯条）。

**踩过的坑（不要再踩）**：

1. **CSS 注释提前闭合（真出过一次）** —— 浏览器解析 `/* ... */` 时**遇到第一个 `*/` 就结束**。如果注释正文里出现「星号紧跟斜杠」的写法（例如写通配类名 `.section-` 后接 `*/`），注释会在那里提前闭合，紧跟的正文变成非法前导，解析器一路吞到下一个 `{`，**把 `:root` 令牌块整块当成垃圾选择器丢掉**。表现：全站颜色退回黑色、玻璃卡全透明，而 CSS 文件看起来完全正常。`gen_deck.py` 的 `lint_css()` 会在生成前拦住这种情况（既扫 `-*/` 字面量，也按浏览器规则剥掉注释后验证 `:root` 仍是独立规则）。
2. **页面里不要自己加背景色** —— 玻璃卡的透视感来自 `.bg` 层，卡片上盖不透明底色会把玻璃做死。要分类标记就用 `.chip` / `.flash-row` 的 `sec-*` 变体。
3. **别沿用 news 的荧光四色** —— DBS 是红色点缀 + 低饱和分类色，荧光色在这套浅底上会脏。板块色统一走 `--sec-industry:#3B7DD8` / `--sec-safety:#E50014` / `--sec-tools:#2A8A5A` / `--sec-view:#D97706`。
4. **`.observe .from` 要在浅底上单独压深** —— 琥珀 `#D97706` 压在近白玻璃卡上只有约 3.5:1，22px 正文读着吃力，已改为 `#A85A05` 并加 600 字重。

**本模板日志**：
- 2026-09-12 · 模板建立。同日用 br04 内容换皮出 `br04dbs`（16 步，7 分 55 秒，音频直接复用 br04 的 TTS 产物）。

**约定**：deck 页标 = 「AI 每日简报 · <EP_NAME>」（由 `SERIES` / `SERIES_NO` / `EP_NAME` 拼出）；`EP_NAME` 带日期（如 `09-12 新闻播报`），方便出版表按日检索。

**顶栏 logo 规范**：完整 DBS logo（内联 base64 PNG，486×352，**底部中文小字已裁除**），保持原色、不做灰度/透明处理、底部不得再添加小字。改 logo 见 `dbs-html` 技能。
