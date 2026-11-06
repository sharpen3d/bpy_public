"""Apply local visual edits to generated portfolio pages after each build."""
import hashlib, html, json, re, os
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OVERRIDES = ROOT / 'content/editor-overrides.json'
TAGS = {'h1','h2','h3','h4','h5','h6','p','span','a','li','figcaption','strong','em','label','time','dt','dd','button'}

class Scanner(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source=source; self.lines=[0]
        for m in re.finditer('\n',source): self.lines.append(m.end())
        self.stack=[]; self.items=[]
    def position_offset(self):
        line,col=self.getpos(); return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        start=self.position_offset(); raw=self.get_starttag_text(); end=start+len(raw)
        if self.stack: self.stack[-1]['child']=True
        if tag=='img': self.items.append({'kind':'image','start':start,'end':end,'raw':raw})
        if tag not in {'img','br','meta','link','input','source','hr','area','base','embed','param','track','wbr'}:
            self.stack.append({'tag':tag,'start':start,'content':end,'child':False})
    def handle_startendtag(self,tag,attrs):
        start=self.position_offset(); raw=self.get_starttag_text()
        if self.stack: self.stack[-1]['child']=True
        if tag=='img': self.items.append({'kind':'image','start':start,'end':start+len(raw),'raw':raw})
    def handle_endtag(self,tag):
        if not self.stack: return
        if self.stack[-1]['tag']!=tag: return
        item=self.stack.pop(); end=self.position_offset(); raw=self.source[item['content']:end]
        if tag in TAGS and not item['child'] and raw.strip() and not any(x['tag'] in {'script','style','head','svg'} for x in self.stack):
            self.items.append({'kind':'text','start':item['start'],'content':item['content'],'end':end,'raw':raw})

def process(source, filename, overrides, annotate=False):
    parser=Scanner(source); parser.feed(source)
    changes=[]; counts={}; found=set()
    for item in sorted(parser.items,key=lambda x:x['start']):
        raw=item['raw']; fingerprint=hashlib.sha256((item['kind']+'\0'+raw).encode()).hexdigest()[:16]
        counts[fingerprint]=counts.get(fingerprint,0)+1
        key=f'{fingerprint}-{counts[fingerprint]}'
        edit=overrides.get(key); found.add(key)
        if item['kind']=='text':
            if edit and edit.get('kind')=='text': changes.append((item['content'],item['end'],html.escape(edit['value'],quote=False)))
            if annotate: changes.append((item['content']-1,item['content']-1,f' data-local-edit="{key}"'))
        else:
            tag=raw
            if edit and edit.get('kind')=='image':
                tag=re.sub(r'\bsrc\s*=\s*(["\']).*?\1',lambda m:'src="'+html.escape(edit['value'],quote=True)+'"',tag,count=1,flags=re.I)
                if 'alt' in edit: tag=re.sub(r'\balt\s*=\s*(["\']).*?\1',lambda m:'alt="'+html.escape(edit['alt'],quote=True)+'"',tag,count=1,flags=re.I)
            if annotate: tag=re.sub(r'\s*/?>$',lambda m:f' data-local-image="{key}"'+m.group(0),tag)
            if tag!=raw: changes.append((item['start'],item['end'],tag))
    for start,end,value in sorted(changes,reverse=True): source=source[:start]+value+source[end:]
    return source, sorted(set(overrides)-found)

def apply_all():
    data=json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    cache=os.environ.get('PORTFOLIO_EDITOR_PREVIEW')
    generated=[p for p in ROOT.rglob('*.html') if not any(part in {'archive','.git','.vs'} for part in p.relative_to(ROOT).parts)]
    for path in generated:
        name=path.relative_to(ROOT).as_posix(); edits=data.get(name,{})
        source=path.read_text()
        output, missing=process(source,name,edits)
        if missing: raise ValueError(f'{name}: {len(missing)} visual edits no longer match their original content; review content/editor-overrides.json')
        if edits: path.write_text(output)
        if cache:
            preview,_=process(source,name,edits,annotate=True)
            destination=Path(cache)/name; destination.parent.mkdir(parents=True,exist_ok=True); destination.write_text(preview)
