# TomABC Deck — 视频幻灯片标准化模板

> 用于 T Agent 开发纪实 vlog 系列的视频幻灯片制作。
> 风格：1920×1080 全屏幻灯片，TomABC 品牌暖白风，代码走读 + 问题驱动叙事。

---

## 文件规范

```
docs/html/video-{NN}-{topic}.html
```

| 部分 | 规则 |
|------|------|
| `NN` | 两位数字：EP01 → `01`，EP05 → `05` |
| `topic` | 英文连字符：CLI 与会话管理 → `cli-session` |

---

## 标准结构（12 步）

每期固定 12 步，叙事节奏为 **问题 → 方案 → 代码 → 踩坑 → 修复 → 验证**：

| Step | 类型 | 内容 | 时长参考 |
|:----:|:----|:------|:--------:|
| 1 | **封面** | 标题 + 标签 | 15s |
| 2 | **起点问题** | 本期要解决的核心矛盾，4-6 个问题卡片 | 30s |
| 3 | **设计决策** | 架构选择，为什么这样设计 | 25s |
| 4 | **核心代码 1** | 关键实现代码，带解释 | 30s |
| 5 | **核心代码 2** | 另一个关键视角 | 25s |
| 6 | **核心代码 3** | 第三个视角（可选） | 20s |
| 7 | **踩坑 1** | 开发/测试/审计中发现的问题 | 20s |
| 8 | **踩坑 2** | 另一个问题 | 20s |
| 9 | **踩坑 3** | 安全/性能问题 | 20s |
| 10 | **横向话题** | Plan Mode/记忆注入等挂载功能 | 25s |
| 11 | **验证数据** | 测试覆盖率 + 关键指标 | 20s |
| 12 | **总结** | 本期要点时间线 + 下期预告 | 20s |

---

## HTML 模板框架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920,initial-scale=0.5">
  <title>EP{NN} {标题} — TomABC / T Agent</title>
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
    h1 { font-size:64px; font-weight:700; line-height:1.2; margin-bottom:16px; letter-spacing:-0.02em; }
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
  <!-- 12 个 slide，data-step="1" ~ data-step="12" -->
  <!-- 底部 JS 导航脚本 -->
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
  <div class="page-label">T Agent / EP{NN}</div>
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

## JS 导航脚本（每页固定）

```html
<script>
var step = 1, total = 12;
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

## 内容写作规范（vlog 风格）

### 每期叙事弧线

```
"上一期我们做了 X。遇到一个实际问题→我们这样设计→代码实现→
踩坑了（审计/测试发现）→这样修复→验证通过。
下一期做 Y。"
```

### 代码引用规则

- 只展示**关键代码片段**（5-20 行），完整文件在 GitHub
- 不需要展示的代码用 `…` 省略
- 错误示例用 `// 修复前：` 标注
- 修复后示例用 `// 修复后：` 标注

### 问题记录规则

```html
<div class="issue">
  <span class="id">VULN/B-编号:</span> 一句话描述问题
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

---

## 完整管线（6 Phase，文件级落地）

每期 EP 在 `docs/html/` 和 `video/ep{NN}/` 两个目录下产生结构化文件：

```
docs/html/video-{NN}-{topic}.html    ← Phase 2 产出：幻灯片
video/ep{NN}/
├── research.md                       ← Phase 1 产出：内容研究笔记
├── narrations.json                   ← Phase 3 产出：口播稿
├── record.cjs                        ← Phase 5 产出：录屏脚本
├── audio/                            ← Phase 4 产出：音频文件
│   ├── 01.mp3
│   ├── 02.mp3
│   └── …
└── output/
    └── EP{NN}-final.mp4              ← Phase 5 产出：成品视频
```

---

## Phase 1 — 内容研究（15 min）

模板文件：无需特定模板，但输出必须包含以下结构：

```markdown
# EP{NN} 内容研究

## 涉及的源文件
- src/xxx.rs (关键行号)

## 开发历程
- 起点：本期要解决的核心问题
- 设计决策：为什么这样设计
- 关键代码：3 个以内核心代码片段

## 踩坑记录（来自 ISSUE_REGISTER / SECURITY_AUDIT）
- 问题 1：描述 + 修复
- 问题 2：描述 + 修复

## 验证数据
- 测试数 / 覆盖率 / 编译状态
```

保存位置：`video/ep{NN}/research.md`

---

## Phase 2 — 幻灯片（20 min）

模板：本文档上方的 HTML 模板框架

输出：`docs/html/video-{NN}-{topic}.html`

规则：
- 固定 12 步（Step 1 封面 ~ Step 12 总结）
- 品牌顶栏 + 导航 + JS 脚本从模板直接复制，不改动
- 只改动 `<!-- 内容区 -->` 内部
- 创建后手动翻页验证

---

## Phase 3 — 口播稿（10 min）

模板文件：`video/ep{NN}/narrations.json`

```json
[
  {
    "step": 1,
    "text": "封面口播——本期主题的一句话介绍",
    "duration_sec": 15
  },
  {
    "step": 2,
    "text": "起点问题——4 个卡片逐一介绍",
    "duration_sec": 30
  }
]
```

规则：
- step 1-12 对应幻灯片步数
- duration_sec 根据口播文本长度估算（~4 字/秒）
- 文本不要超过 120 字（约 30 秒）
- 保存后检查总时长 ≈ 4-5 分钟

---

## Phase 4 — 音频合成（3 min）

步骤：
```bash
# 1. 从 narrations.json 提取文本逐条合成
mkdir -p video/ep{NN}/audio
for i in $(seq 1 12); do
  text=$(python3 -c "import json; d=json.load(open('video/ep{NN}/narrations.json')); print(d[$i-1]['text'])")
  edge-tts --text "$text" --voice zh-CN-XiaoxiaoNeural --write-media "video/ep{NN}/audio/$i.mp3"
done

# 2. 拼接全章音频
ffmpeg -y -f concat -safe 0 -i <(for i in $(seq 1 12); do echo "file '$PWD/video/ep{NN}/audio/$i.mp3'"; done) \
  -c copy "video/ep{NN}/audio/full.mp3"

# 3. 检查总时长
ffprobe -v quiet -of csv=p=0 -show_entries format=duration "video/ep{NN}/audio/full.mp3"
```

输出：`video/ep{NN}/audio/{01..12}.mp3` + `video/ep{NN}/audio/full.mp3`

---

## Phase 5 — 录屏 + 合成（6 min）

### 5a. 获取音频时长

```bash
for i in $(seq 1 12); do
  ffprobe -v quiet -of csv=p=0 -show_entries format=duration "video/ep{NN}/audio/$i.mp3"
done
```

### 5b. 创建录屏脚本 `video/ep{NN}/record.cjs`

模板：

```javascript
const { chromium } = require("playwright");
const path = require("path");
// 从 ffprobe 获取的每步时长（秒）+ 0.5s buffer
const STEPS = [15.5, 30.5, 25.5, 30.5, 25.5, 20.5, 20.5, 20.5, 20.5, 25.5, 20.5, 20.5];

(async () => {
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: path.join(__dirname, "output"), size: { width: 1920, height: 1080 } }
  });
  const p = await ctx.newPage();
  // 用 file:// 协议直接打开本地 HTML
  await p.goto("file://" + path.resolve(__dirname, "../../docs/html/video-{NN}-{topic}.html"),
    { waitUntil: "networkidle" });
  await p.waitForTimeout(500);

  for (let i = 0; i < STEPS.length; i++) {
    console.log("Step " + (i+1) + " — " + STEPS[i].toFixed(1) + "s");
    await p.waitForTimeout(STEPS[i] * 1000);
    if (i < STEPS.length - 1) {
      await p.click("#nextBtn");
      await p.waitForTimeout(200);
    }
  }
  await ctx.close(); await b.close();
  console.log("Recording done");
})();
```

### 5c. 合成音视频

```bash
# 重命名录制文件
mv video/ep{NN}/output/page*.webm video/ep{NN}/output/raw.webm

# 合成
ffmpeg -y -i video/ep{NN}/output/raw.webm \
  -i video/ep{NN}/audio/full.mp3 \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k -shortest \
  video/ep{NN}/output/EP{NN}-final.mp4
```

输出：`video/ep{NN}/output/EP{NN}-final.mp4`

---

## Phase 6 — 发布（2 min）

### 6a. 复制视频到网站

```bash
cp video/ep{NN}/output/EP{NN}-final.mp4 \
   /home/nvidia/workspace/grok/tomabc-engine/content/videos/t-agent/ep{NN}.mp4
```

### 6b. 添加 EP 到 build.py

编辑 `build.py` 的 `tagent_episodes` 列表，添加：

```python
{"num": "EP{NN}", "title": "{标题}",
 "desc": "{一句话描述}",
 "duration": "{X} min", "date": "{YYYY-MM-DD}",
 "video_file": "ep{NN}.mp4"},
```

### 6c. 构建并部署

```bash
cd /home/nvidia/workspace/grok/tomabc-engine
python3 build.py
bash deploy.sh demo
```

### 6d. 验证

```bash
curl -s -o /dev/null -w "%{http_code}" https://demo.tomabc.com/t-agent/ep{NN}.html
```

---

## Phase 0 — 项目初始化

新一期开始时运行：

```bash
mkdir -p video/ep{NN}/audio video/ep{NN}/output
```

---

## 文件清单检查

每期完成后检查以下文件全部存在：

```
docs/html/video-{NN}-{topic}.html    ← 幻灯片
video/ep{NN}/research.md              ← 研究笔记
video/ep{NN}/narrations.json          ← 口播稿
video/ep{NN}/audio/{01..12}.mp3       ← 逐步音频
video/ep{NN}/audio/full.mp3           ← 拼接音频
video/ep{NN}/record.cjs               ← 录屏脚本
video/ep{NN}/output/EP{NN}-final.mp4  ← 成品视频
```

---

## 制作流程（旧版保留，以上为完整版）

```
Phase 1 — 内容研究（15 min）
  ├─ 阅读对应章节源码（src/*.rs）
  ├─ 查阅 ISSUE_REGISTER.md 中的问题记录
  ├─ 查阅 SECURITY_AUDIT.md 中的安全发现
  └─ 查阅 TEST_LOG.md 中的测试问题

Phase 2 — 创建 HTML（20 min）
  ├─ 复制 video-template.html → video-{NN}-{topic}.html
  ├─ 编写 12 步内容
  └─ 验证 ← → 翻页正常

Phase 3 — 口播稿（10 min）
  ├─ 每步 15-30s 口播
  └─ 保存至 video/ep{NN}/narrations.json

Phase 4 — 音频合成（3 min）
  ├─ edge-tts 生成 step MP3
  └─ ffmpeg 拼接全章音频

Phase 5 — 录屏（6 min）
  ├─ Playwright 逐步录制 1920×1080
  └─ ffmpeg 合成音视频

Phase 6 — 发布（2 min）
  ├─ 复制 MP4 到 content/videos/t-agent/
  ├─ 添加 EP 到 build.py
  ├─ python3 build.py
  └─ bash deploy.sh demo
```

---

## 已出版期数

| EP | 文件 | 状态 |
|:--|:-----|:----:|
| EP01 | `video-01-dev-process.html` | ✅ 已发布 |
| EP02 | `video-02-tools-security.html` | ✅ 已发布 |
| EP03 | `video-03-multi-agent.html` | ✅ 已发布 |
| EP04 | `video-04-system-prompt.html` | ✅ 幻灯片完成 |
| EP05 | `video-05-cli-session.html` | ✅ 幻灯片完成 |
