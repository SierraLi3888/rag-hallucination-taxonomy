"""Generate a portable static website from six independently editable Markdown files."""
from pathlib import Path
from html import escape
import json, os, shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
AREAS = json.loads((ROOT / 'content/areas.json').read_text())
SECTIONS = ['Overview / Definition', 'Subcategories or Failure Modes', 'Evidence Reviewed', 'Cross-paper Comparison', 'Analysis / Synthesis', 'Current Conclusion', 'Detection & Mitigation', 'References']
assert len(AREAS) == 6 and len({a['id'] for a in AREAS}) == 6

def render(area):
    raw = (ROOT / 'content' / (area['id'] + '.md')).read_text()
    meta, body = raw.split('\n\n', 1)
    metadata = dict(line.split(': ', 1) for line in meta.splitlines())
    headings = [line[3:].strip() for line in body.splitlines() if line.startswith('## ')]
    if headings != SECTIONS:
        raise ValueError(f"{area['id']}: retain the eight required ## headings in order")
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    html = md.convert(body)
    return metadata, html, md.toc_tokens

# Validate all member files before replacing the last successful build.
records = [(a, *render(a)) for a in AREAS]
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')
(OUT / '.nojekyll').touch()

def page(title, main):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · RAG Research</title><meta name="description" content="A collaborative RAG Hallucination Taxonomy and research outcomes project.">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2313233c'/%3E%3Cpath d='M8 24V16H24V24M16 16V7' fill='none' stroke='%236dd5cb' stroke-width='3'/%3E%3C/svg%3E"><link rel="stylesheet" href="assets/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="index.html"><span class="mark">R</span> RAG / RESEARCH ATLAS</a><span class="project">5800 · Collaborative research</span></header>{main}
<footer><span>RAG Hallucination Taxonomy</span><span>Six research directions · One shared enquiry</span></footer></body></html>'''

cards=[]
for a,meta,_,_ in records:
    cards.append(f'''<a class="node n{a['member']}" href="{a['id']}.html"><span class="node-top">DIRECTION {a['member']:02d}<span>↗</span></span><h2>{escape(a['title'])}</h2><span class="node-bottom">Member {a['member']}<span>{escape(meta['Status'])}</span></span></a>''')
main='''<main id="main"><div class="intro"><div><p class="eyebrow">THE RESEARCH MAP</p><h1>RAG Hallucination<br><em>Taxonomy</em></h1></div><p class="intro-note">Explore a research direction to read its evidence, comparisons and conclusions.</p></div>
<section class="map" aria-label="Six research directions"><div class="map-heading"><span>Taxonomy overview</span><span>06 research directions</span></div><div class="tree"><svg class="connections" viewBox="0 0 1000 600" preserveAspectRatio="none" aria-hidden="true"><path d="M500 300 C380 300 420 100 310 100 M500 300 C620 300 580 100 690 100 M500 300 H310 M500 300 H690 M500 300 C380 300 420 500 310 500 M500 300 C620 300 580 500 690 500"/></svg><div class="root"><span>SHARED RESEARCH TOPIC</span><strong>RAG Hallucination</strong></div><div class="branches">'''+''.join(cards)+'''</div></div><div class="map-note">Research framework · Subcategories and findings will be developed by the assigned members.</div></section><p class="scope-note">The six branches organise team responsibilities. Their placement does not imply a causal sequence or a final classification.</p></main>'''
(OUT/'index.html').write_text(page('Taxonomy overview',main))

def child_links(tokens, depth=0):
    return ''.join(f'<li><a href="#{escape(t["id"])}">{t["name"]}</a>'+ ('<ul>'+child_links(t['children'],depth+1)+'</ul>' if t['children'] else '')+'</li>' for t in tokens)

repo=os.environ.get('GITHUB_REPOSITORY','')
for a,meta,body,tokens in records:
    nav=''.join(f'<a {"aria-current=\"page\"" if b["id"]==a["id"] else ""} href="{b["id"]}.html"><span>{b["member"]:02d}</span>{escape(b["title"])}</a>' for b in AREAS)
    toc=''.join(f'<a href="#{t["id"]}">{t["name"]}</a>' for t in tokens)
    children=tokens[1]['children']
    sub='<ul class="subtree">'+child_links(children)+'</ul>' if children else '<p class="empty">No subcategories added yet.<br>The assigned member will define this branch.</p>'
    edit=f'<a class="edit" href="https://github.com/{escape(repo)}/edit/main/content/{a["id"]}.md">Edit this research on GitHub ↗</a>' if repo else ''
    main=f'''<main id="main" class="detail"><aside class="sidebar"><a class="back" href="index.html">← Taxonomy overview</a><p class="eyebrow">RESEARCH DIRECTIONS</p><nav aria-label="Research directions">{nav}</nav></aside><div class="research"><p class="eyebrow">DIRECTION {a['member']:02d} / RESEARCH OUTCOMES</p><h1>{escape(a['title'])}</h1><div class="metadata"><span>{escape(meta['Owner'])}</span><span class="status">{escape(meta['Status'])}</span></div><p class="notice">Research content and subcategories are maintained by the assigned member. Empty sections are placeholders, not findings.</p><section class="branch-box"><h2>Branch structure</h2>{sub}</section><div class="reading-layout"><article>{body}</article><aside class="toc"><p class="eyebrow">ON THIS PAGE</p><nav aria-label="On this page">{toc}</nav>{edit}</aside></div></div></main>'''
    (OUT/(a['id']+'.html')).write_text(page(a['title'],main))
print(f'Built {len(records)+1} pages in {OUT}')
