# tomabc 模板 · TomABC 毛玻璃风（tomabc-deck 第 6 套）

**用途**：要毛玻璃那套观感、但**主体是 TomABC 自己**的片子 —— 面向外部受众的科普/讲解/品牌向内容，顶栏挂 TomABC 的猫而不是 DBS 字标。与 dbs 是同一套设计系统的两个品牌版本，**选哪个只看这段片子该署谁的名**。

**与 dbs 的关系（一句话）**：本模板 = `dbs-deck.css` **逐像素照搬** + 两处替换。除此之外没有任何差异——毛玻璃效果、光斑参数、玻璃卡透明度、blur 半径、动效时长全部原样。

| | dbs | tomabc |
|---|---|---|
| 点缀色 | `#E50014`（DBS 红） | **`#C8161D`**（TomABC 红，取自 ai.tomabc.com 的 `--red`） |
| 顶栏 logo | 横向 DBS 字标图（内联 base64 PNG 486×352） | **像素猫 SVG + `Tom`/`ABC` 字标 + `Always Be Curious` 副标**（取自 ai.tomabc.com 顶栏） |
| 其余全部 | — | **完全一致** |

验证方式：`diff <(sed 's/#C8161D/#E50014/g; s/rgba(200,22,29,/rgba(229,0,20,/g' tomabc-deck.css) ../dbs/dbs-deck.css` —— 除上述两处与注释文字外应当**无输出**。

**设计系统来源**：`tomabc-html` / `dbs-html` 的 **DBS Glass**。`tomabc-deck.css` 是那套设计的 **1920×1080 定尺改造版**；网页那套是流式布局，本模板所有尺寸写死 px（录制画布恒定，不需要 clamp/vw/vh）。

**风格要点**：
- 粉紫渐变底 + **三个彩色光斑**（`filter:blur(90px)`）：粉 `#F2B8C4` / 紫 `#C9BCE8` / 暖橙 `#F4D3B0`
- **半透明白玻璃卡**：`--glass:rgba(255,255,255,.55)` + `backdrop-filter:blur(20px)` + 1px 白描边 + 内高光
- **唯一点缀色是 TomABC 红 `#C8161D`**（`.red` / `.lede-red` / `.kicker::before` 红条）；分类色只用低饱和的 `--sec-*`
- 顶部 **sticky 玻璃导航**：`rgba(255,255,255,.45)` + `backdrop-filter:blur(18px) saturate(160%)`，只放完整 logo，**高度 92px**（放得下 56px 猫 + 两行字标；注意不是 64px，64px 是 dbs 那张 logo 图的 `img` 高度）
- 底部玻璃导航胶囊（`bottom:100px`，让出快讯条）+ `.ticker` 快讯条；进场 `.slide.active > *` 逐项 `glassIn`（上浮淡入）

**与 news / dbs 模板的关系**：**组件 class 完全同名** —— `.kicker .h1 .h2 .lead .flash-list .flash-row .panel .item .observe .section-bar .section-ghost .ticker .cover-* .end-*` 等。三套模板的 slides **可以整体平移**，只换 CSS 与壳，内容几乎不用改。差别只在：背景画在哪（news 画在 `.slide::after`；dbs/tomabc 是壳里独立的固定 `.bg` 层）、尺寸（news 流式 clamp，后两者定尺 px）、主色。

**字体**：系统黑体栈 `Noto Sans CJK SC`（Linux 已装）→ **无 fonts/ 目录、无 @font-face、无 404 风险**。

**期号规则**（与 notebook / news / dbs 同）：
- `EP_NN = "83"` → 目录 `video/ep83/`
- `EP_NN = "br01"` → 目录 `video/br01/`
- **同内容换皮肤**：`EP_NN = "br04tomabc"`（br04 的 TomABC 版）→ 目录 `video/br04tomabc/`，产物 `docs/html/video-br04tomabc-daily-brief.html`

**用法**：
```bash
cp -r /home/nvidia/.claude/skills/tomabc-deck/templates/tomabc ~/workspace/Twork/video/<期号>/
cd ~/workspace/Twork/video/<期号>/
# 改 gen_deck.py 顶部 ① 期信息 + 写 slides_part1/2.html
python3 gen_deck.py        # → docs/html/video-<EP_NN>-<TOPIC>.html
# TTS 合成 audio/full.wav（见 SKILL.md Phase 4）
bash build.sh              # 静帧采集 + CRF 编码（一步到底，约 1 分钟）
```

**gen_deck 契约**：16 步默认（`EXPECTED_STEPS`，做 12 步短版时同步改）；slides 拆 `slides_part1.html`（1-8）+ `slides_part2.html`（9-16）；壳内替换点与 news / dbs 相同（`<a class="logo"` → `</a>`、page-label、`<!-- 导航控件 -->` 前拼接）。校验：**步数 + class 检查 + CSS 注释陷阱 lint**。注意 `SKILL_TEMPLATE` 指向的是 `templates/tomabc`（不是 dbs），`css_path` 读的是 `tomabc-deck.css`。

**踩过的坑（不要再踩）**：

1. **CSS 注释提前闭合（dbs 上真出过一次）** —— 浏览器解析 `/* ... */` 时**遇到第一个 `*/` 就结束**。如果注释正文里出现「星号紧跟斜杠」的写法（例如写通配类名 `.section-` 后接 `*/`），注释会在那里提前闭合，紧跟的正文变成非法前导，解析器一路吞到下一个 `{`，**把 `:root` 令牌块整块当成垃圾选择器丢掉**。表现：全站颜色退回黑色、玻璃卡全透明，而 CSS 文件看起来完全正常。`gen_deck.py` 的 `lint_css()` 会在生成前拦住（既扫 `-*/` 字面量，也按浏览器规则剥掉注释后验证 `:root` 仍是独立规则）。
2. **页面里不要自己加背景色** —— 玻璃卡的透视感来自 `.bg` 层，卡片上盖不透明底色会把玻璃做死。要分类标记就用 `.chip` / `.flash-row` 的 `sec-*` 变体。
3. **别沿用 news 的荧光四色** —— 这套是红色点缀 + 低饱和分类色，荧光色在这浅底上会脏。板块色走 `--sec-industry:#3B7DD8` / `--sec-safety:#C8161D` / `--sec-tools:#2A8A5A` / `--sec-view:#D97706`。
4. **`.observe .from` 要在浅底上单独压深** —— 琥珀 `#D97706` 压在近白玻璃卡上只有约 3.5:1，22px 正文读着吃力，已改为 `#A85A05` 并加 600 字重。
5. **像素猫底板不要照抄站点原样** —— ai.tomabc.com 上那只猫身下有块 `#F4F2EC` 米白方板，那是为了贴合站点自己的米白底（`--ground:#F4F2EC`）；**直接搬到这里会变成玻璃条上一块硬边方片**。本模板改成透明的圆角玻璃托（`rx=7` + `rgba(255,255,255,.55)`），猫本体（耳/头/眼/鼻/嘴）一个像素未动。改 logo 见 `logo.html` 里的注释。

**本模板日志**：
- 2026-09-13 · 模板建立（照 dbs 复制改造，点缀色换 `#C8161D`、顶栏换像素猫 logo）。

**顶栏 logo 规范**：完整 TomABC logo = 像素猫 SVG（`viewBox 0 0 36 36`，`shape-rendering:crispEdges` 保住像素感）+ 右侧两行字标（`Tom` 500 字重 / `ABC` 600 字重且 `color:var(--red)`；副标 `Always Be Curious` 走 `--ink-quiet`）。**纯矢量、无 base64**，所以 `logo.html` 只有 1KB 出头（dbs 那张是 76KB 的 PNG）。放大只看 `svg` 的 `width/height` 与 `.logo-top` / `.logo-sub` 的 `font-size`，三者要同步改，否则猫和字标的视觉重量会失衡。
