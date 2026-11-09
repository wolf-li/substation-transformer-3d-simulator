#!/usr/bin/env python3
"""生成专用视角页：在页面副本 </body> 前注入轮询脚本。
轮询全局对象就绪 → 执行 --pre 脚本(如切换型号) → 设置相机位 → controls.update()。
用法:
  python3 make_view_page.py SRC.html OUT.html --cam "x,y,z" --tgt "x,y,z" \
      --global TransformerSim [--pre "JS代码"] [--delay 700]
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--cam', required=True, help='相机位置 "x,y,z"')
    ap.add_argument('--tgt', required=True, help='观察目标 "x,y,z"')
    ap.add_argument('--global', dest='glob', default='TransformerSim', help='就绪判断的全局对象名')
    ap.add_argument('--pre', default='', help='就绪后、设相机前执行的 JS（如型号切换）')
    ap.add_argument('--delay', type=int, default=700, help='pre 执行后等待毫秒再设相机')
    a = ap.parse_args()

    s = open(a.src, encoding='utf-8').read()
    if '</body>' not in s:
        sys.exit('src 缺少 </body>')
    pre = f"setTimeout(()=>{{ {a.pre} }},0);" if a.pre else ''
    js = (f"<script>(function w(){{ if(!window.{a.glob}){{ setTimeout(w,300); return; }}"
          f"setTimeout(()=>{{ {pre}"
          f"setTimeout(()=>{{ const T=window.{a.glob};"
          f"T.camera.position.set({a.cam}); T.controls.target.set({a.tgt}); T.controls.update(); }},{a.delay});"
          f"}},500); }})();</script></body>")
    open(a.out, 'w', encoding='utf-8').write(s.replace('</body>', js, 1))
    print('written:', a.out)

if __name__ == '__main__':
    main()
