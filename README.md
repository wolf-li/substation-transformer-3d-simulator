# 变电站变压器 3D 交互仿真与油色谱智能诊断系统

[中文](README.md) · [English](README_en.md)

---

基于 Three.js 的变压器高精度 3D 交互仿真与油色谱（DGA）智能诊断系统。单文件应用，无需构建，浏览器直接运行。

[在线演示](https://wolf-li.github.io/substation-transformer-3d-simulator/)

### 功能特性

- **真实型号建模**：TBEA SSZ-100000/110、SFSZ-240000/220、SF-180000/500 三款电力变压器，外观按产品照片多轮视觉校准
- **DGA 智能诊断**：改良三比值法（DL/T 722-2014）+ Duval 三角形备用诊断，内置正常运行与典型故障预设样本
- **电气-热耦合仿真**：电压、负载率、分接开关联动，损耗、顶层油温、油位实时计算并绘制曲线
- **3D 交互**：部件悬停说明、剖切、爆炸视图、内部结构透视、多视角切换、油流粒子可视化
- **故障演练**：过热 / 放电等故障场景一键注入，瓦斯继电器、压力释放阀等保护状态联动

### 项目结构

```javascript
├── index.html                                              # 系统核心（单文件，Three.js r160通过CDN引入）
└── skills                                                
    └── photo-3d-calibration                                # 核心工作流：比例测量→视角页→无头截图→TESTLOG回归
        ├── SKILL.md                                        # 技能详情
        ├── references                                      # 参考资料
        │   ├── pitfalls.md                                 # 防坑清单（全替换、root只读、悬空部件、凭感觉调比例...）
        │   └── testlog-harness.md                          # 自测试断言页模板 + 时序铁律
        └── scripts                                         # 脚本工具
            ├── extract_testlog.py                          # 从dump-dom提取回归结果，FAIL时退出码1
            └── make_view_page.py                           # 视角页生成器（轮询全局对象→切换型号→设定相机）
```

### 关于配套 Skill

`skills/photo-3d-calibration` 目录沉淀了本项目 3D 模型的校准方法：参考照片 → 参数化建模 → 无头浏览器截图 → 像素级比对 → 迭代修正的多轮闭环，内含工作流说明、视角页生成与回归测试脚本、防坑清单，可复用于任何按参考图复刻 Three.js 工业设备模型的任务。
**注意**：photo-3d-calibration 这个 skill 目前只在 kimi-k3 模型上进行过测试。

### 技术栈

Three.js r160（CDN / importmap）· 原生 HTML / CSS / JavaScript · 零构建

### 许可证

MIT
