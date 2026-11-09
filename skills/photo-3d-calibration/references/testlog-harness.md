# TESTLOG 自测试回归页模板

把下面脚本注入页面副本的 `</body>` 前（页面须暴露调试全局对象，如 `window.TransformerSim`）。
headless 运行 `--dump-dom` 后用 `scripts/extract_testlog.py` 提取结果。

```html
<script>
window.__errors=[]; window.onerror=(m,s,l,c)=>{__errors.push(m+' @'+l)};
(function poll(){
  if(!window.TransformerSim){ setTimeout(poll,300); return; }   // 铁律：先轮询就绪
  const T=window.TransformerSim, R=[];
  const t=(name,fn)=>{ try{ const r=fn();
      R.push((r===true?'PASS':(r===false?'FAIL':(r?'PASS':'FAIL:'+r)))+' '+name); }
    catch(e){ R.push('FAIL '+name+' :: '+e.message); } };
  setTimeout(()=>{
    // ① 数据/编码映射断言（按业务改）
    t('preset normal→000', ()=>codeOf(T.DGA_PRESETS.normal)==='000');
    // ② 型号切换断言：切换后参数与部件数同步
    const ms=document.getElementById('model-sel');
    ms.value='500'; ms.dispatchEvent(new Event('change'));
    t('switch 500kV rebuild', ()=>T.S.rated===180e3 && T.pickables.length>50);
    // ③ 交互开关断言（剖切/爆炸）
    t('clip toggle', ()=>{ T.toggleClip(); const on=T.clipOn; T.toggleClip(); return on===true; });
    // ④ 故障场景断言
    t('scenario overheat', ()=>{ T.applyScenario('overheat'); return T.S.faultHeat>0; });
    // ⑤ 收尾必须无未捕获错误
    t('no uncaught errors', ()=>window.__errors.length===0 || window.__errors.join(';'));
    document.title='TESTS_DONE';
    const pre=document.createElement('pre'); pre.id='TESTLOG';
    pre.textContent='TESTBEGIN\n'+R.join('\n')+'\nERRS:'+window.__errors.length+'\nTESTEND';
    document.body.appendChild(pre);
  }, 3000);
})();
</script>
```

## 要点

- **轮询优先**：`--pre` 类操作（型号切换等 DOM 事件）必须在全局对象就绪后派发，否则 CDN 模块未加载完时事件静默丢失，表现为"同样的脚本时好时坏"。
- **截图与回归分离**：回归页结尾若切换回默认型号，截图要另用专用视角页（`make_view_page.py`），否则截到的是旧/默认模型。
- **virtual-time-budget**：截图给 9000ms，回归给 15000ms；加载慢时优先怀疑时序而非增加预算。
- 断言覆盖四区：数据编码映射、型号切换后（参数+部件数+铭牌文案）、交互开关往返、故障场景与错误计数。
