#!/usr/bin/env python3
"""tomabc 模板生成器：生成 TomABC 毛玻璃风幻灯片（tomabc-deck 技能 · templates/tomabc）。

用法（每期只改 ① 与 ② 两处）：
  ① 期信息：SERIES / SERIES_NO / EP_NN / EP_NAME / TOPIC（用于头部注释、<title>、页标、输出文件名）
  ② SHELL / DST：壳与输出路径（默认用技能模板自带 shell.html）
  ③ slides_part1.html（第 1-8 步）+ slides_part2.html（第 9-16 步）：本期内容，参考 slides_example_*
  ④ 改完在 video/{EP_NN}/ 下运行：python3 gen_deck.py

期号规则（EP_NN 三种写法，与 notebook / news 模板一致）：
  · 经典两位数字：EP_NN = "83"    → 工程目录 video/ep83/
  · 带前缀系列号：EP_NN = "br01"  → 工程目录 video/br01/
  · 同模板改写版：EP_NN = "br04dbs" → 工程目录 video/br04dbs/（同一内容的另一套皮肤）
  （TOPIC 用于输出文件名 video-{NN}-{topic}.html，NN = EP_NN 原样）

设计系统来源：tomabc-html / dbs-html 的 DBS Glass（粉紫渐变 + 彩色光斑 + 半透明白玻璃卡 + 红点缀）。
本模板是 **dbs 模板的 TomABC 品牌版**：毛玻璃效果（渐变/光斑/玻璃卡/blur 参数）逐像素一致，
只换两处 —— ① 点缀色 #E50014 → #C8161D（TomABC 红）② 顶栏 logo → ai.tomabc.com 那套
（像素猫 SVG + Tom / ABC 字标 + Always Be Curious 副标）。
样式文件 templates/tomabc/tomabc-deck.css 是该系统的 1920×1080 定尺改造版；组件 class 与 news 模板同名，
三套模板（news / dbs / tomabc）的内容可互相平移（只换 CSS 与壳，slides 基本不动）。

与 news 模板的差异：
  · 背景不是画在 .slide 上，而是壳里一个固定的 .bg 层（渐变 + 三光斑），玻璃卡片透视它
  · 定尺字号（无 clamp / vw / vh），因为录制画布恒为 1920×1080
  · 光斑与玻璃都用 blur，渲染较重 —— 录屏前务必先跑 QC 截图确认没掉帧/没糊

脚本行为：
  1. 以 SHELL 为底：替换头部注释 / <title> / <style>（→ tomabc-deck.css）/ page-label / 顶栏 logo
  2. 在 page-label 之后、导航控件之前拼接 slides
  3. 校验步数（默认 16 步）+ 幻灯片用到的 class 都有 CSS 定义 → 写出 DST
"""

import os, re, sys

# ═════════════════════════════ ① 每期期信息 ═════════════════════════════
SERIES    = "AI 每日简报"          # 系列名
SERIES_NO = ""                     # 期号展示文案（如 "第 12 期"；不需要就留空）
EP_NN     = "NN"                   # 期号：两位数字（"01"）或带前缀（"br01"）
EP_NAME   = "日期 新闻播报"        # 本期标题（短名，用于 <title> / 页标 / 头部注释）
TOPIC     = "topic"                # 英文连字符主题（输出文件名 video-{NN}-{topic}.html）

HEADER_COMMENT = f"""<!--
═══════════════════════════════════════════════════════════════════════════════
  {SERIES} · {SERIES_NO + (' · ' if SERIES_NO else '')}{EP_NAME}（{EP_NN}）
═══════════════════════════════════════════════════════════════════════════════
  系列：{SERIES}{(' · ' + SERIES_NO) if SERIES_NO else ''}
  风格：tomabc 模板（TomABC 毛玻璃风 · 粉紫渐变底 + 彩色光斑 + 半透明白玻璃卡 + TomABC 红点缀 · 系统黑体 Noto Sans CJK SC）
        与 dbs 模板同源，仅点缀色与顶栏 logo 不同
  结构：tomabc-deck 16 步标准结构 + 6 Phase 管线（gen_deck → narrations → TTS → 录屏 → 发布）
  顶栏：完整 TomABC logo（像素猫 SVG + 字标 + 副标，取自 ai.tomabc.com）
  用法：
    1. 改 slides_part1.html / slides_part2.html 后重跑 gen_deck.py（勿手改本文件）
    2. 录制：Playwright 打开本文件，ffprobe 音频时长 +0.4s GAP 绝对时间轴推进 nextStep()
    3. 玻璃与光斑靠 blur 实现，渲染比 news 模板重——录屏前先跑 QC 截图
═══════════════════════════════════════════════════════════════════════════════
-->"""
_page_label_body = f"{SERIES}{(' · ' + SERIES_NO) if SERIES_NO else ''} · {EP_NAME}"
TITLE      = f"<title>{_page_label_body} — TomABC</title>"
PAGE_LABEL = f'<div class="page-label">{_page_label_body}</div>'

# ═════════════════════════════ ② 壳与输出 ═════════════════════════════
SKILL_TEMPLATE = "/home/nvidia/.claude/skills/tomabc-deck/templates/tomabc"
SHELL = SKILL_TEMPLATE + "/shell.html"      # 默认模板自带壳；也可改成上一期 deck 绝对路径
DST   = f"/home/nvidia/workspace/Twork/docs/html/video-{EP_NN}-{TOPIC}.html"

EXPECTED_STEPS = 16                        # 标准 16 步；做 12 步短版时改成 12（并同步 narrations / 口播节奏）

# ═════════════════════════════ ③ slides 内容 ═════════════════════════════
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
slides = ""
for fname in ("slides_part1.html", "slides_part2.html"):
    with open(os.path.join(_SCRIPT_DIR, fname), encoding="utf-8") as f:
        slides += f.read() + "\n"

PART_HEADER = f"""  <!-- ══════════ {_page_label_body}（第 1-{EXPECTED_STEPS} 步）══════════ -->
  <!-- 拼装：{os.path.basename(__file__)}（勿手改生成文件，改 slides_part*.html 后重跑） -->
"""

# ═════════════════════════════ 主流程 ═════════════════════════════

def lint_css(css: str, path: str) -> list:
    """CSS 注释陷阱检查。

    浏览器解析注释的规则是「遇到第一个 */ 就结束」。若注释正文里出现
    「-*/」这类通配写法（如 .section-*/），注释会提前闭合，后面紧跟的正文
    变成非法前导，解析器会一路吞到下一个 { —— :root 令牌块就是这样整块
    失效的，表现为全站颜色退回黑色、背景全透明，而文件看起来完全正常。

    返回告警列表（空 = 通过）。
    """
    warns = []
    for i, line in enumerate(css.splitlines(), 1):
        if "-*/" in line:
            warns.append(f"第 {i} 行注释含「-*/」，会提前闭合 CSS 注释：{line.strip()[:70]}")
    # 兜底：按浏览器规则剥掉注释后，:root 必须还是一行新规则的开头
    stripped, i = [], 0
    while i < len(css):
        j = css.find("/*", i)
        if j < 0:
            stripped.append(css[i:]); break
        stripped.append(css[i:j])
        k = css.find("*/", j + 2)
        if k < 0:
            stripped.append(css[j:]); break
        i = k + 2
    if not re.search(r'(?m)^\s*:root\s*\{', "".join(stripped)):
        warns.append("剥掉注释后 :root 不是独立规则 —— CSS 注释疑似被提前闭合")
    return warns


def main():
    html = open(SHELL, encoding="utf-8").read()

    # 1. 头部注释整体替换（doctype 后第一个 <!-- ... --> 块）
    html = re.sub(r'<!--.*?-->\s*(<html lang="zh-CN">)', HEADER_COMMENT + '\n' + r'\1', html, count=1, flags=re.S)

    # 2. <title>
    html = re.sub(r'<title>.*?</title>', TITLE, html, count=1, flags=re.S)

    # 3. <style> 块整体替换为 tomabc-deck.css（先过注释陷阱检查，注释坏了后面全白搭）
    css_path = os.path.join(SKILL_TEMPLATE, "tomabc-deck.css")
    css = open(css_path, encoding="utf-8").read()
    css_warns = lint_css(css, css_path)
    for w in css_warns:
        print("FAIL - CSS:", w)
    if css_warns:
        sys.exit(1)
    html = re.sub(r'<style>.*?</style>', '<style>\n' + css + '\n  </style>', html, count=1, flags=re.S)

    # 4. page-label（sticky-top 右侧）
    html = re.sub(r'<div class="page-label">.*?</div>', PAGE_LABEL, html, count=1, flags=re.S)

    # 4b. 顶栏 logo → TomABC 完整 logo（像素猫 SVG + 字标）
    logo_html = open(os.path.join(SKILL_TEMPLATE, "logo.html"), encoding="utf-8").read().strip()
    logo_start = html.index('<a class="logo"')
    logo_end = html.index('</a>', logo_start) + len('</a>')
    html = html[:logo_start] + logo_html + html[logo_end:]

    # 5. 拼接 slides：从 page-label 所在 div 结束后，到 导航控件 前
    marker = PAGE_LABEL + "\n  </div>"
    start = html.index(marker) + len(marker)
    end = html.index('<!-- 导航控件 -->')
    html = html[:start] + "\n\n  " + PART_HEADER + slides + "  <!-- 导航控件 -->\n" + html[end:]

    # 6. 校验背景层还在（玻璃卡片的透视源，删了就变平底）
    if 'class="bg"' not in html:
        print("WARN - 壳里没有 .bg 背景层，玻璃卡片会失去透视源")

    # 7. 校验步数
    steps = re.findall(r'data-step="(\d+)"', html)
    expected = [str(i) for i in range(1, EXPECTED_STEPS + 1)]
    print("slides:", " ".join(f"s{s}" for s in steps))
    if steps != expected:
        print(f"FAIL - expected {len(expected)} steps, found {len(steps)}")
        sys.exit(1)

    # 8. class 使用检查（幻灯片用到的 class 是否都有定义）
    used = set()
    for m in re.finditer(r'class="([^"]+)"', slides):
        used.update(m.group(1).split())
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css)) | {"slide", "active"}
    missing = sorted(c for c in used if c not in defined)
    if missing:
        print("WARN - 幻灯片用到但 CSS 未定义:", ", ".join(missing))
    else:
        print("class check: OK")

    with open(DST, "w", encoding="utf-8") as f:
        f.write(html)
    print("written:", DST)


if __name__ == "__main__":
    main()
