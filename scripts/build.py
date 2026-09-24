"""Generate a portable static website from six independently editable Markdown files."""
from pathlib import Path
from html import escape
import json, os, shutil, re
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
    if metadata.get('Layout') == 'report':
        if not headings or headings[-1] != 'References':
            raise ValueError(f"{area['id']}: report must end with References")
        chapters = re.split(r'^## ', body, flags=re.M)[1:-1]
        for chapter in chapters:
            subs = re.findall(r'^### (.+)$', '## ' + chapter, re.M)
            if subs != ['Paper comparison', 'Analysis', 'Current conclusion', 'Evidence reviewed']:
                raise ValueError(f"{area['id']}: retain the report subsection headings")
    elif metadata.get('Layout') == 'stage-review':
        expected = ['4.1 Stage Role and Boundary', '4.2 Major Failure Mechanisms', '4.3 Comparison of Existing Literature', '4.4 Cross-Stage Effects and Hallucination Manifestations', '4.5 Section Conclusion', 'References']
        if headings != expected:
            raise ValueError(f"{area['id']}: preserve the agreed Section 4 structure")
        mechanisms = re.findall(r'^### (4\.2\.\d+ .+)$', body, re.M)
        if len(mechanisms) != 7:
            raise ValueError(f"{area['id']}: expected seven failure mechanisms")
        comparison = body.split('## 4.3 ', 1)[1].split('## 4.4 ', 1)[0]
        for theme in re.split(r'^### ', comparison, flags=re.M)[1:]:
            if re.findall(r'^#### (.+)$', theme, re.M) != ['Paper comparison', 'Analysis', 'Current conclusion', 'Evidence reviewed']:
                raise ValueError(f"{area['id']}: incomplete literature comparison")
    elif not headings:
        raise ValueError(f"{area['id']}: add at least one ## heading")
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
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2313233c'/%3E%3Cpath d='M8 24V16H24V24M16 16V7' fill='none' stroke='%236dd5cb' stroke-width='3'/%3E%3C/svg%3E"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/workbench.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="index.html"><span class="mark">R</span> RAG / RESEARCH ATLAS</a><span class="project">5800 · Collaborative research</span></header>{main}
<footer><span>RAG Hallucination Taxonomy</span><span>Six research directions · One shared enquiry</span></footer></body></html>'''

from home import render_home, branch_tokens
(OUT/'index.html').write_text(page('Taxonomy overview',render_home(records, os.environ.get('GITHUB_REPOSITORY',''))))

def child_links(tokens, depth=0):
    return ''.join(f'<li><a href="#{escape(t["id"])}">{t["name"]}</a>'+ ('<ul>'+child_links(t['children'],depth+1)+'</ul>' if t['children'] else '')+'</li>' for t in tokens)

repo=os.environ.get('GITHUB_REPOSITORY','')
for a,meta,body,tokens in records:
    nav=''.join(f'<a {"aria-current=\"page\"" if b["id"]==a["id"] else ""} href="{b["id"]}.html"><span>{b["member"]:02d}</span>{escape(b["title"])}</a>' for b in AREAS)
    toc=''.join(f'<a href="#{t["id"]}">{t["name"]}</a>' for t in tokens)
    children=branch_tokens(body,tokens)
    sub='<ul class="subtree">'+child_links(children)+'</ul>' if children else '<p class="empty">No subcategories added yet.<br>The assigned member will define this branch.</p>'
    if meta.get('Layout') in ('report', 'stage-review'):
        sub = ''.join('<details class="report-branch"><summary>' + escape(t['name']) + '</summary><a href="#' + escape(t['id']) + '">Read section</a><ul class="subtree">' + child_links(t['children']) + '</ul></details>' for t in tokens if t['name'] != 'References')
    edit=f'<a class="edit" href="https://github.com/{escape(repo)}/edit/main/content/{a["id"]}.md">Edit this research on GitHub ↗</a>' if repo else ''
    main=f'''<main id="main" class="detail"><aside class="sidebar"><a class="back" href="index.html">← Taxonomy overview</a><p class="eyebrow">RESEARCH DIRECTIONS</p><nav aria-label="Research directions">{nav}</nav></aside><div class="research"><p class="eyebrow">DIRECTION {a['member']:02d} / RESEARCH OUTCOMES</p><h1>{escape(a['title'])}</h1><div class="metadata"><span>{escape(meta['Owner'])}</span><span class="status">{escape(meta['Status'])}</span></div><p class="notice">Research content and subcategories are maintained by the assigned member. Empty sections are placeholders, not findings.</p><section class="branch-box"><h2>Branch structure</h2>{sub}</section><div class="reading-layout"><article>{body}</article><aside class="toc"><p class="eyebrow">ON THIS PAGE</p><nav aria-label="On this page">{toc}</nav>{edit}</aside></div></div></main>'''
    (OUT/(a['id']+'.html')).write_text(page(a['title'],main))
print(f'Built {len(records)+1} pages in {OUT}')
