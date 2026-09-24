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
        if tag=='a' and 'node' in a.get('class','').split(): self.nodes+=1
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
    assert docs[a['id']+'.html'].h2==9, f'{a["id"]}: missing research sections'
print('PASS: 6 main nodes, 6 research pages, 8 sections each; all local links and anchors resolve.')
