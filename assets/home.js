(() => {
  const data = JSON.parse(document.getElementById('taxonomy-data').textContent);
  const panels = [...document.querySelectorAll('[data-panel]')];
  const viewport = document.querySelector('.map-viewport');
  const sizing = document.querySelector('.map-sizing');
  const canvas = document.querySelector('.map-canvas');
  const expanded = new Set(['taxonomy-root','query-retrieval','query-retrieval--1-representing-the-information-need-without-changing-the-question']);
  const widths = [210,260,370,190];
  function width(level) { return widths[level] || 210; }
  function xAt(level) { let x=28;for(let i=0;i<level;i++)x+=width(i)+85;return x; }
  let zoom = 1, diagramWidth = 1050, diagramHeight = 750;
  function scale(value) {
    zoom = Math.max(.35, Math.min(1.8,value));
    canvas.style.transform = `scale(${zoom})`;
    sizing.style.width = `${diagramWidth*zoom}px`;
    sizing.style.height = `${diagramHeight*zoom}px`;
    document.getElementById('zoom-label').textContent = `${Math.round(zoom*100)}%`;
  }
  function children(n) { return expanded.has(n.id) ? n.children : []; }
  function height(n) {
    n.boxHeight = n.level===1 ? 90 : n.level===2 ? 78 : 54;
    n.height = children(n).length ? Math.max(n.boxHeight,children(n).reduce((sum,c)=>sum+height(c),0)+18*(children(n).length-1)) : n.boxHeight;
    return n.height;
  }
  function draw() {
    height(data);
    const nodes=[], edges=[];
    function layout(n,top) {
      n.x=xAt(n.level); n.y=top+n.height/2;
      nodes.push(n);
      let childTop=top;
      for(const child of children(n)) { layout(child,childTop);edges.push([n,child]);childTop+=child.height+18; }
    }
    layout(data,28);
    diagramWidth=Math.max(...nodes.map(n=>n.x+width(n.level)))+42;
    diagramHeight=data.height+56;
    canvas.replaceChildren();
    canvas.style.width=`${diagramWidth}px`; canvas.style.height=`${diagramHeight}px`;
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
    svg.setAttribute('width',diagramWidth); svg.setAttribute('height',diagramHeight);svg.setAttribute('aria-hidden','true');
    for(const [a,b] of edges) {
      const path=document.createElementNS(svg.namespaceURI,'path');
      const x=a.x+width(a.level), mid=(x+b.x)/2;
      path.setAttribute('d',`M${x},${a.y} C${mid},${a.y} ${mid},${b.y} ${b.x},${b.y}`);
      svg.append(path);
    }
    canvas.append(svg);
    for(const n of nodes) {
      const box=document.createElement('div');box.className=`map-node level-${n.level}`;
      box.style.cssText=`left:${n.x}px;top:${n.y-n.boxHeight/2}px;width:${width(n.level)}px;min-height:${n.boxHeight}px`;
      const label=document.createElement(n.level ? 'a' : 'strong');label.textContent=n.label;
      if(n.level) label.href='#'+n.id;
      box.append(label);
      if(n.owner) { const owner=document.createElement('small');owner.textContent=n.owner;box.append(owner); }
      if(n.children.length && n.level) {
        const toggle=document.createElement('button');toggle.type='button';toggle.textContent=expanded.has(n.id)?'−':'+';
        toggle.setAttribute('aria-label',`${expanded.has(n.id)?'Collapse':'Expand'} ${n.label}`);
        toggle.setAttribute('aria-expanded',expanded.has(n.id));
        toggle.addEventListener('click',()=>{expanded.has(n.id)?expanded.delete(n.id):expanded.add(n.id);draw();const next=[...canvas.querySelectorAll('button')].find(b=>b.getAttribute('aria-label').endsWith(n.label));if(next)next.focus({preventScroll:true});});
        box.append(toggle);
      }
      canvas.append(box);
    }
    scale(zoom);
  }
  function activate(hash,scroll) {
    let id;try{id=decodeURIComponent(hash.replace(/^#/,''));}catch{return;}
    const panel=panels.find(p=>p.dataset.panel===id.split('--')[0]);if(!panel)return;
    panels.forEach(p=>p.hidden=p!==panel);
    if(scroll){const target=document.getElementById(id)||panel;target.scrollIntoView({block:'start'});target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}
  }
  document.addEventListener('click',e=>{
    const link=e.target.closest('a[href^="#"]');
    if(!link || !panels.some(p=>link.hash.startsWith('#'+p.dataset.panel)))return;
    e.preventDefault();history.pushState(null,'',link.hash);activate(link.hash,true);
  });
  window.addEventListener('hashchange',()=>activate(location.hash||'#query-retrieval',true));
  window.addEventListener('popstate',()=>activate(location.hash||'#query-retrieval',true));
  document.getElementById('zoom-in').onclick=()=>scale(zoom+.15);
  document.getElementById('zoom-out').onclick=()=>scale(zoom-.15);
  function fit(){scale(Math.min((viewport.clientWidth-24)/diagramWidth,(viewport.clientHeight-24)/diagramHeight,1));viewport.scrollTo(0,0);}
  document.getElementById('zoom-fit').onclick=fit;
  let drag;
  viewport.addEventListener('pointerdown',e=>{if(e.target.closest('a,button')||e.pointerType==='touch')return;drag={x:e.clientX,y:e.clientY,left:viewport.scrollLeft,top:viewport.scrollTop};viewport.setPointerCapture(e.pointerId);viewport.classList.add('dragging');});
  viewport.addEventListener('pointermove',e=>{if(!drag)return;viewport.scrollLeft=drag.left-(e.clientX-drag.x);viewport.scrollTop=drag.top-(e.clientY-drag.y);});
  function stop(){drag=null;viewport.classList.remove('dragging');}
  viewport.addEventListener('pointerup',stop);viewport.addEventListener('pointercancel',stop);
  draw();activate(location.hash||'#query-retrieval',false);fit();
})();
