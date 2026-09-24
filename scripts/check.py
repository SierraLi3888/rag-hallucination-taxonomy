"""Validate generated navigation, assets, anchors, and the six research templates."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.ids=set(); self.links=[]; self.nodes=0; self.h2=0
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f"Duplicate id: {a['id']}"
            self.ids.add(a['id'])
        if tag=='h2': self.h2+=1
        if tag=='section' and 'home-panel' in a.get('class','').split(): self.nodes+=1
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
docs={p.name:Document(p) for p in OUT.glob('*.html')}
assert len(docs)==7 and docs['index.html'].nodes==6
for name,doc in docs.items():
    for link in doc.links:
        url=urlsplit(link)
        if url.scheme or url.netloc: continue
        target=unquote(url.path) or name
        assert (OUT/target).is_file(), f'{name}: broken link {link}'
        if url.fragment:
            assert target in docs and unquote(url.fragment) in docs[target].ids, f'{name}: missing anchor {link}'
for a in json.loads((ROOT/'content/areas.json').read_text()):
    raw = (ROOT/'content'/(a['id']+'.md')).read_text()
    expected = sum(line.startswith('## ') for line in raw.splitlines()) + 1
    assert docs[a['id']+'.html'].h2 == expected, f'{a["id"]}: missing research sections'
print('PASS: 6 main nodes, 6 research pages, source headings preserved; all local links and anchors resolve.')

# Contributor headings must keep producing nested branches without frontend edits.
import markdown
from home import branch_tokens, render_home
sample = '''## Topic

### Mechanism

#### Analysis

Research text.

##### Detail

###### Evidence

## New empty topic

## Untouched template

To be completed by the assigned member.
'''
parser = markdown.Markdown(extensions=['toc'])
body = parser.convert(sample)
branches = branch_tokens(body, parser.toc_tokens)
assert [b['name'] for b in branches] == ['Topic', 'New empty topic']
node = branches[0]
for label in ['Mechanism', 'Analysis', 'Detail', 'Evidence']:
    assert len(node['children']) == 1
    node = node['children'][0]
    assert node['name'] == label
areas = json.loads((ROOT/'content/areas.json').read_text())
fixture = render_home([(a, {'Owner':'Test contributor','Status':'In progress'}, body, parser.toc_tokens) for a in areas], '')
import re
fixture_graph = json.loads(re.search(r'id="taxonomy-data">(.*?)</script>', fixture, re.S)[1])
for area in fixture_graph['children']:
    node = area['children'][0]
    for expected_level in range(2, 7):
        assert node['level'] == expected_level
        if expected_level < 6:
            node = node['children'][0]
print('PASS: all six contributor files support automatic branches through Markdown heading levels 2–6, including newly added empty headings.')
