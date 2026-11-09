# **Substation Transformer 3D Interactive Simulation & DGA Diagnosis System**

[中文](README.md) · [English](README_en.md)

---

A Three.js-based high-fidelity 3D interactive simulation and DGA (Dissolved Gas Analysis) intelligent diagnosis system for substation transformers. Single-file app — no build step, runs directly in the browser.

[Live demo](https://wolf-li.github.io/substation-transformer-3d-simulator/)

## Features

- **Real product models**: three TBEA power transformers — SSZ-100000/110, SFSZ-240000/220 and SF-180000/500 — visually calibrated against product photos over multiple rounds
- **DGA diagnosis**: improved three-ratio method (DL/T 722-2014) with the Duval triangle as backup; built-in presets for normal operation and typical faults
- **Electro-thermal simulation**: voltage, load ratio and tap-changer linkage, with real-time loss, top-oil temperature and oil-level calculation plus trend curves
- **3D interaction**: part hover tooltips, clipping plane, exploded view, internal structure, multi-angle cameras and oil-flow particle visualization
- **Fault drills**: one-click overheat / discharge scenarios with linked Buchholz relay and pressure-relief states

## Project structure

```javascript
├── index.html                                              # System core (single file, Three.js r160 loaded via CDN)
└── skills                                                 
    └── photo-3d-calibration                                # Core workflow: ratio measurement → view page → headless screenshot → TESTLOG regression
        ├── SKILL.md                                        # Skill details
        ├── references                                      # References section
        │   ├── pitfalls.md                                 # Pitfall checklist (replace full replace, root read-only, dangling parts, adjust ratio by intuition…)
        │   └── testlog-harness.md                          # Self-test assertion page template + timing rules
        └── scripts                                         # Scripts 
            ├── extract_testlog.py                          # Extract regression results from dump-dom, exit code 1 on FAIL
            └── make_view_page.py                           # View page generator (poll global objects → switch model → set camera)
```

### About the skill

The `skills/photo-3d-calibration` directory serves as a repository for our 3D model calibration process. This sophisticated workflow implements a multi-stage, closed-loop system: starting with Reference Photos, proceeding through Parametric Modeling, capturing Headless Browser Screenshots, conducting Pixel-Level Comparison, and finally undergoing Iterative Correction. Included within are the complete workflow documentation, scripts for view page generation and regression testing, and a detailed list of common pitfalls, enabling its reuse across any project aiming to replicate Three.js industrial device models from reference images.  
**Note**: The photo-3d-calibration skill has currently only been tested on the kimi-k3 model.

### Tech stack

Three.js r160 (CDN / importmap) · Vanilla HTML / CSS / JavaScript · Zero build

### License

MIT
