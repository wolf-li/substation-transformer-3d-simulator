---
name: photo-3d-calibration
description: 按参考照片迭代校准 Three.js 3D 工业设备模型（变压器、电机、开关柜等）的多轮视觉比对工作流，含无头浏览器截图、像素级比例测量、自测试回归页（TESTLOG）与参数化模型族架构。当用户要求"按图片复刻/仿制 3D 模型"、"模型和原图差距大"、要求"多轮校对/视觉审核"，或需要在无显示环境对 Three.js 单页应用做截图验证与回归测试时使用。
---

# 照片级 3D 模型校准工作流

## 核心闭环（每轮必走）

```
建模/修改 → 生成专用视角页 → 无头截图(正视+3/4侧视)
        → 与参考图并排比对(像素级测量) → 差异清单 → 修正 → 重复
```

用户要求"N 轮校对"时，严格完成 N 轮；每轮只修一类问题（结构 → 贴合 → 细节），防止改一处坏一处。

## 第 0 步：先量比例，再动手

连续凭感觉调整往往越改越偏。**先用 PIL 从参考图量出关键像素比例**（如"盖以上高度≈1.2×箱高"、"正面长宽比≈2.2:1"），换算成模型坐标再改代码：

```python
import numpy as np
from PIL import Image
im=np.array(Image.open('ref.png').convert('RGBA')).astype(int)
mask=(im[:,:,3]>200)&(im[:,:,:3].sum(2)>450)   # 不透明且较亮=设备本体
rows=np.where(mask[:,x0:x1].sum(1)>阈值)[0]     # 行范围→高度比例
```

先确认部件真实功能再建模（例：散热器下的圆罐是 ONAF 风扇而非储油罐）——别按几何外形猜测语义。

## 第 1 步：专用视角页（不污染主文件）

在页面副本尾部注入轮询脚本：等全局对象就绪 → 切换型号 → 设相机。用 `scripts/make_view_page.py`：

```bash
python3 scripts/make_view_page.py app/index.html /tmp/t/v_front.html \
  --cam "0.3,5.2,18.5" --tgt "0,3.8,0" --global TransformerSim \
  --pre "const ms=document.getElementById('model-sel');ms.value='500';ms.dispatchEvent(new Event('change'));"
```

**铁律：必须先轮询全局对象（如 `window.TransformerSim`）再派发任何事件**——CDN 模块加载时序不稳定，事件在模块就绪前会静默丢失，这是截图结果"时好时坏"的根因。

## 第 2 步：无头截图

```bash
chromium --headless=old --no-sandbox --disable-dev-shm-usage \
  --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --virtual-time-budget=9000 --window-size=1400,900 \
  --screenshot=/tmp/front.png 'http://localhost:PORT/v_front.html'
```

- 本地起静态服务：`python3 -m http.server PORT --directory /tmp/t`
- 截"当前模型"而非"默认模型"：测试脚本结尾若切回默认型号，截图必须用专用视角页
- 用 PIL 把渲染图与参考图缩放到同宽、上下/左右拼接对比，crop 掉 UI 面板只看 3D 视口

## 第 3 步：TESTLOG 自测试回归页

把断言脚本注入页面副本，输出 `<pre id="TESTLOG">`，headless 跑完用 `scripts/extract_testlog.py` 提取：

```bash
chromium --headless=old ... --virtual-time-budget=15000 --dump-dom URL > /tmp/dom.html
python3 scripts/extract_testlog.py /tmp/dom.html
```

断言模板（轮询全局对象 → 延迟执行 → 写入 pre → 改 title）见 `references/testlog-harness.md`。覆盖：数据编码映射、型号切换后参数/部件数、交互开关（剖切/爆炸）、故障场景、`window.onerror` 计数。**每次修改后必须重跑回归再交付。**

## 参数化模型族架构（推荐代码模式）

新增型号 = 规格表加一行，而非复制建模代码：

- `MODEL_SPECS` 规格表：每型号一条记录（尺寸数组 `tank:[w,h,d]`、套管高、散热器数、材质/布局特征开关、业务物理参数如空载/负载损耗）
- `buildModel(specKey)` 全量重建：`root.clear()` 保留特效层，重置 `pickables/explodables/故障部件表` 与模块级 `let` 共享引用（仿真、流道、故障高亮等子系统据此取最新几何）
- 特征开关命名（`white/radFan/sideLimbs`）优于型号 if-else
- 物理公式与型号解耦：`pFe=P0·(Φ/1.7)²`、`pCu=PK·(负载率)²`，P0/PK 从规格表读

## 防坑清单

修改多轮后必查 `references/pitfalls.md`，高频坑：

1. Python `str.replace` 默认替换**全部**出现——锚点必须唯一，或 `replace(old,new,1)`+`assert old in s`
2. 平台快照后文件变 root 只读：`os.remove(p)` 后重写
3. 支撑柱/附件要算到目标面，防悬空；套管排布先核对附件 z 范围防相交
4. JS 语法检查：`node --check` 只认 `.mjs`，需先提取 `<script type="module">` 内容
5. 梯子/爬梯等共享部件的位置要按型号规格条件化
