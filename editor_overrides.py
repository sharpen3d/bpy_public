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
        if tag=='a': self.items.append({'kind':'link','start':start,'end':end,'raw':raw})
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

def safe_url(value):
    from urllib.parse import urlsplit
    value=value.strip()
    if any(ord(c)<32 for c in value) or value.startswith('//') or urlsplit(value).scheme.lower() not in {'','http','https','mailto'}:
        raise ValueError('Use a relative link, https://, http://, or mailto: address.')
    return value

class InlineSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.result=[]; self.stack=[]
    def handle_data(self,data): self.result.append(html.escape(data,quote=False))
    def handle_starttag(self,tag,attrs):
        tag={'b':'strong','i':'em'}.get(tag,tag)
        if tag=='br': self.result.append('<br>'); return
        if tag not in {'strong','em','a'}: raise ValueError('Only bold, italic, and links are supported in formatted text.')
        if tag=='a':
            attrs=dict(attrs); href=safe_url(attrs.get('href',''))
            self.result.append('<a href="'+html.escape(href,quote=True)+'">')
        else: self.result.append('<'+tag+'>')
        self.stack.append(tag)
    def handle_endtag(self,tag):
        tag={'b':'strong','i':'em'}.get(tag,tag)
        if not self.stack or self.stack[-1]!=tag: raise ValueError('Invalid formatting.')
        self.stack.pop();self.result.append('</'+tag+'>')
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)

def clean_inline(value):
    parser=InlineSanitizer(); parser.feed(value); parser.close()
    if parser.stack: raise ValueError('Invalid formatting.')
    return ''.join(parser.result)

def process(source, filename, overrides, annotate=False):
    parser=Scanner(source); parser.feed(source)
    changes=[]; counts={}; found=set(); entries=[]
    for item in sorted(parser.items,key=lambda x:(x['start'],x['kind'])):
        raw=item['raw']; fingerprint=hashlib.sha256((item['kind']+'\0'+raw).encode()).hexdigest()[:16]
        counts[fingerprint]=counts.get(fingerprint,0)+1
        key=f'{fingerprint}-{counts[fingerprint]}'
        found.add(key); entries.append((item,key,overrides.get(key)))
    text_by_start={item['start']:key for item,key,_ in entries if item['kind']=='text'}
    link_starts={item['start'] for item,key,_ in entries if item['kind']=='link'}
    for item,key,edit in entries:
        raw=item['raw']
        if item['kind']=='text':
            if edit and edit.get('kind') in {'text','rich'}:
                value=html.escape(edit['value'],quote=False) if edit['kind']=='text' else clean_inline(edit['value'])
                changes.append((item['content'],item['end'],value))
            if annotate and item['start'] not in link_starts: changes.append((item['content']-1,item['content']-1,f' data-local-edit="{key}"'))
        else:
            tag=raw
            if edit and item['kind']=='image' and edit.get('kind')=='image':
                tag=re.sub(r'\bsrc\s*=\s*(["\']).*?\1',lambda m:'src="'+html.escape(edit['value'],quote=True)+'"',tag,count=1,flags=re.I)
                if 'alt' in edit: tag=re.sub(r'\balt\s*=\s*(["\']).*?\1',lambda m:'alt="'+html.escape(edit['alt'],quote=True)+'"',tag,count=1,flags=re.I)
            if edit and item['kind']=='link' and edit.get('kind')=='link':
                url=html.escape(safe_url(edit['value']),quote=True)
                tag=re.sub(r'\bhref\s*=\s*(["\']).*?\1',lambda m:'href="'+url+'"',tag,count=1,flags=re.I)
                tag=re.sub(r'\s+data-site(?:-path)?\s*=\s*(["\']).*?\1','',tag,flags=re.I)
            if annotate:
                attrs=f' data-local-{item["kind"]}="{key}"'
                if item['kind']=='link' and item['start'] in text_by_start: attrs+=f' data-local-edit="{text_by_start[item["start"]]}"'
                tag=re.sub(r'\s*/?>$',lambda m:attrs+m.group(0),tag)
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
