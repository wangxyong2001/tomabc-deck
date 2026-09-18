# hand-draw2 模板 · doodle 手绘风

tomabc-deck 技能的**手绘风模板**（与默认「TomABC 品牌暖白风」并列）。源自 EP59（DSH 拆解 EP1）实战样式，白底 + 墨蓝描边 + 手绘卡片，标题用 ZCOOL KuaiLe、手写点缀用 Ma Shan Zheng。

## 色板

| 变量 | 值 | 用途 |
|------|------|------|
| `--ground` | `#FFFFFF` | 纯白背景（用户确认弃米黄） |
| `--surface` | `#FFFDF2` | 卡片纸白 |
| `--ink` | `#263D5B` | 墨蓝：主文字 / 描边 |
| `--ink-soft` | `#4A5A78` | 柔和文字 |
| `--ink-quiet` | `#796F91` | 浅灰紫 |
| `--hairline` | `#EADFBA` | 分隔线 / 浅描边 |
| `--border` | `#C9B97F` | 手绘描边 |
| `--blue` / `--blue-deep` | `#49B6E5` / `#1B7BA8` | 主蓝 / 深蓝 |
| `--orange` / `--orange-deep` | `#FF6B00` / `#B35100` | 主橙 / 深橙 |
| `--red` / `--red-deep` | `#E5484D` / `#B02633` | 警示红 / 深红 |
| `--gold` | `#FFE98A` | 标记黄（高亮 / 手绘下划线） |
| `--code-bg` | `#F5ECCD` | 代码底 |

## 字体

| 字体 | 角色 | 文件 |
|------|------|------|
| ZCOOL KuaiLe | 标题 / 封面大标题 | `fonts/ZCOOLKuaiLe-Regular.ttf` |
| Ma Shan Zheng | 手写强调（`.cover-accent`、`.tk-num` 数字） | `fonts/MaShanZheng-Regular.ttf` |

- `gen_deck.py` 运行时会自动把 `fonts/` 复制到 `video/ep{NN}/fonts/`，deck 内 `@font-face` 以相对路径引用，无需手工处理。
- 两个字体也已全局安装到 `~/.fonts`（Playwright / 系统渲染兜底）。

## 文件清单

| 文件 | 作用 |
|------|------|
| `shell.html` | 壳：sticky-top + 导航 + 步数自适应 JS（`<style>`/logo/页标/slides 全由 gen_deck.py 替换） |
| `hand-draw2.css` | 完整手绘样式系统（唯一 CSS 源；gen_deck.py 注入 `<style>`） |
| `gen_deck.py` | 参数化生成器：改顶部常量即可生成新一期 |
| `logo.html` | ai.tomabc.com 同款 logo（猫咪 SVG + TomABC 文字，白底版） |
| `slides_example_part1.html` | 第 1-8 步示例（覆盖全部组件类用法） |
| `slides_example_part2.html` | 第 9-16 步示例 |
| `fonts/` | 两个 TTF（约 7.4MB） |

## 组件 class 速查

| 用途 | class |
|------|------|
| 封面 | `.cover .cover-title .cover-accent .cover-desc .cover-metrics .metric .kicker` |
| 手绘下划线 | `.sqline`（h1 内 `<span class="sqline">`），宽版 `.sq-wide` |
| doodle 装饰 | `.doodle .doodle-star .doodle-arrow .doodle-circle`（封面 SVG） |
| 标签 | `.tag-row .tag .tag-gold .tag-blue .tag-red` |
| 网格 | `.grid-2 .grid-3 .grid-4 .grid-5` |
| 卡片 | `.card .card-blue .card-warn .card-red .card-mini .card-title`（grid 内自动轻微歪斜） |
| 徽标 | `.pill .pill-blue .pill-orange` |
| 出处 | `.src`（mono 小字，标文件行号） |
| 重点行 | `.issue .id .hl .hl2`（黄 / 橙高亮） |
| 手绘箭头 | `.farrow`（行内 SVG，见示例） |
| 分层条 | `.layer-strip .layer-box .layer-top` |
| 流程条 | `.flow .flow-5 .flow-box .flow-warn .flow-red .fb-sub` |
| 系列路线图 | `.series-chips .chip .chip-cur` |
| 对比表 | `.cmp-table .row-self` |
| 不能照搬 | `.cannot-list .cannot-title .cannot-row` |
| 优先级色 | `.p0`（红）`.p1`（蓝）`.p2`（橙） |
| 总结五句话 | `.takeaways .tk .tk-num` |
| 下期预告 | `.next-ep .next-label .next-title .next-desc` |
| 结尾封面 | `.cover-end` |

## 用法（tomabc-deck 技能 Phase 2）

```bash
# 1. 建目录并复制模板（slides 示例改名为正式文件）
mkdir -p video/ep{NN}/audio video/ep{NN}/output
cp -r /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/{gen_deck.py,logo.html,hand-draw2.css,shell.html} video/ep{NN}/
cp /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/slides_example_part1.html video/ep{NN}/slides_part1.html
cp /home/nvidia/.claude/skills/tomabc-deck/templates/hand-draw2/slides_example_part2.html video/ep{NN}/slides_part2.html

# 2. 改 gen_deck.py 顶部常量：SERIES / EP_NN / EP_NAME / TOPIC / DST
# 3. 逐页替换 slides_part1.html / slides_part2.html 的占位内容
# 4. 生成 + 校验（自动复制字体、校验 16 步 + class 检查）
cd video/ep{NN}
python3 gen_deck.py
```

其余 Phase（narrations → TTS → 画面采集 → 发布）与 tomabc-deck 技能标准流程一致。
本模板没有入场动画（无 `.slide.active > *` 动画声明），静帧采集会退化成硬切 1 帧——与模板本来的观感一致。
