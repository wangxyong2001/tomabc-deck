# notebook 模板 — 学霸笔记本手写纸风（tomabc-deck）

来源：note-skill「学霸笔记本 Style A」（米黄横线纸 + 手写字体），视觉与其保持一致，做视频适配。
适用：论文精读 / 学习笔记 / 知识讲解类内容（区别于 hand-draw2 的白底 doodle 风）。

## 色板（与 note-skill Style A 同源）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--paper` | `#fdf6e3` | 米黄纸面（页面底） |
| `--paper-deep` | `#f5ecd3` | 纸深档（code 底、tag） |
| `--paper-line` | `#e8e0cc` | 横线 / 卡片描边 |
| `--ink` | `#2c2c2c` | 墨黑正文 / 导航按钮 |
| `--red` | `#c0392b` | 批注红（装订线 / 强调 / 眉题） |
| `--blue` `--green` `--purple` `--orange` | `#2980b9` `#27ae60` `#8e44ad` `#e67e22` | 信息 / 正面 / 技术 / 警告 |
| `--card` | `#fffdf4` | 便签卡片白 |
| `--tape` | `rgba(255,255,255,.5)` | 胶带半透白 |

## 字体（gen_deck.py 自动复制 4 个 TTF 到工程目录 fonts/）

| family | 文件 | 用途 |
|--------|------|------|
| `MaShanZheng` | MaShanZheng-Regular.ttf | 毛笔标题 h1/h2/cover-title（**中文唯一毛笔体**） |
| `LongCang` | LongCang-Regular.ttf | 手写点缀：kicker / flow-arrow / issue 的 id / foot / cover-sub |
| `Kalam` (400/700) | Kalam-*.ttf | 数字与英文（num / cover-nums 的 n / logo-sub） |

正文字体回落到 `--font`（Noto Sans SC 等系统中文），保证 26px 长文可读。

## 页面结构

每页 = 横线本一张纸（1920×1080）：
- 左缘装订孔列（12 孔，纯 CSS `::after`，slides **不要**手放孔元素）
- 红装订线（`::before`，左 52px）
- 顶部中央胶带 `.paper-tape`（普通页自动有；放个 `<div class="paper-tape"></div>` 即可，无内容）
- 切页 write-in：`.slide.active > *` 逐级淡入上移（0.5s，最多 7 级延迟）
- **封面/总结页**：`<section class="slide cover">` 全幅居中、无孔线，不要手写太多内容

## 组件 class 清单

| class | 说明 |
|-------|------|
| `.kicker` | 眉题：手写红字 + 可选 `.en` 英文小标 |
| `h1` / `h2` / `h3` | 毛笔大标题 88/64px；h3 系统黑体 34px |
| `.card` | 便签卡片（白卡纸 + 阴影），`.card-title` 前置红条；`t-blue/t-green/t-purple` 换色 |
| `.card .num` | 卡内大数字 44px Kalam |
| `.sticker` | 顶部胶带固定的小贴纸（重点框），`.s-title` 标题 |
| `.note-pin` | 图钉便签（红圆针），独立强调 |
| `.tag` / `.tag-red` `.tag-blue` `.tag-green` | 圆角药丸标签（纸深底/淡色底） |
| `.tag-line` | 红描边透明标签 |
| `.mark` `.mark-r` `.mark-g` `.mark-o` | 荧光笔高亮（黄/粉/绿/橙，底部扫光式） |
| `.underline-red` | 红色下划线式强调 |
| `.red` `.blue` `.green` `.purple` `.orange` | 行内颜色 |
| `.issue` + `.id` | 红笔批注框（虚线红边，**收口结论**用它） |
| `.grid-2/3/4` | 等宽网格 |
| `.flow` / `.flow-box` / `.flow-arrow` | 流程链（箭头为 LongCang 手写 →） |
| `.num-row .item .n .t` | 大数字行（关键指标，n 有 .green/.blue/.ink 变体） |
| `.timeline` / `.timeline-item` | 虚线红时间线，项前圆点 |
| `pre` | 便签代码块（右上不折角，`--paper-deep` 内 code） |
| `.cover` 子类 | `.cover-kicker` `.cover-title` `.cover-sub` `.cover-tags` `.cover-nums .n .t` |
| `.foot` | 页脚手写小字（右下方） |
| `.paper-tape` | 顶部胶带装饰（空 div） |

## 期号规则（gen_deck.py ① 区）

```
EP_NN = "83"    → 工程目录 video/ep83/、deck docs/html/video-83-{topic}.html（经典 T Agent 期）
EP_NN = "pr01"  → 工程目录 video/pr01/、deck docs/html/video-pr01-{topic}.html（论文精读第 1 期）
```

非两位数字期号（`EP_NN.isdigit()==False`）时，字体路径目录段直接用 EP_NN 本身，因此**工程目录名必须等于 EP_NN**（`mkdir video/pr01`）。
`SERIES_NO` 只影响页标文案（如 "第 1 期"），不影响路径。

## 使用（Phase 2 流程）

```bash
mkdir -p video/ep{NN}/audio video/ep{NN}/output     # 或 video/pr01/
cp -r ~/.claude/skills/tomabc-deck/templates/notebook/{gen_deck.py,logo.html,notebook.css,shell.html} video/ep{NN}/
cp ~/.claude/skills/tomabc-deck/templates/notebook/slides_example_part1.html video/ep{NN}/slides_part1.html
cp ~/.claude/skills/tomabc-deck/templates/notebook/slides_example_part2.html video/ep{NN}/slides_part2.html
# 改 gen_deck.py ① ② + 替换 slides_part1/2.html 内容
cd video/ep{NN} && python3 gen_deck.py
```

校验三行：`fonts: Kalam-Bold.ttf, …`、`slides: s1 … s16`、`class check: OK`。
