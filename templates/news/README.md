# news 模板 · 演播室电视风每日简报播报（tomabc-deck 第 4 套）

**用途**：AI 每日简报 → 6-7 分钟新闻播报视频（每期 12-16 步）。源头数据：`ai.tomabc.com/daily-brief/`（或本地 RAG 项目 digest），播报脚本由原始新闻**改写总结**，勿照抄原文。

**风格要点**：
- 深藏青演播室底（`#0a1f40 → #081a33`）+ 顶部冷光 + 底部红束（`.slide::after`）
- 头条红白大字（`.h1` 88px / `.h2` 56px / 900 字重）+ `.kicker` 频道小标
- **板块四色**：行业=蓝 `#5ac8fa` / 安全=红 `#ff4d3e` / 工具=绿 `#4cd964` / 观察=琥珀 `#ffd166`
- 每页底部**下第三屏快讯条** `.ticker`（静态 chyron，一条相关快讯）
- 组件：`.chip` 分类标 / `.flash-list`+`.flash-row` 速览行 / `.panel` 深度卡（`.metric` 数字） / `.section-*` 板块转场页（幽灵英文 + 红条） / `.item` 编号条目 / `.observe` 今日观察引用块 / `.stat` 封面数据 / `.end-*` 收尾页 / `.tagline` 关键词胶囊
- 分类标签同时用 class 上色：`chip`/`flash-row`/`item`/`panel .no` 的 `safety`/`tools` 变体
- 进场：`.slide.active > *` 逐项 tvIn（快切感），直系子级 ≤7 节奏最佳

**字体**：系统黑体栈 `Noto Sans CJK SC`（Linux 已装）→ **无 fonts/ 目录、无 @font-face、无 404 风险**；英文/编号用 `Droid Sans Mono` 系。gen_deck.py 已去掉 copy_fonts。

**期号规则**（与 notebook 同）：`EP_NN` 全数字 `"83"` → 目录 `video/ep83/`；带前缀 `"br01"` → 目录就叫 `video/br01/`。每日简报建议 `brNN`（br01=第 1 期），`TOPIC="daily-brief"` → 产物 `docs/html/video-br01-daily-brief.html`。

**本模板日志**：
- 2026-09-02 · br01：AI 每日简报第 1 期（12 条新闻 → 16 步播报，6 分 40 秒左右成片）

**约定**：deck 页标 = 「AI 每日简报 · <EP_NAME>」；EP_NAME 带日期（如 `09-02 新闻播报`），方便出版表按日检索。

**结构与 gen_deck 契约**：16 步默认（`EXPECTED_STEPS`）；slides 拆 `slides_part1.html`（1-8）+ `slides_part2.html`（9-16）；壳内替换点与 notebook 相同（`<a class="logo"` → `</a>`、page-label、`<!-- 导航控件 -->` 前拼接）；.nav 定位在 bottom 86px（让出快讯条）。校验：步数 + class 检查。
