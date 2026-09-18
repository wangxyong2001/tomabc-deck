#!/usr/bin/env python3
"""notebook 模板生成器：生成学霸笔记本手写纸风幻灯片（tomabc-deck 技能 · templates/notebook）。

用法（每期只改 ① 与 ② 两处）：
  ① 期信息：SERIES / SERIES_NO / EP_NN / EP_NAME / TOPIC（用于头部注释、<title>、页标、输出文件名、字体路径）
  ② SHELL / DST：壳与输出路径（默认用技能模板自带 shell.html，可改指上一期 deck 复用品牌结构）
  ③ slides_part1.html（第 1-8 步）+ slides_part2.html（第 9-16 步）：本期内容，参考 slides_example_*
  ④ 改完在 video/ep{NN}/ 下运行：python3 gen_deck.py

期号规则（EP_NN 两种写法）：
  · 经典两位数字：EP_NN = "83"  → 工程目录 video/ep83/、字体路径 …/video/ep83/fonts/
  · 带前缀系列期号：EP_NN = "pr01"（论文精读第 1 期）→ 工程目录 video/pr01/、字体路径 …/video/pr01/fonts/
  （TOPIC 用于输出文件名 video-{NN}-{topic}.html，NN = EP_NN 原样）

脚本行为：
  1. 复制技能模板 fonts/ → 本脚本所在目录 fonts/（deck 内 @font-face 相对路径引用）
  2. 以 SHELL 为底：替换头部注释 / <title> / <style>（→ notebook.css）/ page-label / 顶栏 logo
  3. 在 page-label 之后、导航控件之前拼接 slides
  4. 校验步数（默认 16 步）+ 幻灯片用到的 class 都有 CSS 定义 → 写出 DST
"""

import os, re, shutil, sys

# ═════════════════════════════ ① 每期期信息 ═════════════════════════════
SERIES    = "T Agent 开发纪实"     # 系列名
SERIES_NO = ""                     # 期号展示文案（如 "第 12 期"；不需要就留空）
EP_NN     = "NN"                   # 期号：两位数字（EP01 → "01"）或带前缀（论文精读 → "pr01"）；兼作字体路径段
EP_NAME   = "标题"                 # 本期标题（短名，用于 <title> / 页标 / 头部注释）
TOPIC     = "topic"                # 英文连字符主题（输出文件名 video-{NN}-{topic}.html）

if EP_NN.isdigit():
    VIDEO_DIR = "ep" + EP_NN       # 经典期：video/epNN/fonts
else:
    VIDEO_DIR = EP_NN              # 系列期：video/pr01/fonts

HEADER_COMMENT = f"""<!--
═══════════════════════════════════════════════════════════════════════════════
  {SERIES} · {SERIES_NO + (' · ' if SERIES_NO else '')}{EP_NAME}（{EP_NN}）
═══════════════════════════════════════════════════════════════════════════════
  系列：{SERIES}{(' · ' + SERIES_NO) if SERIES_NO else ''}
  风格：notebook 模板（学霸笔记本手写纸风 · 米黄纸 #fdf6e3 + 毛笔标题 MaShanZheng + Kalam 数字）
  结构：tomabc-deck 16 步标准结构 + 6 Phase 管线（gen_deck → narrations → TTS → 录屏 → 发布）
  顶栏：logo 采用 ai.tomabc.com 同款（猫咪 SVG + TomABC 文字）
  用法：
    1. 改 slides_part1.html / slides_part2.html 后重跑 gen_deck.py（勿手改本文件）
    2. 录制：Playwright 打开本文件，ffprobe 音频时长 +0.5s buffer 推进 #nextBtn
═══════════════════════════════════════════════════════════════════════════════
-->"""
_page_label_body = f"{SERIES}{(' · ' + SERIES_NO) if SERIES_NO else ''} · {EP_NAME}"
TITLE      = f"<title>{_page_label_body} — TomABC</title>"
PAGE_LABEL = f'<div class="page-label">{_page_label_body}</div>'

# ═════════════════════════════ ② 壳与输出 ═════════════════════════════
SKILL_TEMPLATE = "/home/nvidia/.claude/skills/tomabc-deck/templates/notebook"
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

def copy_fonts():
    """把模板自带字体复制到本目录 fonts/（deck 内 @font-face 用相对路径引用）。"""
    src_dir = os.path.join(SKILL_TEMPLATE, "fonts")
    dst_dir = os.path.join(_SCRIPT_DIR, "fonts")
    os.makedirs(dst_dir, exist_ok=True)
    for name in sorted(os.listdir(src_dir)):
        if name.lower().endswith((".ttf", ".otf", ".woff", ".woff2")):
            shutil.copy2(os.path.join(src_dir, name), os.path.join(dst_dir, name))
    print("fonts:", ", ".join(sorted(os.listdir(dst_dir))), "→", dst_dir)


def main():
    copy_fonts()

    html = open(SHELL, encoding="utf-8").read()

    # 1. 头部注释整体替换（doctype 后第一个 <!-- ... --> 块）
    html = re.sub(r'<!--.*?-->\s*(<html lang="zh-CN">)', HEADER_COMMENT + '\n' + r'\1', html, count=1, flags=re.S)

    # 2. <title>
    html = re.sub(r'<title>.*?</title>', TITLE, html, count=1, flags=re.S)

    # 3. <style> 块整体替换为 notebook.css（__EP__ → 工程目录段，用于字体相对路径）
    css = open(os.path.join(SKILL_TEMPLATE, "notebook.css"), encoding="utf-8").read()
    css = css.replace("__EP__", VIDEO_DIR)
    html = re.sub(r'<style>.*?</style>', '<style>\n' + css + '\n  </style>', html, count=1, flags=re.S)

    # 4. page-label（sticky-top 右侧）
    html = re.sub(r'<div class="page-label">.*?</div>', PAGE_LABEL, html, count=1, flags=re.S)

    # 4b. 顶栏 logo → ai.tomabc.com 同款（猫咪 + 文字整体）
    logo_html = open(os.path.join(SKILL_TEMPLATE, "logo.html"), encoding="utf-8").read().strip()
    logo_start = html.index('<a class="logo"')
    logo_end = html.index('</a>', logo_start) + len('</a>')
    html = html[:logo_start] + logo_html + html[logo_end:]

    # 5. 拼接 slides：从 page-label 所在 div 结束后，到 导航控件 前
    marker = PAGE_LABEL + "\n  </div>"
    start = html.index(marker) + len(marker)
    end = html.index('<!-- 导航控件 -->')
    html = html[:start] + "\n\n  " + PART_HEADER + slides + "  <!-- 导航控件 -->\n" + html[end:]

    # 6. 校验步数
    steps = re.findall(r'data-step="(\d+)"', html)
    expected = [str(i) for i in range(1, EXPECTED_STEPS + 1)]
    print("slides:", " ".join(f"s{s}" for s in steps))
    if steps != expected:
        print(f"FAIL - expected {len(expected)} steps, found {len(steps)}")
        sys.exit(1)

    # 7. class 使用检查（幻灯片用到的 class 是否都有定义）
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
