#!/usr/bin/env python3
"""Build the static portfolio. Edit content/projects.json and assets/portfolio.css; no dependencies required."""
from pathlib import Path
from site_credit import author_footer
import html
import json
from datetime import date

ROOT=Path(__file__).resolve().parent
PROJECTS=json.loads((ROOT/'content/projects.json').read_text())
ARCHIVED=json.loads((ROOT/'content/archived-documents.json').read_text())
RESUME=json.loads((ROOT/'content/resume.json').read_text())
DEVLOG=sorted(json.loads((ROOT/'content/devlog.json').read_text()),key=lambda entry:entry['date'],reverse=True)
SITES=json.loads((ROOT.parent/'sites.json' if (ROOT.parent/'sites.json').exists() else ROOT/'sites.json').read_text())
TUTORIALS=json.loads((ROOT/'content/tutorials.json').read_text())
EMAIL='stilson.luke@gmail.com'
esc=lambda value:html.escape(str(value),quote=True)

NAMES={'tools':'Independent tool','shipped':'Shipped work','experiments':'Personal study','engine':'Personal engine'}

def url(project): return project.get('page',f'projects/{project["id"]}.html')
def link(href,label,cls='text-link'):
    extra=' target="_blank" rel="noopener noreferrer"' if href.startswith('https://') else ''
    return f'<a class="{cls}" href="{esc(href)}"{extra}>{label}</a>'
def site_link(site,path,label,cls='text-link'):
    href=SITES[site]['url'].rstrip('/')+'/'+path
    return f'<a class="{cls}" href="{esc(href)}" data-site="{site}" data-site-path="{esc(path)}">{label}</a>'
def header(root='',active=''):
    items=[('Work','index.html#work'),('Tutorials','tutorials.html'),('About','index.html#about'),('Résumé','resume.html'),('Email','mailto:'+EMAIL)]
    nav=''.join(f'<a href="{esc(path if path.startswith(("mailto:","https:")) else root+path)}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for name,path in items)
    return f'<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="identity" href="{root}index.html" aria-label="Luke Stilson home">Luke Stilson<span>Technical art & tools</span></a><nav aria-label="Main navigation">{nav}</nav></header>'
def footer(root=''):
    return author_footer(root)

def page(title,description,body,root='',active='',body_class=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Luke Stilson</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#0a0b0d"><link rel="stylesheet" href="{root}assets/portfolio.css?v=20261105-openvat-feature"><link rel="stylesheet" href="{root}assets/authorship.css?v=2">
<script src="{root}assets/portfolio.js" defer></script><script src="{root}assets/related-sites.js?v=20261105-credit2" defer></script></head>
<body id="top" class="{body_class}">{header(root,active)}{body}{footer(root)}</body></html>'''
def recognition(p, compact=False):
    if compact:
        labels=['15k+ downloads','80 Level feature','Community Godot tools']
        return '<div class="proof-links" aria-label="OpenVAT downloads, coverage and community">'+''.join(link(item['href'],label+' ↗') for item,label in zip(p.get('recognition',[]),labels))+'</div>'
    items=''.join(f'<a class="recognition-item" href="{esc(item["href"])}" target="_blank" rel="noopener noreferrer"><strong>{esc(item["value"])}</strong><span>{esc(item["label"])}</span><small>{esc(item["note"])}</small><span class="text-link">{esc(item["action"])} ↗</span></a>' for item in p.get('recognition',[]))
    return f'<div class="recognition" aria-label="OpenVAT reach and recognition">{items}</div>' if items else ''

def tool_card(key):
    p=PROJECTS[key]
    source=link('https://openvat.org/','OpenVAT.org ↗') if key=='openvat' else (link(p['links'][0]['href'],'GitHub ↗') if p.get('links') else '')
    return f'''<article class="tool-card"><a class="tool-image" href="{url(p)}"><img src="{esc(p['image'])}" alt="{esc(p['title'])} work preview" loading="lazy" width="640" height="400"></a><p class="card-status">{'Released extension' if key=='openvat' else 'In development'}</p><h3>{link(url(p),esc(p['title']))}</h3><p>{esc(p['description'])}</p><div class="tool-links">{link(url(p),'My work →')}{source}</div>{recognition(p,True) if key=='openvat' else ''}</article>'''

def plush_eye(navigation=True):
    destinations=('<nav class="peek-links" aria-label="PlushEngine project">'+link('plush.html','Why Plush?','button peek-link peek-about')+site_link('plush','download/','Download ↗','button peek-link peek-start')+'</nav>') if navigation else ''
    return f'''<div class="plush-peek" data-plush-peek>
<span class="peek-main" aria-hidden="true"><svg class="peek-eye" viewBox="-125 -75 250 150" aria-hidden="true" focusable="false">
<defs><clipPath id="portfolio-eye-open"><path data-eye-clip d="M-100 4C-52-62 46-66 100-6C50 44-46 42-100 4Z"/></clipPath></defs>
<g clip-path="url(#portfolio-eye-open)"><g data-eye-iris transform="translate(0 -10)"><circle class="peek-iris" r="27"/><circle class="peek-pupil" data-eye-pupil r="8"/></g></g>
<path class="peek-lid" data-eye-upper d="M-100 4C-52-62 46-66 100-6"/><path class="peek-lid" data-eye-lower d="M100-6C50 44-46 42-100 4"/></svg></span>
{destinations}</div>'''

def home_project_card(key):
    p=PROJECTS[key]
    summaries={
        'plush':('In development','My game engine, editor, and standalone runtime.',PROJECTS['plush']['storyHero']['src'],PROJECTS['plush']['storyHero']['alt']),
        'openvat':('Released Blender extension','Geometry Nodes animation, baked into textures for real-time playback.',p['image'],'OpenVAT vertex animation texture encoder'),
        'aether':('Materials & baking · Ongoing','My texture-baking and material tools, bringing xBake and TextureLab together.',p['image'],'Earlier xBake output, now part of Aether'),
        'attrio':('Released Blender extension',p['description'],p['image'],'Attrio CSV exporting evaluated Blender geometry and attributes')
    }
    category,description,image,alt=summaries[key]
    visual=link(url(p),f'<img src="{esc(image)}" alt="{esc(alt)}" width="960" height="540" loading="lazy">','project-card-visual')
    mark=''
    if key=='openvat':external=link('https://openvat.org/','OpenVAT.org ↗')
    elif key=='aether':external=link(p['links'][0]['href'],'GitHub ↗')
    elif key=='attrio':external=link(url(p),'Blender Extensions ↗')
    else:external=link(url(p),'About the project →')
    evidence=''
    if key=='openvat':
        labels=['15k+ downloads','80 Level feature','Community Godot tools']
        evidence='<div class="project-card-evidence">'+''.join(link(item['href'],esc(label)+' ↗') for item,label in zip(p['recognition'],labels))+'</div>'
    body=f'<p class="project-card-description">{esc(description)}</p>' if description else ''
    return f'''<article class="project-card" aria-labelledby="project-{esc(key)}-title">{visual}<div class="project-card-copy"><div class="project-card-heading"><h3 id="project-{esc(key)}-title">{link(url(p),esc(p['title']))}</h3>{mark}</div><p class="project-card-category">{esc(category)}</p>{body}<div class="project-card-links">{external}</div>{evidence}</div></article>'''


def devlog_preview(entry,root='',featured=False):
    href=root+'devlog/'+entry['slug']+'.html'
    return f'''<article class="devlog-preview{' devlog-feature' if featured else ''}"><a href="{esc(href)}"><img src="{root}{esc(entry['thumbnail'])}" alt="{esc(entry['thumbnailAlt'])}" width="180" height="180" loading="lazy"><div><p class="devlog-meta">From the devlog · <time datetime="{esc(entry['date'])}">{esc(entry['dateLabel'])}</time></p><h2>{esc(entry['title'])}</h2><p class="devlog-excerpt">{esc(entry['excerpt'])}</p><span class="text-link">Read the entry →</span></div></a></article>'''

def home_tool_card(key):
    p=PROJECTS[key]
    summary={
        'aether':('In development','Texture baking and material creation, bringing xBake and TextureLab together.','Earlier xBake material and baking work, now part of Aether'),
        'attrio':('Released Blender extension','Geometry and attributes ↔ CSV.','Attrio CSV exporting evaluated Blender geometry and attributes'),
        'sprite':('In development','Images, layers, and pixel-aligned scenes in Blender.','Earlier 2D Tools workflow, now developed as Sprite Toolkit')
    }
    status,description,alt=summary[key]
    visual=link(url(p),f'<img src="{esc(p["image"])}" alt="{esc(alt)}" width="640" height="360" loading="lazy">','tool-card-preview')
    if key=='aether': destinations=link(url(p),'About →')+link(p['links'][0]['href'],'GitHub ↗')
    elif key=='attrio': destinations=link(url(p),'Blender Extensions ↗')
    else: destinations=link(url(p),'About →')
    return f'''<article class="home-tool-card" aria-labelledby="tool-{key}-title">{visual}<div class="home-tool-card-body"><header><p class="project-card-category">{esc(status)}</p><h3 id="tool-{key}-title">{link(url(p),esc(p['title']))}</h3></header><p class="home-tool-card-description">{esc(description)}</p><nav class="home-tool-card-links" aria-label="{esc(p['title'])} links">{destinations}</nav></div></article>'''


def home_openvat_feature():
    p=PROJECTS['openvat']
    return f'''<article class="openvat-feature-card tool-openvat" aria-labelledby="tool-openvat-title"><a class="openvat-feature-art" href="{esc(url(p))}" aria-label="About OpenVAT"><img src="assets/tool-art/openvat-surface.png" alt="Colored vertices and wireframe deformation from OpenVAT" width="1600" height="900" loading="lazy"><span class="openvat-art-title">OpenVAT<span>Vertex Animation Toolkit</span></span></a><div class="openvat-feature-copy"><p class="project-card-category">Free & open source · Blender extension</p><h3 id="tool-openvat-title">OpenVAT</h3><p>{esc(p['description'])}</p><div class="openvat-stats">{link('https://extensions.blender.org/add-ons/openvat/','17,416 <span>downloads</span>')}{link('https://extensions.blender.org/add-ons/openvat/reviews/','5.0 / 5 <span>· 12 reviews ↗</span>')}</div><nav class="openvat-feature-links" aria-label="OpenVAT links">{link(url(p),'About the project →')}{site_link('openvat','','OpenVAT.org ↗')}{link('https://github.com/sharpen3d/openvat','GitHub ↗')}{link('https://github.com/sponsors/sharpen3d','Sponsor development ↗')}{link('https://youtube.com/playlist?list=PLxoaj1mvYohtaPyN0qmhTVHZJqLh8VTlt','Tutorials ↗')}</nav><p class="stats-note">Blender Extensions · November 5, 2026 snapshot.</p></div></article>'''



def tutorial_selection(root=''):
    cards=''
    for video in [v for v in TUTORIALS if v.get('featured')]:
        href='https://www.youtube.com/watch?v='+video['id']
        cards+=f'<article class="tutorial-pick"><a class="tutorial-thumbnail" href="{href}" target="_blank" rel="noopener noreferrer"><img src="https://i.ytimg.com/vi/{video["id"]}/hqdefault.jpg" alt="{esc(video["title"])} video thumbnail" loading="lazy" width="480" height="360"><span>Watch on YouTube ↗</span></a><p class="eyebrow">{esc(video["topic"])}</p><h3>{link(href,esc(video["title"]))}</h3><p>{esc(video["description"])}</p></article>'
    return '<section class="tutorial-selection" id="tutorials"><header class="index-heading"><h2>Tutorials & walkthroughs</h2>'+link(root+'tutorials.html','All tutorials →')+'</header><div class="tutorial-picks">'+cards+'</div></section>'

def tutorials_page():
    groups=[('fundamentals','Blender fundamentals','Datablocks, external files, and the system behind Geometry Nodes.'),('openvat','OpenVAT & engine workflows','Start with the overview, then follow the workflow into an engine or explore the experiments.'),('tools','Tools & materials','Walkthroughs for the Blender tools I’m building.'),('pipeline','Pipeline notes','Export, lightmapping, and the bits between Blender and an engine.')]
    order={'openvat':['eTBuDbZxwFg','cLP6ZKOyClM','NGniucSk4hU','T1KVvUIduGI','uZ4-0MxR3CU','xoLxKinzBwI'],'fundamentals':['_aracv2CA6o','RD7hQlBFZYs','uQ9egD4Wb1M']}
    jumps=''.join(link('#'+key,title+' <span>'+str(sum(v['group']==key for v in TUTORIALS))+'</span>','catalog-jump') for key,title,_ in groups)
    sections=''
    for key,title,intro in groups:
        videos=[v for v in TUTORIALS if v['group']==key]
        if key in order:videos.sort(key=lambda v:order[key].index(v['id']))
        cards=''
        for v in videos:
            href=v['source']
            resources=''.join(link(x['href'],esc(x['label'])+' ↗','resource-link') for x in v.get('resources',[]))
            resources='<nav class="catalog-resources" aria-label="Resources for '+esc(v['title'])+'">'+resources+'</nav>' if resources else ''
            chapters=''
            if v.get('chapters'):
                chapters='<details class="catalog-chapters"><summary>Video chapters</summary><ol>'+''.join('<li>'+link(href+'&t='+str(x['seconds']),'<span>'+esc(x['time'])+'</span> '+esc(x['title']))+'</li>' for x in v['chapters'])+'</ol></details>'
            cards+=f'<article class="catalog-card" id="video-{esc(v["id"])}"><a class="tutorial-thumbnail" href="{href}" target="_blank" rel="noopener noreferrer"><img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" alt="{esc(v["title"])} thumbnail" width="480" height="360" loading="lazy"><span>Watch on YouTube ↗</span></a><div class="catalog-copy"><h3>{link(href,esc(v["title"]))}</h3><p>{esc(v["description"])}</p>{resources}{chapters}</div></article>'
        sections+=f'<section class="catalog-group" id="{key}" aria-labelledby="{key}-title"><header><h2 id="{key}-title">{title}</h2><p>{intro}</p></header><div class="catalog-grid">{cards}</div></section>'
    body=f'<main id="main" class="tutorial-catalog wrap"><header class="catalog-heading"><p class="eyebrow">Blender · Tools · Real-time graphics</p><h1>Tutorials & walkthroughs</h1><p>I like figuring out how things work, why they work the way they do, and whether there’s a better way to do them.</p><p class="catalog-subtitle">Longer explanations, practical workflows, and experiments. Project files, source code, and downloads are linked alongside the videos that use them.</p>{link("https://www.youtube.com/@LukeStilson","Follow along on YouTube ↗","button")}</header><nav class="catalog-jumps" aria-label="Tutorial topics">{jumps}</nav>{sections}<section class="catalog-end"><h2>More of the process</h2><p>Shorter tests and work in progress are in the dev log and on Instagram.</p>{link("devlog/index.html","Experiments & Dev Log →")}{link("https://www.instagram.com/3d_luke/","Instagram ↗")}{link("https://github.com/sponsors/sharpen3d","Support my open-source work ↗")}</section></main>'
    (ROOT/'tutorials.html').write_text(page('Tutorials & walkthroughs','Blender tutorials, OpenVAT engine workflows, tools, and source files by Luke Stilson.',body,active='Tutorials'))

def home():
    work=''.join(home_tool_card(key) for key in ['aether','attrio','sprite'])
    latest=''.join(devlog_preview(entry) for entry in DEVLOG[2:4])
    recent_card='<div class="featured-devlog-entries">'+''.join('<a class="recent-note" href="devlog/'+esc(entry['slug'])+'.html"><img src="'+esc(entry['thumbnail'])+'" alt="'+esc(entry['thumbnailAlt'])+'" width="160" height="100" loading="lazy"><div><p class="eyebrow">From the dev log</p><h2>'+esc(entry['title'])+'</h2><p>'+esc(entry['excerpt'])+'</p><span class="text-link">Read the entry →</span></div></a>' for entry in DEVLOG[:2])+'</div>'
    body=f'''<main id="main">
<section class="home-opening home-showcase wrap" id="work" aria-labelledby="home-title"><header class="home-welcome"><div><p class="eyebrow">Luke Stilson · Technical artist</p><h1 id="home-title">Technical art & tools</h1><p>I’ve spent most of my career making tools that help other people make things. Most of what’s here is personal work: my own tools, games, and experiments.</p><a class="welcome-studio" href="studio-work.html">For my professional roles, see Studio Work →</a></div><nav class="welcome-links" aria-label="Tutorials and social profiles">{link('tutorials.html','Tutorials & walkthroughs <span aria-hidden="true">→</span>','welcome-tutorials')}{link('https://www.youtube.com/@LukeStilson','YouTube ↗','welcome-social')}{link('https://www.instagram.com/3d_luke/','Instagram ↗','welcome-social')}{link('https://github.com/sharpen3d','GitHub ↗','welcome-social')}</nav></header><article class="plush-spotlight"><figure class="spotlight-footage spotlight-still"><a href="plush.html" aria-label="Explore PlushEngine"><img src="assets/plush-materials-home.jpg" alt="Fur, fabric, and reflective material tests rendered in PlushEngine" width="1100" height="550" fetchpriority="high"></a><figcaption>Material tests · Rendered in PlushEngine</figcaption></figure><div class="spotlight-copy"><img class="spotlight-logo" src="assets/plush-logo.png" alt="" width="64" height="64"><p class="eyebrow">My game engine · In development</p><h2>PlushEngine</h2><p>A game engine I can keep building on.</p><p class="spotlight-detail">C# gameplay, a shared data model, and an editor I can change when something gets in the way.</p><nav aria-label="PlushEngine links">{link('plush.html','Explore Plush →','button')}{site_link('plush','download/','Download ↗')}</nav></div></article><div class="showcase-latest"><div class="devlog-introduction"><h2>Experiments & Dev Log</h2><p>Tests, prototypes, and notes from whatever I’m working on. What I tried, what worked, and what I’m still figuring out.</p></div>{recent_card}{link('devlog/index.html','All experiments →','latest-all')}</div></section>
<section class="home-tools wrap" aria-labelledby="tools-title"><header class="index-heading"><h2 id="tools-title">Blender tools</h2></header>{home_openvat_feature()}<div class="home-tool-card-grid">{work}</div></section>
<div class="wrap">{tutorial_selection()}</div>
<section class="home-experiments wrap" aria-labelledby="experiments-title"><header class="index-heading"><h2 id="experiments-title">Experiments &amp; Dev Log</h2>{link('devlog/index.html','All entries →')}</header>{latest}</section>
<nav class="collection-links studio-link wrap" aria-label="Studio work"><a href="studio-work.html"><span>Studio work</span><span aria-hidden="true">↗</span></a></nav>
<section class="personal-note wrap" id="about" aria-labelledby="about-title"><h2 id="about-title">About</h2><div><p>I've spent most of my career making tools that help other people make things.</p><p>I like figuring out how things work, why they work the way they do, and whether there's a better way to do them.</p>{link('https://www.youtube.com/@LukeStilson','Tutorials and experiments on YouTube ↗')}</div></section>
<section class="support-note wrap"><div><h2>Open-source work</h2><p>If one of my tools has been useful to you, you can support the work on GitHub.</p></div>{link("https://github.com/sponsors/sharpen3d","Support my open-source work ↗")}</section>
<section class="contact-line wrap" id="contact" aria-label="Contact">{link('mailto:'+EMAIL,EMAIL+' ↗','contact-address')}{link('https://www.linkedin.com/in/luke-stilson/','LinkedIn ↗')}</section></main>'''
    (ROOT/'index.html').write_text(page('Technical Art & Tools','Luke Stilson: technical artist and tools designer. PlushEngine, OpenVAT, production pipelines, rendering, and independent experiments.',body,body_class='home portfolio-home'))


def video_markup(p,root):
    poster=p.get('videoPoster',p['image'])
    return f'<video controls playsinline preload="none" poster="{root}{esc(poster)}" width="1280" height="720" aria-label="{esc(p["title"])} demonstration"><source src="{root}{esc(p["videoSrc"])}" type="video/mp4"><a href="{root}{esc(p["videoSrc"])}">Open the demonstration video</a></video>'

def media(p,root):
    caption=esc(p.get('mediaCaption',p['title']+' · '+p['context']))
    image_alt=esc(p.get('imageAlt',p['title']+' project overview'))
    if p.get('videoSrc'):
        notes='<details class="reel-notes"><summary>What’s in the reel</summary><ol>'+''.join(f'<li><span>{esc(x["time"])}</span> {esc(x["text"])}</li>' for x in p['videoTranscript'])+'</ol></details>' if p.get('videoTranscript') else ''
        return f'<figure class="project-hero">{video_markup(p,root)}<figcaption>{caption}</figcaption></figure>{notes}'
    return f'<figure class="project-hero"><img src="{root}{esc(p["image"])}" alt="{image_alt}" width="1440" height="810"><figcaption>{caption}</figcaption></figure>'

def plush_case(p):
    feature=json.loads((ROOT/'content/plush-feature.json').read_text())
    hero=p['storyHero']
    paragraphs=''.join('<p>'+esc(text)+'</p>' for text in feature['dataParagraphs'])
    stack=''.join('<div><dt>'+esc(label)+'</dt><dd>'+esc(value)+'</dd></div>' for label,value in feature['stack'])
    extras=''.join('<section><h2>'+esc(title)+'</h2><p>'+esc(text)+'</p></section>' for title,text in feature['extras'])
    body=f'''<main id="main" class="plush-brief wrap"><a class="back-link" href="index.html#work">← Back to the portfolio</a><header class="plush-brief-heading"><p class="eyebrow">My game engine · In development</p><h1>PlushEngine</h1><p>{esc(feature['intro'])}</p><nav class="brief-actions" aria-label="PlushEngine links">{site_link('plush','download/','Download ↗','button')}{site_link('plush','about/','Why I’m making Plush →')}</nav></header><figure class="brief-hero"><a href="assets/plush-editor.jpg"><img src="{esc(hero['src'])}" alt="{esc(hero['alt'])}" width="1150" height="450"></a><figcaption>A scene, its reusable objects, and the connections between them.</figcaption></figure><section class="brief-data" id="project-data"><div><p class="eyebrow">The data model</p><h2>{esc(feature['dataTitle'])}</h2>{paragraphs}</div><figure><a href="assets/plush-editor.jpg"><img src="assets/plush-data-detail.jpg" alt="Shared meshes, materials, and scripts connected in the Plush data graph" width="1098" height="684" loading="lazy"></a><figcaption>The relationships are part of the editor.</figcaption></figure></section><section class="brief-stack" id="engine-stack"><div><p class="eyebrow">The engine stack</p><h2>What’s underneath</h2><p>{esc(feature['stackIntro'])}</p></div><dl>{stack}</dl></section><div class="brief-extras">{extras}</div><footer class="brief-end"><p>{esc(feature['closing'])}</p>{link('devlog/index.html','Experiments & Dev Log →')}{site_link('plush','about/','More about Plush →')}</footer></main>'''
    (ROOT/'plush.html').write_text(page(p['title'],feature['intro'],body,active='Work',body_class='project-page plush-story'))


def openvat_case(p):
    feature=json.loads((ROOT/'content/openvat-feature.json').read_text())
    video=next(v for v in TUTORIALS if v['id']==feature['videoId'])
    watch='https://www.youtube.com/watch?v='+video['id']
    chapters=''.join(link(watch+'&t='+str(seconds)+'s',label+' ↗') for seconds,label in [(95,'What a VAT stores'),(581,'Use cases'),(1099,'Decoding in a shader')])
    features=''.join('<section><h2>'+esc(title)+'</h2><p>'+esc(text)+'</p></section>' for title,text in feature['features'])
    workflow=''.join('<div><span>'+number+'</span><h2>'+title+'</h2><p>'+text+'</p></div>' for number,title,text in [('01','Animate','Use the Blender tools you already work with.'),('02','Encode','Bake the evaluated deformation into textures.'),('03','Deploy','Read the textures in an engine’s vertex shader.')])
    body=f'''<main id="main" class="plush-brief openvat-brief wrap"><a class="back-link" href="../index.html#work">← Back to the portfolio</a>
<header class="plush-brief-heading"><p class="eyebrow">My Blender tools · Free & open source</p><h1>OpenVAT</h1><p>{esc(feature['intro'])}</p><nav class="brief-actions" aria-label="OpenVAT links">{link('https://extensions.blender.org/add-ons/openvat/','Get OpenVAT ↗','button')}{site_link('openvat','','OpenVAT.org ↗')}{link('https://github.com/sharpen3d/openvat','Source code ↗')}{link('https://github.com/sharpen3d/openvat/commits/main/','Latest development ↗')}</nav></header>
<div class="vat-workflow" aria-label="OpenVAT workflow">{workflow}</div>
<section class="brief-data vat-origami"><div><p class="eyebrow">Vertex animation textures</p><h2>{esc(feature['origamiTitle'])}</h2><p>{esc(feature['origamiText'])}</p><p>{esc(feature['origamiNote'])}</p></div><figure class="origami-media"><video controls muted playsinline preload="none" poster="../assets/openvat-origami-poster.jpg" width="405" height="720" aria-label="Origami folding shown as a vertex animation texture, vertex offsets, and the final mesh"><source src="../assets/openvat-origami.mp4" type="video/mp4"></video><figcaption>Texture data → vertex offsets → the folding mesh.</figcaption></figure></section>
<section class="brief-data vat-explainer"><figure><a class="vat-video-link" href="{watch}" aria-label="Watch {esc(video['title'])}"><img src="https://i.ytimg.com/vi/{video['id']}/hqdefault.jpg" alt="{esc(video['title'])}" width="480" height="360" loading="lazy"><span>Watch the explanation on YouTube ↗</span></a><figcaption>{esc(video['title'])}</figcaption></figure><div><p class="eyebrow">The idea behind it</p><h2>How vertex animation textures work</h2><p>{esc(feature['explainer'])}</p><p>I walk through the format, the encoding, and the shader side in this video, with examples of what you can do with the result.</p><nav class="vat-chapters" aria-label="Video chapters">{chapters}</nav></div></section>
<div class="brief-extras vat-features">{features}</div>
<section class="brief-stack vat-project"><div><p class="eyebrow">My part in it</p><h2>From Blender to the engine</h2><p>{esc(feature['work'])}</p></div><div class="vat-engine-notes"><h3>Engine examples</h3><p>Unity and Unreal integrations, GLSL templates, and a separate community Godot integration by AntzGames.</p><nav>{site_link('openvat','#engines','Integrations & setup →')}{link('https://github.com/antzGames/OpenVAT-for-Godot','Community Godot project ↗')}</nav><h3>One constraint to know</h3><p>{esc(feature['limit'])}</p></div></section>
{recognition(p)}
<footer class="brief-end"><p>The extension is free and open source. The OpenVAT site has the technical details, engine setup, and documentation; my YouTube channel has the walkthroughs.</p><nav class="brief-actions" aria-label="Explore OpenVAT">{site_link('openvat','','OpenVAT.org ↗','button')}{link('../tutorials.html#openvat','More OpenVAT tutorials →')}{link('https://github.com/sharpen3d/openvat','GitHub ↗')}</nav></footer></main>'''
    (ROOT/url(p)).write_text(page('OpenVAT',feature['intro'],body,'../',active='Work',body_class='project-page openvat-story'))


def case(p):
    if p["id"] == "openvat":
        openvat_case(p)
        return
    if p.get("presentation")=="feature-story":
        plush_case(p)
        return
    path=url(p); root='../' if '/' in path else ''
    actions=''.join(link(root+x['href'] if not x['href'].startswith(('https:','mailto:')) else x['href'],esc(x['label'])+' ↗','button') for x in p.get('links',[]))
    gallery=''
    for number,im in enumerate(p.get('images',[]),1):
        caption=im.get('caption') or f'{p["title"]} · Detail {number}'
        src=root+im['src']
        if src.lower().endswith(('.mp4','.webm')):
            poster=f' poster="{root}{esc(im["poster"])}"' if im.get('poster') else ''
            item=f'<video controls playsinline preload="none"{poster} aria-label="{esc(caption)}"><source src="{esc(src)}" type="video/mp4"></video>'
        else:
            item=f'<a href="{esc(src)}" aria-label="Open full-size image: {esc(caption)}"><img loading="lazy" src="{esc(src)}" alt="{esc(caption)}"></a>'
        gallery+=f'<figure>{item}<figcaption>{esc(caption)}</figcaption></figure>'
    gallery_block=('<section class="editor-views"><div class="plain-heading"><h2>Editor views</h2><p>Open an image for a closer look.</p></div><div class="gallery">'+gallery+'</div></section>') if gallery and p.get('galleryBeforeNotes') else ('<section class="gallery" aria-label="Project gallery">'+gallery+'</section>' if gallery else '')
    sections=''
    for section in p.get('sections',[]):
        anchor=f' id="{esc(section["id"])}"' if section.get('id') else ''
        paragraphs=''.join(f'<p>{esc(text)}</p>' for text in (section.get('paragraphs') or [section['text']]))
        sections+=f'<section{anchor}><h2>{esc(section["title"])}</h2>{paragraphs}</section>'
    notes=f'<div class="case-content"><aside><p class="eyebrow">Project notes</p><p>{esc(NAMES[p["category"]])}</p></aside><article>{sections}<div class="actions">{actions}</div></article></div>'
    body=f'''<main id="main" class="case-page wrap"><a class="back-link" href="{root}index.html#work">← Back to the work</a><header class="case-heading"><p class="eyebrow">{esc(p['label'])}</p><h1>{esc(p['title'])}</h1><p class="case-description">{esc(p['description'])}</p></header><dl class="project-facts"><div><dt>My role</dt><dd>{esc(p['role'])}</dd></div><div><dt>Tools & context</dt><dd>{esc(p['tools'])}</dd></div><div><dt>Project</dt><dd>{esc(p['context'])}</dd></div></dl>{media(p,root)}{recognition(p)}{gallery_block if p.get("galleryBeforeNotes") else ""}{notes}{gallery_block if not p.get("galleryBeforeNotes") else ""}<div class="case-end">{link(root+'index.html#work','← Explore more work','button')}{link('mailto:'+EMAIL,'Get in touch ↗')}</div></main>'''
    target=ROOT/path; target.parent.mkdir(exist_ok=True)
    target.write_text(page(p['title'],p['description'],body,root,active='Work',body_class='project-page'))

def document_page(name,title,intro,content,action=''):
    body=f'<main id="main" class="document-page wrap"><a class="back-link" href="index.html">← Back to the portfolio</a><p class="eyebrow">Archive · 2024</p><h1>{esc(title)}</h1><p class="document-intro">{esc(intro)}</p>{action}<article class="document-content">{content}</article></main>'
    (ROOT/name).write_text(page(title,intro,body,active='Résumé' if name=='resume.html' else 'Work'))

def resume_page():
    roles=''.join('<section class="resume-job"><div class="resume-job-heading"><h3>'+esc(job['company'])+'</h3><span>'+esc(job['dates'])+'</span></div><p class="resume-job-title">'+esc(job['title'])+'</p><ul>'+''.join('<li>'+esc(item)+'</li>' for item in job['bullets'])+'</ul></section>' for job in RESUME['experience'])
    projects=''.join('<section class="resume-job"><h3>'+esc(item['title'])+'</h3><p class="resume-job-title">'+esc(item['role'])+'</p><ul>'+''.join('<li>'+esc(bullet)+'</li>' for bullet in item['bullets'])+'</ul></section>' for item in RESUME['projects'])
    capabilities=''.join('<li>'+esc(skill)+'</li>' for skill in RESUME['skills'])
    body=f'''<main id="main" class="document-page resume-page wrap"><a class="back-link" href="index.html">← Back to the portfolio</a><p class="eyebrow">Résumé · {RESUME['year']}</p><h1>{esc(RESUME['name'])}</h1><p class="resume-role">{esc(RESUME['title'])}</p><p class="resume-contact">{esc(RESUME['location'])} · {link('mailto:'+EMAIL,EMAIL)} · {esc(RESUME['phone'])}</p><div class="actions">{link(RESUME['download'],'Download résumé (Word) ↓','button')}<button class="button print-resume" type="button" hidden>Print / Save PDF</button></div><article class="document-content"><section class="resume-section"><h2>Profile</h2><p>{esc(RESUME['profile'])}</p></section><section class="resume-section"><h2>Core capabilities</h2><ul class="capabilities">{capabilities}</ul></section><section class="resume-section"><h2>Professional experience</h2>{roles}<p class="resume-earlier">Earlier experience: {esc(RESUME['earlier'])}</p></section><section class="resume-section"><h2>Selected independent projects</h2>{projects}</section><section class="resume-section"><h2>Education</h2><p>{esc(RESUME['education'])}</p></section></article></main>'''
    (ROOT/'resume.html').write_text(page('Résumé',RESUME['profile'],body,active='Résumé'))


def image_figure(src,caption,root=''):
    return f'<figure><a href="{root}{esc(src)}"><img loading="lazy" src="{root}{esc(src)}" alt="{esc(caption)}"></a><figcaption>{esc(caption)}</figcaption></figure>'

def studio_page():
    entries=json.loads((ROOT/'content/studio.json').read_text())
    roles={job['company']:job for job in RESUME['experience']}
    sections=''
    for entry in entries:
        role=roles[entry['company']]
        paragraphs=''.join('<p>'+esc(text)+'</p>' for text in entry['paragraphs'])
        sections+=f'<section class="studio-entry studio-role" id="{esc(entry["id"])}"><header><h2>{esc(entry["company"])}</h2><p>{esc(role["title"])}<br>{esc(role["dates"])}</p>{link(entry["website"],"Company website ↗","studio-company-link")}</header><div class="studio-entry-copy">{paragraphs}</div></section>'
    body=f'<main id="main" class="collection-page studio-work-page wrap"><a class="back-link" href="index.html#work">← Back to the portfolio</a><header class="case-heading"><p class="eyebrow">Teams I’ve worked with</p><h1>Studio work</h1><p class="case-description">I’ve usually been the person figuring out how to make things work. That’s taken me from modeling, texturing, and rigging into AR, VR, games, and visualization in Unity and Unreal, and into designing the tools and pipelines that connect it all.</p></header>{sections}<p class="studio-context">Studio projects are team efforts; these descriptions focus on my contribution. My independent tools and experiments are presented separately.</p><div class="case-end">{link("index.html#work","← Back to the portfolio","button")}{link("resume.html","Full résumé →")}</div></main>'
    (ROOT/'studio-work.html').write_text(page('Studio work','Technical art, tools, and production work by Luke Stilson.',body,active='Work'))


def study_entry(key,anchor):
    p=PROJECTS[key]
    text={
      'railway':'I built this environment in a week, creating the models and materials with Maya, Substance Designer, Substance Painter, and Blender, then assembling and lighting the scene in Unreal Engine 4.',
      'audiovisualizer':'I used audio measurements and Blender drivers to change a Geometry Nodes system. Blender has its own sound input now; this was an earlier experiment in connecting pitch and frequency to procedural motion.',
      'minesweeperRemastered':'An independent first-person Minesweeper concept in Unreal. I worked on the game concept, environment, materials, and gameplay, exploring a physical grid and a handheld display.',
      'blink':'A freerunning combat prototype in Unreal Engine 4. I worked on the level design and Blueprint systems, with a multipurpose device for grappling, combat, and traversal.',
      'hexscapes':'A puzzle prototype about changing neighboring islands on a hexagonal board. I explored it in Unreal, then rebuilt it in Unity to work through recursive solving, data, and generated boards in C#.',
      'die':'A gameplay experiment with dice as characters, where their numbers affect the odds of an encounter. I worked on the game design, behavior, physics interactions, and presentation.'
    }[key]
    gallery=''
    keep=p.get('images',[])[:3 if key=='railway' else 2]
    if keep:
        gallery='<details class="more-work"><summary>More images</summary><div class="study-gallery">'+''.join(image_figure(im['src'],im.get('caption') or p['title']+' study') for im in keep)+'</div></details>'
    notes=link('minesweeper-notes.html','Original concept notes (2024) →') if key=='minesweeperRemastered' else ''
    return f'<article class="study-entry" id="{anchor}"><div class="study-entry-heading"><h3>{esc(p["title"])}</h3><p>{esc(p["role"])}</p></div>{media(p,"")}<p class="study-description">{esc(text)}</p>{notes}{gallery}</article>'

def studies_page():
    games=''.join(study_entry(key,anchor) for key,anchor in [('minesweeperRemastered','minesweeper'),('blink','blink'),('hexscapes','hexscapes'),('die','dice')])
    effects=PROJECTS['bpxemitters']
    body=f'''<main id="main" class="collection-page wrap"><a class="back-link" href="index.html#work">← Back to the portfolio</a><header class="case-heading"><h1>Experiments</h1><p class="case-description">Environments, game prototypes, and smaller studies with sound and procedural animation. Personal work I still like, gathered in one place.</p></header><nav class="collection-nav" aria-label="Experiment categories">{link('#audio','Sound & animation ↓')}{link('#environment','Environment art ↓')}{link('#games','Game prototypes ↓')}</nav><section class="study-group" id="audio"><h2>Sound & procedural animation</h2>{study_entry('audiovisualizer','audio-geometry')}<article class="study-entry" id="effects"><div class="study-entry-heading"><h3>Procedural effects</h3><p>Geometry Nodes, Python, and sprite output</p></div>{media(effects,'')}<p class="study-description">An earlier Blender tool for particle effects and sprite sequences. I built the Python controls and editable node groups for spawning, motion, scale, rotation, color, and looping output. I’m showing it here as a procedural study; it isn’t a current extension release.</p></article></section><section class="study-group" id="environment"><h2>Environment art</h2>{study_entry('railway','railway')}</section><section class="study-group" id="games"><h2>Game prototypes</h2><div class="game-study-grid">{games}</div></section><div class="case-end">{link('index.html#work','← Back to the portfolio','button')}{link('mailto:'+EMAIL,'Email ↗')}</div></main>'''
    (ROOT/'studies.html').write_text(page('Experiments','Personal work by Luke Stilson: environment art, materials, game prototypes, audio-driven Geometry Nodes, and procedural effects.',body,active='Work'))

def redirect_page(path,target,title):
    root='../' if '/' in path else ''
    href=root+target
    body=f'<main id="main" class="document-page wrap"><h1>{esc(title)}</h1><p class="document-intro">This work is now part of a consolidated project page.</p>{link(href,"Continue to the project →","button")}</main>'
    output=page(title,title,body,root)
    output=output.replace('</head>',f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={esc(href)}"><link rel="canonical" href="{esc(href)}"></head>')
    destination=ROOT/path;destination.parent.mkdir(exist_ok=True);destination.write_text(output)

def legacy_pages():
    aliases={'xbake':('aether.html','Aether'),'textureLab':('aether.html','Aether'),'Pixels':('sprite-toolkit.html','Sprite Toolkit'),'zfo':('studio-work.html#onchain','OnChain Studios'),'unboxing':('studio-work.html#onchain','OnChain Studios'),'egaming':('studio-work.html#arrow','Arrow International'),'hellomoto':('studio-work.html#earlier','Earlier client work'),'stackattack':('studio-work.html#earlier','Earlier client work'),'railway':('studies.html#railway','Abandoned Railway'),'audiovisualizer':('studies.html#audio-geometry','Audio & Geometry'),'bpxemitters':('studies.html#effects','Procedural effects'),'minesweeperRemastered':('studies.html#minesweeper','Minesweeper'),'blink':('studies.html#blink','BLiNK'),'hexscapes':('studies.html#hexscapes','HexScapes'),'die':('studies.html#dice','Die!')}
    for key,(target,title) in aliases.items():redirect_page(url(PROJECTS[key]),target,title)
    for key in ['rendercontroller','filemanager','terminallauncher','blenderndo']:
        p=dict(PROJECTS[key]);p['links']=[];p['context']='Archive · Earlier tool';p['label']='Archived project';p['description']='Earlier Blender tool. This is retained for old links; it is not a currently maintained release. '+p['description']
        case(p)
        path=ROOT/url(p);s=path.read_text().replace('</head>','<meta name="robots" content="noindex"></head>');path.write_text(s)

def devlog_figure(figure):
    return f'''<figure class="devlog-figure{' devlog-portrait' if figure.get('layout')=='portrait' else ''}"><a href="../{esc(figure['src'])}" aria-label="Open full-size image: {esc(figure['alt'])}"><img src="../{esc(figure['src'])}" alt="{esc(figure['alt'])}" loading="lazy"></a><figcaption>{esc(figure['caption'])} {link(figure['source'],'Original post ↗') if figure.get('source') else ''}</figcaption></figure>'''

def devlog_pages():
    folder=ROOT/'devlog';folder.mkdir(exist_ok=True)
    cards=''.join(devlog_preview(entry,'../') for entry in DEVLOG)
    body=f'''<main id="main" class="document-page devlog-index wrap"><a class="back-link" href="../index.html">← Back to the portfolio</a><header class="case-heading"><h1>Experiments &amp; Dev Log</h1><p class="case-description">Notes from whatever I’m working on.</p></header><div class="devlog-entries">{cards}</div>{tutorial_selection("../")}<nav class="social-follow" aria-label="More experiments">{link("https://www.instagram.com/3d_luke/","Short experiments on Instagram ↗")}{link("https://www.youtube.com/@LukeStilson","YouTube ↗")}</nav></main>'''
    (folder/'index.html').write_text(page('Experiments & Dev Log','Notes on tools, rendering, animation, and games by Luke Stilson.',body,'../',active='Work'))
    for entry in DEVLOG:
        sections=''
        for section in entry['sections']:
            paragraphs=''.join(f'<p>{esc(paragraph)}</p>' for paragraph in section['paragraphs'])
            figure=devlog_figure(section['figure']) if section.get('figure') else ''
            clip=section.get('video')
            video=f'<video class="devlog-video" controls playsinline preload="none" poster="../{esc(clip["poster"])}"><source src="../{esc(clip["src"])}" type="video/mp4"></video>' if clip else ''
            source=link(section['source'],'Original post ↗') if section.get('source') else ''
            sections+=f'<section><h2>{esc(section["title"])}</h2>{paragraphs}{figure}{video}{source}</section>'
        body=f'''<main id="main" class="devlog-article wrap"><a class="back-link" href="index.html">← Experiments &amp; Dev Log</a><article><header class="devlog-heading"><p class="devlog-meta">Research notes · <time datetime="{esc(entry['date'])}">{esc(entry['dateLabel'])}</time> · {esc(entry['category'])}</p><h1>{esc(entry['title'])}</h1><p class="devlog-lede">{esc(entry['lede'])}</p><p class="devlog-origin">{esc(entry['sourceLabel'])} {link(entry['source'],'Read the thread ↗') if entry.get('source') else ''}</p></header>{devlog_figure(entry['hero'])}<div class="devlog-prose">{sections}</div><footer class="devlog-end">{link(entry['source'],'Original discussion on BlenderArtists ↗') if entry.get('source') else ''}{link('index.html','All devlog entries →')}</footer></article></main>'''
        (folder/(entry['slug']+'.html')).write_text(page(entry['title'],entry['lede'],body,'../',active='Work'))
    redirect_page('plush-devlog.html','devlog/index.html','Experiments & Dev Log')

def main():
    tutorials_page()
    home()
    devlog_pages()
    for p in PROJECTS.values():
        if p.get('published'): case(p)
    studio_page()
    studies_page()
    legacy_pages()
    resume_page()
    document_page('minesweeper-notes.html','Minesweeper: original concept notes','Original 2024 design notes for an independent concept. These describe ideas and plans, rather than features of a released game.',ARCHIVED['minesweeper'])
    print('Built portfolio: PlushEngine, three Blender tools, studio work, experiments, résumé, and legacy links.')
if __name__=='__main__':main()
