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
    chapter_labels = {
        '5.1 Stage Role and Boundary': '5.1 Role & boundary',
        '5.2 Major Failure Mechanisms': '5.2 Failure mechanisms',
        '5.3 Comparison of Existing Literature': '5.3 Literature comparison',
        '5.4 Cross-Stage Effects and Hallucination Manifestations': '5.4 Effects & hallucination',
        '5.5 Section Conclusion': '5.5 Conclusion',
        '5.2.1 Ambiguous or Incomplete Queries': '5.2.1 Query ambiguity',
        '5.2.2 Query Reformulation Problems': '5.2.2 Reformulation',
        '5.2.3 Query–Document Mismatch': '5.2.3 Mismatch',
        '5.2.4 Missing Relevant Evidence': '5.2.4 Missing evidence',
        '5.2.5 Irrelevant Retrieved Passages': '5.2.5 Irrelevant passages',
        '5.2.6 Ranking and Evidence Selection Failures': '5.2.6 Ranking & selection',
        '5.2.7 Multi-Hop Retrieval Failures': '5.2.7 Multi-hop failures',
        '5.3.1 Query Reformulation and Supervision': '5.3.1 Query supervision',
        '5.3.2 Retriever Alignment and Bias': '5.3.2 Alignment & bias',
        '5.3.3 Evidence Coverage and Diagnostic Granularity': '5.3.3 Evidence coverage',
        '5.3.4 Ranking and Evidence Set Selection': '5.3.4 Evidence selection',
        '5.3.5 Multi-Hop Dependencies and Iterative Retrieval': '5.3.5 Dependencies',
        '5.3.6 Evaluation of Evidence Sufficiency and Hallucination': '5.3.6 Evaluation',
        '5.4.1 From Missing Evidence to Unsupported Completion': '5.4.1 Unsupported claims',
        '5.4.2 From Distractors to Misleading or Incorrectly Attributed Claims': '5.4.2 Misapplied evidence',
        '5.4.3 From Partial Evidence to Incomplete or Contradictory Synthesis': '5.4.3 Partial synthesis',
        '5.4.4 Conditions for Attributing a Hallucination Reduction to Retrieval': '5.4.4 Causal assessment',
    }
    def apply_labels(node):
        if node['label'] in chapter_labels:
            node['shortLabel'] = chapter_labels[node['label']]
        for child in node['children']:
            apply_labels(child)
    short_areas = ['Conflict hallucination', 'Unsupported hallucination', 'Knowledge & indexing', 'Query & retrieval', 'Context construction', 'Generation & utilisation']
    for i, area in enumerate(graph):
        area['shortLabel'] = short_areas[i]
        area['number'] = i + 1
        if area['id'] == 'query-retrieval':
            apply_labels(area)
    data=json.dumps({'id':'taxonomy-root','label':'RAG Hallucination','level':0,'children':graph},ensure_ascii=False).replace('<',r'\u003c')
    return '''<main id="main" class="research-workbench"><div class="workbench-title"><div><p class="eyebrow">COLLABORATIVE RESEARCH</p><h1>RAG Hallucination Taxonomy</h1></div><span class="workspace-note">Explore the map. Read the evidence.</span></div><div class="workbench-grid"><section class="explorer" aria-label="Research mind map"><div class="explorer-toolbar"><button id="map-overview" type="button">All directions</button><span class="map-hint">Select a branch to explore</span><div class="zoom-tools"><button id="zoom-out" type="button" aria-label="Zoom out">−</button><output id="zoom-label">100%</output><button id="zoom-in" type="button" aria-label="Zoom in">+</button><button id="zoom-fit" type="button">Fit</button></div></div><div class="map-viewport" tabindex="0" aria-label="Mind map. Drag the background to pan."><div class="map-sizing"><div class="map-canvas"></div></div></div><div class="explorer-footer"><span>Click a node to expand · Drag to move</span><span>6 research directions</span></div></section><aside class="evidence-reader" aria-label="Research reading panel"><div class="reader-topline"><span id="reader-breadcrumb">RESEARCH OVERVIEW</span><span id="reader-owner"></span></div><div class="reader-scroll"><h2 id="selection-title" tabindex="-1">A map of the research</h2><div id="selection-context"></div><div id="selection-content"><p>Select a research direction on the map to explore its chapters, comparisons and findings.</p><p>Each branch is maintained by its assigned contributor.</p></div></div><div class="reader-bottom"><a id="reader-edit" hidden>Edit on GitHub ↗</a><span id="reader-status">Select a direction to begin</span></div></aside></div><div hidden id="research-sources">'''+''.join(panels)+'''</div></main><script type="application/json" id="taxonomy-data">'''+data+'''</script><script src="assets/home.js"></script>'''
