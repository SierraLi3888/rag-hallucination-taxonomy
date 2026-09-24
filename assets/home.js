(() => {
  const root = JSON.parse(document.getElementById('taxonomy-data').textContent);
  const viewport = document.querySelector('.map-viewport'), canvas = document.querySelector('.map-canvas'), sizing = document.querySelector('.map-sizing');
  const reader = document.querySelector('.reader-scroll'), title = document.getElementById('selection-title'), context = document.getElementById('selection-context'), content = document.getElementById('selection-content');
  const index = new Map();
  function register(n,parent,area) { n.parent=parent;n.area=area || (n.level===1?n:null);index.set(n.id,n);n.children.forEach(c=>register(c,n,n.area)); }
  register(root,null,null);
  let activeArea=null, expanded=new Set(), selected=null, zoom=1, dimensions={width:920,height:540}, positions=new Map();
  const palette=['#8a5975','#8b7138','#4d7896','#247f80','#73679a','#677e48'];
  const width = n => n.level===0?180:n.level===1?210:n.level===2?220:170;
  const nodeHeight=n=>n.level===1?100:n.level===0?76:n.level===2?64:48;
  function visibleChildren(n) {return expanded.has(n.id)?n.children:[];}
  function measure(n) {const children=visibleChildren(n);n.span=children.length?Math.max(nodeHeight(n),children.reduce((sum,c)=>sum+measure(c),0)+(children.length-1)*20):nodeHeight(n);return n.span;}
  function setZoom(z) {zoom=Math.max(.5,Math.min(1.7,z));canvas.style.transform=`scale(${zoom})`;sizing.style.width=`${dimensions.width*zoom}px`;sizing.style.height=`${dimensions.height*zoom}px`;document.getElementById('zoom-label').textContent=Math.round(zoom*100)+'%';}
  function fit() {setZoom(Math.min(1,(viewport.clientWidth-24)/dimensions.width,(viewport.clientHeight-24)/dimensions.height));viewport.scrollTo(0,0);}
  function draw() {
    const nodes=[root],edges=[];positions=new Map();
    const sides=[root.children.slice(0,3),root.children.slice(3)];
    const totals=sides.map(side=>side.reduce((sum,n)=>sum+measure(n),0)+64);
    const total=Math.max(...totals,460);
    positions.set(root.id,{x:0,y:total/2});
    function layout(n,x,top,side) {
      const pos={x,y:top+n.span/2};positions.set(n.id,pos);nodes.push(n);
      let y=top;
      for(const c of visibleChildren(n)) {layout(c,side===1?x+width(n)+62:x-width(c)-62,y,side);edges.push([n,c,side]);y+=c.span+20;}
    }
    sides.forEach((side,i)=>{let top=(total-totals[i])/2;for(const n of side){layout(n,i===0?-width(n)-74:width(root)+74,top,i===0?-1:1);edges.push([root,n,i===0?-1:1]);top+=n.span+32;}});
    const minX=Math.min(...nodes.map(n=>positions.get(n.id).x))-35;
    dimensions={width:Math.max(...nodes.map(n=>positions.get(n.id).x+width(n)))-minX+35,height:total+50};
    nodes.forEach(n=>{positions.get(n.id).x-=minX;positions.get(n.id).y+=25;});
    canvas.replaceChildren();canvas.style.width=dimensions.width+'px';canvas.style.height=dimensions.height+'px';
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('width',dimensions.width);svg.setAttribute('height',dimensions.height);svg.setAttribute('aria-hidden','true');
    edges.forEach(([a,b,side])=>{const pa=positions.get(a.id),pb=positions.get(b.id),x1=pa.x+(side===1?width(a):0),x2=pb.x+(side===1?0:width(b));const line=document.createElementNS(svg.namespaceURI,'path');const mid=(x1+x2)/2;line.setAttribute('d',`M${x1},${pa.y} C${mid},${pa.y} ${mid},${pb.y} ${x2},${pb.y}`);line.setAttribute('class',b.area===activeArea?'active-connection':'');svg.append(line);});canvas.append(svg);
    nodes.forEach(n=>{
      const p=positions.get(n.id),button=document.createElement('button');button.type='button';button.className=`research-node depth-${n.level}${selected===n?' selected':''}${n.area===activeArea?' in-active-area':''}`;
      button.style.cssText=`left:${p.x}px;top:${p.y-nodeHeight(n)/2}px;width:${width(n)}px;min-height:${nodeHeight(n)}px;--branch-color:${palette[(n.area?.number||1)-1]}`;
      button.title=n.label;button.setAttribute('aria-label',n.label);button.dataset.node=n.id;
      if(n.children.length&&n.level)button.setAttribute('aria-expanded',expanded.has(n.id));
      if(n.level===1){const meta=document.createElement('span');meta.className='node-number';meta.textContent=String(n.number).padStart(2,'0');button.append(meta);}
      const label=document.createElement('span');label.className='node-label';label.textContent=n.shortLabel||(n.label.length>56?n.label.slice(0,53)+'…':n.label);button.append(label);
      if(n.level===1&&n.owner){const owner=document.createElement('small');owner.textContent=n.owner;button.append(owner);}
      if(n.children.length&&n.level){const indicator=document.createElement('span');indicator.className='node-disclosure';indicator.textContent=expanded.has(n.id)?'−':'+';button.append(indicator);}
      button.onclick=()=>select(n,true);canvas.append(button);
    });setZoom(zoom);
  }
  function showContent(n) {
    title.textContent=n.label;context.replaceChildren();content.replaceChildren();reader.scrollTop=0;
    const area=n.area, source=document.getElementById(area.id);
    document.getElementById('reader-breadcrumb').textContent=`DIRECTION ${String(area.number).padStart(2,'0')} / ${n.level===1?'OVERVIEW':n.level===2?'CHAPTER':'RESEARCH NOTE'}`;
    document.getElementById('reader-owner').textContent=area.owner||'';
    if(n.level>1){const full=document.createElement('p');full.textContent=n.level>2?n.parent.label:area.label;context.append(full);}
    const edit=document.getElementById('reader-edit'),sourceEdit=source.querySelector('.metadata a');edit.hidden=!sourceEdit;if(sourceEdit)edit.href=sourceEdit.href;
    document.getElementById('reader-status').textContent=source.querySelector('.status').textContent;
    if(n.level===1){
      const article=source.querySelector('article');
      for(const el of article.children){if(/^H[1-6]$/.test(el.tagName))break;content.append(el.cloneNode(true));}
      if(!n.children.length){const p=document.createElement('p');p.className='reader-empty';p.textContent='Research content is being prepared by the assigned contributor.';content.append(p);}
      else{const list=document.createElement('div');list.className='reader-chapters';n.children.forEach(c=>{const a=document.createElement('a');a.href='#'+c.id;a.textContent=c.label;list.append(a);});content.append(list);}
    }else{
      const start=document.getElementById(n.id);const level=Number(start.tagName.slice(1));
      for(let el=start.nextElementSibling;el;el=el.nextElementSibling){if(/^H[1-6]$/.test(el.tagName)&&Number(el.tagName.slice(1))<=level)break;const copy=el.cloneNode(true);copy.removeAttribute('id');copy.querySelectorAll('[id]').forEach(c=>c.removeAttribute('id'));content.append(copy);}
    }
  }
  function reveal(n){expanded=new Set();if(n.area){expanded.add(n.area.id);for(let p=n.level>2?n.parent:n;p&&p.level>1;p=p.parent)expanded.add(p.id);}}
  function select(n,push=false) {
    if(n===root){overview(push);return;}
    const collapse=push&&selected===n&&expanded.has(n.id);
    const oldArea=activeArea, oldExpanded=[...expanded].join();activeArea=n.area;selected=n;reveal(n);
    if(collapse)expanded.delete(n.id);
    showContent(n);
    const changed=oldArea!==activeArea||oldExpanded!==[...expanded].join();
    if(changed){const left=viewport.scrollLeft,top=viewport.scrollTop;draw();if(n.level===1){const p=positions.get(n.id);viewport.scrollLeft=Math.max(0,(p.x-(n.number<=3?320:30))*zoom);viewport.scrollTop=Math.max(0,p.y*zoom-viewport.clientHeight/2);}else{viewport.scrollLeft=left;viewport.scrollTop=top;}}
    else {canvas.querySelectorAll('.selected').forEach(b=>b.classList.remove('selected'));const button=[...canvas.querySelectorAll('[data-node]')].find(b=>b.dataset.node===n.id);if(button)button.classList.add('selected');}
    if(push){history.pushState(null,'','#'+n.id);title.focus({preventScroll:true});}
  }
  function overview(push=false){activeArea=null;selected=null;expanded.clear();draw();fit();if(push)history.pushState(null,'',location.pathname);}
  document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;let id;try{id=decodeURIComponent(a.hash.slice(1));}catch{return;}const n=index.get(id);if(n){e.preventDefault();select(n,true);}});
  function restore(){let n;try{n=index.get(decodeURIComponent(location.hash.slice(1)));}catch{}if(n)select(n);else overview();}
  window.addEventListener('popstate',restore);window.addEventListener('hashchange',restore);
  document.getElementById('map-overview').onclick=()=>overview(true);
  document.getElementById('zoom-in').onclick=()=>setZoom(zoom+.1);document.getElementById('zoom-out').onclick=()=>setZoom(zoom-.1);document.getElementById('zoom-fit').onclick=fit;
  let drag;viewport.addEventListener('pointerdown',e=>{if(e.target.closest('button')||e.pointerType==='touch')return;drag={x:e.clientX,y:e.clientY,left:viewport.scrollLeft,top:viewport.scrollTop};viewport.setPointerCapture(e.pointerId);viewport.classList.add('dragging');});viewport.addEventListener('pointermove',e=>{if(drag){viewport.scrollLeft=drag.left-e.clientX+drag.x;viewport.scrollTop=drag.top-e.clientY+drag.y;}});function stop(){drag=null;viewport.classList.remove('dragging');}viewport.addEventListener('pointerup',stop);viewport.addEventListener('pointercancel',stop);
  draw();fit();restore();
})();
