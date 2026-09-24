"""Render the homepage tree and research reader from the same member content."""
from html import escape, unescape
import re, json

def branch_tokens(body, tokens):
    def populated(t):
        if t['children']: return True
        section = re.search(r'<h2 id="'+re.escape(t['id'])+r'">.*?</h2>(.*?)(?=<h2 |$)', body, re.S)
        text = re.sub(r'<[^>]+>', '', section[1] if section else '').strip()
        return bool(text and text not in ('To be completed by the assigned member.', 'To be completed by the assigned member (if applicable).'))
    return [t for t in tokens if populated(t)]

def render_home(records, repo):
    panels, graph = [], []
    for area, meta, body, tokens in records:
        key = area['id']
        chapters = branch_tokens(body, tokens)
        def graph_node(t, level):
            return {'id':key+'--'+t['id'], 'label':unescape(t['name']), 'level':level, 'children':[graph_node(c,level+1) for c in t['children']]}
        graph.append({'id':key,'label':area['title'],'owner':meta['Owner'],'level':1,'children':[graph_node(t,2) for t in chapters]})
        body = re.sub(r'id="([^"]+)"', lambda m: f'id="{key}--{m[1]}"', body)
        body = body.replace('href="#', f'href="#{key}--')
        edit = f'<a href="https://github.com/{escape(repo)}/edit/main/content/{key}.md">Edit on GitHub ↗</a>' if repo else ''
        panels.append(f'''<section class="home-panel" id="{key}" data-panel="{key}"><div class="reader-heading"><p class="eyebrow">DIRECTION {area['member']:02d} / RESEARCH OUTCOMES</p><h2>{escape(area['title'])}</h2><div class="metadata"><span>{escape(meta['Owner'])}</span><span class="status">{escape(meta['Status'])}</span>{edit}</div></div><article>{body}</article></section>''')
    data=json.dumps({'id':'taxonomy-root','label':'RAG Hallucination','level':0,'children':graph},ensure_ascii=False).replace('<','\u003c')
    return '''<main id="main" class="mindmap-home"><div class="atlas-title"><div><p class="eyebrow">RESEARCH ATLAS</p><h1>RAG Hallucination Taxonomy</h1></div><p>Expand branches with +. Select a node to read its research below.</p></div><section class="mindmap-shell" aria-label="Interactive taxonomy mind map"><div class="map-toolbar"><span>Research map</span><div><button type="button" id="zoom-out" aria-label="Zoom out">−</button><output id="zoom-label" aria-live="polite">100%</output><button type="button" id="zoom-in" aria-label="Zoom in">+</button><button type="button" id="zoom-fit">Fit map</button></div><span>Drag to pan · Scroll to explore</span></div><div class="map-viewport" tabindex="0" aria-label="Scrollable mind map"><div class="map-sizing"><div class="map-canvas"></div></div></div></section><div class="atlas-reader mindmap-reader">'''+''.join(panels)+'''</div></main><script type="application/json" id="taxonomy-data">'''+data+'''</script><script src="assets/home.js"></script>'''
