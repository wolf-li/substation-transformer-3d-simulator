#!/usr/bin/env python3
"""从 headless chromium --dump-dom 的输出中提取 <pre id="TESTLOG"> 结果。
用法:
  chromium --headless=old ... --dump-dom URL > dom.html
  python3 extract_testlog.py dom.html   # 有 FAIL 或 ERRS>0 时退出码为 1
"""
import re, sys

def main():
    s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="TESTLOG">(.*?)</pre>', s, re.S)
    if not m:
        t = re.search(r'<title>(.*?)</title>', s)
        print('NO TESTLOG FOUND (title=%s, dom=%d bytes)' % (t.group(1) if t else '?', len(s)))
        sys.exit(2)
    log = m.group(1)
    print(log)
    errs = re.search(r'ERRS:(\d+)', log)
    bad = ('FAIL' in log) or (errs and errs.group(1) != '0')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
