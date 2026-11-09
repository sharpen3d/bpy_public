#!/usr/bin/env python3
"""Build the static portfolio. Edit content/projects.json and assets/portfolio.css; no dependencies required."""
from pathlib import Path
from site_credit import author_footer
import html
import json
from datetime import date
from sync_aether_gallery import sync_gallery, sync_variations, sync_grass_comparison

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
        'aether':('Geometry-first materials · Ongoing','Editable surface construction for seamless textures, trim sheets, decals, and props.',p['image'],'Earlier xBake camera: source geometry, baked normal map, and textured result'),
        'attrio':('Released Blender extension',p['description'],p['image'],'Attrio CSV exporting evaluated Blender geometry and attributes')
    }
    category,description,image,alt=summaries[key]
    visual=link(url(p),f'<img src="{esc(image)}" alt="{esc(alt)}" width="960" height="540" loading="lazy">','project-card-visual')
    mark=''
    if key=='openvat':external=link('https://openvat.org/','OpenVAT.org ↗')
    elif key=='aether':external=link(p['links'][0]['href'],'Legacy Aether GitHub ↗')
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
        'aether':('Active development','Geometry-first material authoring for seamless surfaces, trim sheets, decals, and props.','Earlier xBake camera: source geometry, baked normal map, and textured result'),
        'attrio':('Released Blender extension','Geometry and attributes ↔ CSV.','Attrio CSV exporting evaluated Blender geometry and attributes'),
        'sprite':('In development','Images, layers, and pixel-aligned scenes in Blender.','Earlier 2D Tools workflow, now developed as Sprite Toolkit')
    }
    status,description,alt=summary[key]
    visual=link(url(p),f'<img src="{esc(p["image"])}" alt="{esc(alt)}" width="640" height="360" loading="lazy">','tool-card-preview')
    if key=='aether': destinations=link(url(p),'About →')+link(p['links'][0]['href'],'Legacy Aether GitHub ↗')
    elif key=='attrio': destinations=link(url(p),'Blender Extensions ↗')
    else: destinations=link(url(p),'About →')
    return f'''<article class="home-tool-card" aria-labelledby="tool-{key}-title">{visual}<div class="home-tool-card-body"><header><p class="project-card-category">{esc(status)}</p><h3 id="tool-{key}-title">{link(url(p),esc(p['title']))}</h3></header><p class="home-tool-card-description">{esc(description)}</p><nav class="home-tool-card-links" aria-label="{esc(p['title'])} links">{destinations}</nav></div></article>'''


def home_openvat_feature():
    p=PROJECTS['openvat']
    return f'''<article class="openvat-feature-card tool-openvat" aria-labelledby="tool-openvat-title"><a class="openvat-feature-art" href="{esc(url(p))}" aria-label="About OpenVAT"><img src="assets/tool-art/openvat-surface.png" alt="Colored vertices and wireframe deformation from OpenVAT" width="1600" height="900" loading="lazy"><span class="openvat-art-title">OpenVAT<span>Vertex Animation Toolkit</span></span></a><div class="openvat-feature-copy"><p class="project-card-category">Free & open source · Blender + Unity</p><h3 id="tool-openvat-title">OpenVAT</h3><p>{esc(p['description'])}</p><div class="openvat-stats">{link('https://extensions.blender.org/add-ons/openvat/','17,416 <span>downloads</span>')}{link('https://extensions.blender.org/add-ons/openvat/reviews/','5.0 / 5 <span>· 12 reviews ↗</span>')}</div><nav class="openvat-feature-links" aria-label="OpenVAT links">{link(url(p),'About the project →')}{site_link('openvat','','OpenVAT.org ↗')}{link('https://github.com/sharpen3d/openvat','GitHub ↗')}{link('https://github.com/sponsors/sharpen3d','Sponsor development ↗')}{link('https://youtube.com/playlist?list=PLxoaj1mvYohtaPyN0qmhTVHZJqLh8VTlt','Tutorials ↗')}</nav><p class="stats-note">Blender Extensions · November 5, 2026 snapshot.</p></div></article>'''



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
<section class="home-tools wrap" aria-labelledby="tools-title"><header class="index-heading"><h2 id="tools-title">Tools &amp; workflows</h2></header>{home_openvat_feature()}<h3 class="more-tools-heading">More Blender tools</h3><div class="home-tool-card-grid">{work}</div></section>
<div class="wrap">{tutorial_selection()}</div>
<section class="home-experiments wrap" aria-labelledby="experiments-title"><header class="index-heading"><h2 id="experiments-title">Experiments &amp; Dev Log</h2>{link('devlog/index.html','All entries →')}</header>{latest}</section>
<section class="home-games wrap" id="games" aria-labelledby="games-title"><header class="index-heading"><div><p class="eyebrow">Personal projects</p><h2 id="games-title">Prototypes</h2><p class="games-intro">Three personal projects, each built around a different question: what can I add, how do I keep it focused, and what does a much bigger game actually take?</p></div></header><div class="home-games-grid">
<article class="home-game-card"><a class="home-game-image" href="vspx.html"><img src="assets/games/vspx-combat.jpg" alt="A VSPX combat test with characters and minions" loading="lazy"></a><div class="home-game-copy"><p class="game-engine"><img src="assets/games/unity.svg" alt=""><span>Unity · Personal project</span></p><h3><a href="vspx.html">VSPX</a></h3><p>A deliberately oversized MOBA-inspired project about reusable systems, character abilities, bot AI, and what it takes to make them work together.</p>{link('vspx.html','Explore the project →')}</div></article>
<article class="home-game-card"><a class="home-game-image" href="mine-over-matter.html"><img src="assets/games/mine-over-matter.jpg" alt="A handheld mine detector overlooking a minefield" loading="lazy"></a><div class="home-game-copy"><p class="game-engine"><img src="assets/games/unreal.svg" alt=""><span>Unreal Engine · Prototype</span></p><h3><a href="mine-over-matter.html">Mine Over Matter</a></h3><p>A focused first-person Minesweeper prototype and an exploration of puzzle generation, solvability, and the move from UE4 to UE5.</p>{link('mine-over-matter.html','Explore the project →')}</div></article>
<article class="home-game-card"><a class="home-game-image" href="blink.html"><img src="assets/games/blink.jpg" alt="A scene from the BLiNK game prototype" loading="lazy"></a><div class="home-game-copy"><p class="game-engine"><img src="assets/games/unreal.svg" alt=""><span>Unreal Engine · Experimental release</span></p><h3><a href="blink.html">BLiNK</a></h3><p>An early UE4 Blueprint project where I kept adding things: weapons, abilities, grappling, and ways to move through a first-person game.</p>{link('blink.html','Explore the project →')}</div></article></div><p class="earlier-link"><a href="earlier-work.html">Earlier art and animation →</a></p></section>
<nav class="collection-links studio-link wrap" aria-label="Studio work"><a href="studio-work.html"><span>Studio work</span><span aria-hidden="true">↗</span></a></nav>
<section class="personal-note wrap" id="about" aria-labelledby="about-title"><h2 id="about-title">About</h2><div><p>I've spent most of my career making tools that help other people make things.</p><p>I like figuring out how things work, why they work the way they do, and whether there's a better way to do them.</p>{link('https://www.youtube.com/@LukeStilson','Tutorials and experiments on YouTube ↗')}</div></section>
<section class="support-note wrap"><div><h2>Open-source work</h2><p>If one of my tools has been useful to you, you can support the work on GitHub.</p></div>{link("https://github.com/sponsors/sharpen3d","Support my open-source work ↗")}</section>
<section class="contact-line wrap" id="contact" aria-label="Contact">{link('mailto:'+EMAIL,EMAIL+' ↗','contact-address')}{link('https://www.linkedin.com/in/luke-stilson/','LinkedIn ↗')}</section></main>'''
    (ROOT/'index.html').write_text(page('Technical Art & Tools','Luke Stilson: technical artist and tools designer. PlushEngine, OpenVAT, production pipelines, rendering, and independent experiments.',body,body_class='home portfolio-home'))


def vspx_page():
    body='''<main id="main" class="vspx-page wrap">
<a class="back-link" href="index.html#games">← Back to prototypes</a>
<header class="vspx-heading"><p class="game-engine game-engine-feature"><img src="assets/games/unity.svg" alt=""><span>Unity · Personal project</span></p>
<h1>VSPX</h1><p>I knew a MOBA was probably too big a project. I wanted to find out what it would take anyway—and learn how to build systems that could handle more than one character, ability, or idea.</p></header>
<figure class="vspx-hero"><img src="assets/games/vspx-combat.jpg" alt="A VSPX combat test with characters and minions on a prototype map"><figcaption>A development test. Some models and other visual assets are borrowed from League of Legends as placeholders and belong to Riot Games.</figcaption></figure>
<section class="vspx-feature"><div><p class="eyebrow">The project</p><h2>Making each piece useful more than once</h2></div><div><p>VSPX started with a scope I knew was too big. That was part of the point: I wanted to see what a game like this asks of its systems, and how to keep a large codebase manageable as those systems grow.</p><p>Instead of solving every problem for one character, I try to make each piece useful across a roster: serialized data, shared combat rules, and ways to author abilities, items, and interactions.</p></div></section>
<section class="vspx-feature"><div><p class="eyebrow">Abilities & authoring</p><h2>Building a kit from shared parts</h2></div><div><p>A character is defined by data: stats, an archetype, and a set of abilities. Each ability describes things like how it targets, its range and cooldown, what happens on a hit, and whether it’s a projectile, dash, area effect, or something else.</p><p>Those pieces connect to shared systems for damage, healing, shields, status effects, and on-hit behavior. The interesting part is using the same vocabulary to make different kits—and then seeing how they interact when an entire roster is in play.</p></div></section>
<figure class="vspx-video"><video controls playsinline preload="none" poster="assets/games/vspx-vfx-combat.jpg"><source src="assets/games/vspx-vfx-combat.mp4" type="video/mp4"></video><figcaption>Abilities, targeting, and combat effects in a development test. The footage includes borrowed placeholder assets.</figcaption></figure>
<section class="vspx-feature"><div><p class="eyebrow">Items & economy</p><h2>Decisions that build over a match</h2></div><div><p>Items aren’t just a list of stat boosts. I’ve been working through components and upgrade recipes, item slots, costs, and how different character archetypes put a build together. Pre-game augments add another place to experiment with how a character plays.</p><p>Then there’s the economy around it: income, minions, camps, kills, and objectives all affect when a player can afford their next item. I’ve been tuning those rewards against match length and one another; the numbers and balance are still very much in progress.</p></div></section>
<figure class="vspx-video"><video controls playsinline preload="none" poster="assets/games/vspx-items-abilities.jpg"><source src="assets/games/vspx-items-abilities.mp4" type="video/mp4"></video><figcaption>An item menu followed by an ability and combat test. Visuals include borrowed placeholder assets.</figcaption></figure>
<figure class="vspx-hero"><img src="assets/games/vspx-augments.jpg" alt="An in-development augment selection screen in VSPX" loading="lazy"><figcaption>An in-progress augment selection and match setup screen.</figcaption></figure>
<section class="vspx-feature"><div><p class="eyebrow">Animation & effects</p><h2>Putting OpenVAT to work</h2></div><div><p>Almost all of the animation and VFX use vertex animation textures. It’s a useful place to put <a href="projects/openvat.html">OpenVAT</a> to work on both characters and effects while I figure out how the game should look and feel in motion.</p><p>These recordings are from different stages of development. They include models and other visuals borrowed from League of Legends as placeholders, including minions in later footage. Later work is mostly my own, but I don’t yet have footage that cleanly separates all of those assets.</p></div></section>
<section class="vspx-feature"><div><p class="eyebrow">Bot players</p><h2>Making the other side think</h2></div><div><p>Bot AI has been a project of its own. A bot needs to make sense of its character’s abilities and role, fight, farm, buy items, and respond to what’s happening around it. Getting those decisions to work together in a complex game has been a lot of the learning.</p><p>I’ve also experimented with accelerated match tests to look at behavior, balance, and pacing as the systems change.</p></div></section>
<section class="vspx-feature"><div><p class="eyebrow">Gameplay design</p><h2>What if players built the map control?</h2></div><div><p>One mode I’ve explored gets rid of fixed lanes and lets players place their own turrets. Those structures create places to recover, control space, and support minion waves; investing in them competes with spending on your own character.</p><p>The idea is to make positioning and small decisions matter while I work through the harder question: how do you keep a match moving without losing the back-and-forth that makes it fun?</p></div></section>
<section class="vspx-gallery" aria-labelledby="vspx-gallery-title"><header><p class="eyebrow">From the workbench</p><h2 id="vspx-gallery-title">A few more tests</h2><p>Short clips from different stages of the project, from an early map to combat and balance tests. Gameplay footage includes borrowed placeholder assets.</p></header><div class="vspx-gallery-grid">
<figure><video controls playsinline preload="none" poster="assets/games/vspx-ability-test.jpg" aria-label="Ability targeting test"><source src="assets/games/vspx-ability-test.mp4" type="video/mp4"></video><figcaption><strong>Ability targeting</strong><span>Trying out attacks, targeting, and effects in a match.</span></figcaption></figure>
<figure><video controls playsinline preload="none" poster="assets/games/vspx-teamfight.jpg" aria-label="Combat test with multiple characters"><source src="assets/games/vspx-teamfight.mp4" type="video/mp4"></video><figcaption><strong>Systems in a fight</strong><span>Characters, minions, abilities, and effects on screen together.</span></figcaption></figure>
<figure><video controls playsinline preload="none" poster="assets/games/vspx-early-map.jpg" aria-label="Early VSPX map prototype"><source src="assets/games/vspx-early-map.mp4" type="video/mp4"></video><figcaption><strong>An earlier map</strong><span>Testing characters and combat in an early blockout.</span></figcaption></figure>
<figure><video controls playsinline preload="none" poster="assets/games/vspx-balance-data.jpg" aria-label="Match balance analysis view"><source src="assets/games/vspx-balance-data.mp4" type="video/mp4"></video><figcaption><strong>Looking at the data</strong><span>Exploring match results and character metrics while working on balance.</span></figcaption></figure>
</div><p class="vspx-gallery-note">Silent development recordings · Select a clip to play</p></section>
<section class="vspx-feature"><div><p class="eyebrow">Still in progress</p><h2>A lot left to figure out</h2></div><div><p>A networked MOBA is the long-term idea, but networking is still groundwork and local testing—not a finished multiplayer game. VSPX is a personal prototype, and the systems and balance are still changing as I learn what they need.</p></div></section>
<div class="vspx-end"><a class="button" href="index.html#games">← More prototypes</a></div></main>'''
    (ROOT/'vspx.html').write_text(page('VSPX','A personal Unity project exploring reusable game systems, bot AI, and MOBA-inspired design.',body,active='Work'))

def personal_game_page(name, title, subtitle, hero, alt, paragraphs, video, itch=False):
    sections=''.join('<section class="vspx-feature"><div><p class="eyebrow">'+esc(label)+'</p><h2>'+esc(heading)+'</h2></div><div>'+''.join('<p>'+esc(p)+'</p>' for p in copy)+'</div></section>' for label,heading,copy in paragraphs)
    resources='<a href="minesweeper-notes.html">Original concept notes →</a>' if name=='mine-over-matter.html' else ''
    release='<a class="button" href="https://sharp3ned.itch.io/blink-devrelease">Experimental Windows build on itch.io ↗</a><p class="game-release-note">An early development build from 2020. The download is hosted externally; see the itch page for controls and known issues.</p>' if itch else ''
    body=f'''<main id="main" class="vspx-page wrap"><a class="back-link" href="index.html#games">← Back to prototypes</a>
<header class="vspx-heading"><p class="game-engine game-engine-feature"><img src="assets/games/unreal.svg" alt=""><span>Unreal Engine · Personal project</span></p><h1>{esc(title)}</h1><p>{esc(subtitle)}</p>{release}</header>
<figure class="vspx-hero"><img src="{esc(hero)}" alt="{esc(alt)}"><figcaption>From the project in development.</figcaption></figure>
{sections}<figure class="vspx-video"><video controls playsinline preload="none" poster="{esc(hero)}"><source src="{esc(video)}" type="video/mp4"></video><figcaption>Gameplay footage from the project.</figcaption></figure>
<div class="vspx-end">{resources} <a class="button" href="index.html#games">← More prototypes</a></div></main>'''
    (ROOT/name).write_text(page(title,subtitle,body,active='Work'))

def other_games_pages():
    personal_game_page('mine-over-matter.html','Mine Over Matter',
        'A focused first-person Minesweeper prototype, built to learn about puzzle generation and what makes a puzzle solvable.',
        'assets/games/mine-over-matter.jpg','A handheld detector overlooking a minefield',[
        ('The idea','A familiar puzzle, in a physical space',[
        'I wanted to take Minesweeper into a first-person environment and see how the same decisions feel when the tiles are part of the world. A handheld detector gives you the information you need to work through the field.',
        'Unlike some of my bigger experiments, I wanted to keep this one tightly scoped. It gave me a manageable way to explore puzzle design alongside the environment, materials, and gameplay.']),
        ('The process','Generating a puzzle worth solving',[
        'A big question was how to generate puzzles that are always solvable: working backward through a solver and learning how to reason about the information a player has at each step. I also brought the project from UE4 into UE5 to understand the differences between the two. The original notes go further into possible progression and presentation.'])],
        'videos/minesweeper1.mp4')
    personal_game_page('blink.html','BLiNK',
        'An early first-person UE4 project where I kept asking what else I could add.',
        'assets/games/blink.jpg','A scene from the BLiNK project',[
        ('The game','A place to try everything',[
        'BLiNK was one of the first big game projects I approached as a place to experiment, rather than a tightly scoped game. I built it in Unreal Engine 4 using Blueprints and kept exploring whatever I wanted to try next.',
        'That meant weapon selection, ability selection, grappling and traversal, combat, and level design all found their way in. The experimental release includes a search-and-destroy mode against AI.']),
        ('An early release','Putting it in people’s hands',[
        'I shared an early Windows development build on itch.io for feedback. It’s a rough pre-alpha rather than a finished game, but it was a chance to put a playable version out and learn from the process.'])],
        'images/blink/blink.mp4',True)

def earlier_work_page():
    body='''<main id="main" class="archive-story wrap">
<a class="back-link" href="index.html#work">← Back to the portfolio</a>
<header class="archive-story-heading"><p class="eyebrow">A little history</p><h1>How I got here</h1>
<p>From stop-motion animation to digital worlds, games, and the tools behind them. A look back at some of the work that got me here.</p></header>
<div class="archive-intro-grid"><figure class="archive-visual archive-intro-large"><img src="assets/early-work/stop-motion.webp" alt="Luke as a kid at a stop-motion setup with a camera and computer" fetchpriority="high"><figcaption>Making stop-motion animation · around 2007</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/hotel.webp" alt="An early modeled and textured hotel room"><figcaption>Hotel room study · Blender Cycles</figcaption></figure></div>
<section class="archive-chapter archive-origin"><div><p class="eyebrow">Where it started</p><h2>One frame at a time</h2></div><div><p>I was making stop-motion animations and starting to learn Blender when I was a kid. There was something about making things move one frame at a time that stuck with me.</p><p>Around the same time, I was trying to make games in the Blender Game Engine. I didn’t really think of it as wanting to work in games; I was interested in art and animation, and making things move was what I liked. That interest followed me into digital animation and eventually to Bradley University, where I studied visual effects and animation. I started exploring modeling, lighting, materials, and building a whole place for a story to happen.</p></div></section>
<section class="archive-chapter"><div><p class="eyebrow">Animation & images · 2015</p><h2>Making images move</h2></div><div><p>In college I was experimenting with animation, compositing, and the strange things that happen when you push an image around. <em>Skygazing</em> came out of that period, alongside datamoshing and other visual tests.</p><div class="archive-image-pair"><figure class="archive-visual"><img src="assets/early-work/datamosh.webp" alt="A colorful datamoshing experiment"><figcaption>A datamoshing experiment</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/lion-sculpt.webp" alt="An early digital sculpt of a seated lion"><figcaption>Lion sculpt · Blender and Mudbox</figcaption></figure></div><figure><div class="archive-video"><iframe src="https://player.vimeo.com/video/143210985" title="Skygazing, 2015" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div><figcaption>Skygazing · 2015</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">2015 · Building environments</p><h2>Making places, piece by piece</h2></div><div><p>I started building environments as sets of pieces: a modular classroom, a hotel room in Blender, and scenes that could move into Unreal. A lot of the work was figuring out what happened between the programs and why something looked different when it got there.</p><div class="archive-image-pair"><figure class="archive-visual"><img src="assets/early-work/classroom.webp" alt="An early modular classroom model"><figcaption>Early modular classroom</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/hotel-detail.webp" alt="A fan in the modeled hotel room"><figcaption>A detail from the hotel room</figcaption></figure></div><figure class="archive-visual archive-wide"><img src="assets/early-work/courtyard.webp" alt="An early Unreal courtyard study with a tree and foliage"><figcaption>Courtyard study · Original work mixed with Unreal’s Kite Demo content</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">Materials & systems</p><h2>Why does it work that way?</h2></div><div><p>The surfaces became their own experiments. I was making materials I could adjust across different objects, vertex-painting wear onto chairs, and finding ways to see changes in real time.</p><div class="archive-image-pair"><figure class="archive-visual"><img src="assets/early-work/chairs.webp" alt="Two orange chairs from an Unreal material study"><figcaption>Chair materials · Unreal Engine 4</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/materials.webp" alt="Several floor material variations"><figcaption>Floor material variations · Unreal Engine 4</figcaption></figure></div><p>I was also exploring motion in materials. This early animated moss test used Quixel Megascans and Blender Cycles.</p><figure><div class="archive-video archive-video-compact"><iframe src="https://player.vimeo.com/video/183374868" title="Animated Moss Grow Texture, 2016" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div><figcaption>Animated moss texture test · 2016</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">College · 2016–2017</p><h2>Learning to build it all</h2></div><div><p>At this point I was focused on animation and 3D modeling, trying to find a style and learning a little bit of everything along the way. I was modeling modular pieces and variations before I had much sense of how I might use those ideas in a game.</p><figure class="archive-visual archive-wide"><img src="assets/early-work/modular-buildings.webp" alt="A modular brick building model with varied windows and details" loading="lazy"><figcaption>Modular modeling study · 2016</figcaption></figure><p>For my senior project I could choose the software, so after working in Cinema 4D and Maya in college, I went back to Blender. It was a solo project and a chance to bring everything I’d been learning together.</p><figure class="archive-visual archive-wide"><img src="assets/early-work/senior-film.webp" alt="A rendered lakeside shot from my senior animation project" loading="lazy"><figcaption>Senior project · Blender Cycles · 2017</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">2018 · Real-time art</p><h2>Getting more out of the pixels</h2></div><div><p>I was also learning Substance Designer and Painter and using those materials on real-time assets. I liked being able to get close to a surface and still see all the small details that made it feel used.</p><div class="archive-image-pair"><figure class="archive-visual"><img src="assets/early-work/substance-detail.webp" alt="A textured valve and pipe against a brick wall" loading="lazy"><figcaption>Early Substance work · Marmoset Toolbag</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/substance-closeup.webp" alt="Close-up of a weathered metal valve" loading="lazy"><figcaption>Material detail · 2018</figcaption></figure></div><p>For this large robot study, inspired by Simon Stålenhag’s <em>Tales from the Loop</em>, I modeled and textured the subject for Unreal. The interesting problem was keeping a consistent level of texture detail across something huge without relying on enormous image maps.</p><figure class="archive-visual archive-wide"><img src="assets/early-work/loop-study.webp" alt="A large robot in a landscape, inspired by Tales from the Loop" loading="lazy"><figcaption>Large-scale asset and texture study · Unreal Engine 4 · 2018</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">2018–2020 · Independent work</p><h2>Putting the pieces together</h2></div><div><p>Over time, these experiments became independent projects, environments, and real-time work. The 2020 reel brings together modeling, textures, environments, and gameplay work from that period.</p><figure><div class="archive-video"><iframe src="https://player.vimeo.com/video/388068539" title="Digital Art Reel 2020" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div><figcaption>Digital Art Reel · 2020</figcaption></figure></div></section>
<section class="archive-chapter"><div><p class="eyebrow">From making things to making tools</p><h2>Finding ways around the work</h2></div><div><p>I came into this from the art side and tried to do a lot myself. That naturally made me a generalist: the more I needed to make, the more I needed to understand the software underneath it.</p><p>Over time I learned more code, became the person people came to with Blender questions, and then the person they asked to make tools. This early texturing toolset was part of the work that eventually led to Aether: building something for Blender, then using it on small projects to find what needed to change.</p><div class="archive-image-pair"><figure class="archive-visual"><img src="assets/early-work/aether-origins.webp" alt="A small computer model textured with an early Blender toolset" loading="lazy"><figcaption>Early texturing toolset test · 2024</figcaption></figure><figure class="archive-visual"><img src="assets/early-work/aether-materials.webp" alt="A colorful material view of the small computer model" loading="lazy"><figcaption>Working through materials and presets</figcaption></figure></div><p>Making tutorials became another way to share what I was figuring out. Alongside the tools, I kept getting deeper into game programming and the systems underneath the things I wanted to build.</p></div></section>
<section class="archive-end"><div><p class="eyebrow">Still figuring things out</p><h2>Making the tools, too</h2><p>These days my work spans technical art, tools, 3D, and game development. I’m proud of how much ground I’ve covered, and I want to keep growing into the technical direction and engineering side of the work. I still like making things, taking them apart, and figuring out how they work.</p></div><nav><a href="index.html#games">Game prototypes →</a><a href="devlog/index.html">Experiments & dev log →</a><a href="index.html#work">Back to the portfolio →</a></nav></section>
</main>'''
    (ROOT/'earlier-work.html').write_text(page('How I got here','A visual history of animation, materials, environments, and tools by Luke Stilson.',body,active='Work'))

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
    workflow=''.join('<div><span>'+number+'</span><h2>'+title+'</h2><p>'+text+'</p></div>' for number,title,text in [('01','Animate','Use the Blender tools you already work with.'),('02','Encode','Bake the evaluated deformation into textures.'),('03','Play','Bring the data into Unity and control playback in a project.')])
    body=f'''<main id="main" class="plush-brief openvat-brief wrap"><a class="back-link" href="../index.html#work">← Back to the portfolio</a>
<header class="plush-brief-heading"><p class="eyebrow">Blender encoder + Unity receiver · Free & open source</p><h1>OpenVAT</h1><p>{esc(feature['intro'])}</p><nav class="brief-actions" aria-label="OpenVAT links">{link('https://extensions.blender.org/add-ons/openvat/','Get OpenVAT ↗','button')}{site_link('openvat','','OpenVAT.org ↗')}{link('https://github.com/sharpen3d/openvat','Source code ↗')}{link('https://github.com/sharpen3d/openvat/commits/main/','Latest development ↗')}</nav></header>
<div class="vat-workflow" aria-label="OpenVAT workflow">{workflow}</div>
<section class="brief-data vat-origami"><div><p class="eyebrow">Vertex animation textures</p><h2>{esc(feature['origamiTitle'])}</h2><p>{esc(feature['origamiText'])}</p><p>{esc(feature['origamiNote'])}</p></div><figure class="origami-media"><video controls muted playsinline preload="none" poster="../assets/openvat-origami-poster.jpg" width="405" height="720" aria-label="Origami folding shown as a vertex animation texture, vertex offsets, and the final mesh"><source src="../assets/openvat-origami.mp4" type="video/mp4"></video><figcaption>Texture data → vertex offsets → the folding mesh.</figcaption></figure></section>
<section class="brief-data vat-explainer"><figure><a class="vat-video-link" href="{watch}" aria-label="Watch {esc(video['title'])}"><img src="https://i.ytimg.com/vi/{video['id']}/hqdefault.jpg" alt="{esc(video['title'])}" width="480" height="360" loading="lazy"><span>Watch the explanation on YouTube ↗</span></a><figcaption>{esc(video['title'])}</figcaption></figure><div><p class="eyebrow">The idea behind it</p><h2>How vertex animation textures work</h2><p>{esc(feature['explainer'])}</p><p>I walk through the format, the encoding, and the shader side in this video, with examples of what you can do with the result.</p><nav class="vat-chapters" aria-label="Video chapters">{chapters}</nav></div></section>
<div class="brief-extras vat-features">{features}</div>
<section class="brief-data vat-unity"><div><p class="eyebrow">The Unity side</p><h2>From a bake to something you can use in a game</h2><p>The Blender encoder is only half of OpenVAT. I also built a Unity receiver to bring the exported mesh and textures into a project, set up the material, and make the animation usable at runtime.</p><p>That means working with shaders and playback from gameplay code, not just watching an animation loop. It’s the side I use for characters and effects in <a href="../vspx.html">VSPX</a>.</p><nav class="brief-actions">{site_link('openvat','integrations.html#unity','Unity setup →')}{link('https://github.com/sharpen3d/openvat-unity','Unity package source ↗')}</nav></div><figure><a class="vat-video-link" href="https://www.youtube.com/watch?v=NGniucSk4hU" target="_blank" rel="noopener noreferrer"><img src="https://i.ytimg.com/vi/NGniucSk4hU/hqdefault.jpg" alt="No Rig Required — Vertex Animation for Gameplay, an OpenVAT video" width="480" height="360" loading="lazy"><span>Watch the Unity gameplay video ↗</span></a><figcaption>No Rig Required · Vertex Animation for Gameplay</figcaption></figure></section>
<section class="brief-stack vat-project"><div><p class="eyebrow">My part in it</p><h2>From Blender to the engine</h2><p>{esc(feature['work'])}</p></div><div class="vat-engine-notes"><h3>Other engines</h3><p>Beyond Unity, OpenVAT includes simpler shader examples for other engines, including Unreal and GLSL templates. AntzGames built a separate, more developed Godot integration for the community.</p><nav>{site_link('openvat','integrations.html#engines','Integrations & setup →')}{link('https://github.com/antzGames/OpenVAT-for-Godot','Community Godot project ↗')}</nav><h3>One constraint to know</h3><p>{esc(feature['limit'])}</p></div></section>
{recognition(p)}
<footer class="brief-end"><p>OpenVAT is free and open source. The OpenVAT site has the technical details, engine setup, and documentation; my YouTube channel has the walkthroughs.</p><nav class="brief-actions" aria-label="Explore OpenVAT">{site_link('openvat','','OpenVAT.org ↗','button')}{link('../tutorials.html#openvat','More OpenVAT tutorials →')}{link('https://github.com/sharpen3d/openvat','GitHub ↗')}</nav></footer></main>'''
    (ROOT/url(p)).write_text(page('OpenVAT',feature['intro'],body,'../',active='Work',body_class='project-page openvat-story'))


def aether_case(p):
    from aether_portfolio import build_page, build_api
    build_api()
    build_page(page, p)

def aether_gallery_page():
    sync_grass_comparison()
    entries=sync_gallery()
    variations=sync_variations()
    sections=[]
    for section in ['Exterior materials','Interior materials','Near-field relief','Trim sheets and atlases','Props']:
        cards=[]
        for item in [entry for entry in entries if entry['section']==section]:
            atlas=(f'<img class="aether-gallery-atlas" src="{esc(item["atlas"])}" alt="PBR map atlas for {esc(item["title"])}" loading="lazy" width="960" height="540">' if item['atlas'] else '')
            hint='Hover for maps · tap to enlarge' if atlas else 'Tap to enlarge'
            cards.append(f'''<article class="aether-gallery-card"><button type="button" data-gallery-card aria-label="Enlarge {esc(item['title'])}"><span class="aether-gallery-media"><img class="aether-gallery-render" src="{esc(item['render'])}" alt="{esc(item['alt'])}" loading="lazy" width="1600" height="900">{atlas}</span><span class="aether-gallery-label"><strong>{esc(item['title'])}</strong><span class="aether-gallery-hint">{hint}</span></span></button></article>''')
        if cards:
            anchor=section.lower().replace(' ','-')
            sections.append(f'<section class="aether-gallery-section" id="{anchor}"><header><h2>{esc(section)}</h2><span>{len(cards)} works</span></header><div class="aether-gallery-grid">{"".join(cards)}</div></section>')
    feature='''<section class="grass-comparison-section" aria-labelledby="grass-meadow-feature">
<p class="eyebrow">Rendering study · Grass Meadow</p><h2 id="grass-meadow-feature">Surface detail in Plush</h2>
<p class="grass-intro">Compare the same surface from a fixed camera in Plush, then inspect the orthographic maps captured by Aether.</p>
<figure class="grass-comparison" data-grass-comparison>
<div class="grass-view-tabs" aria-label="Grass meadow views">
<button type="button" data-view="compare" aria-pressed="true">Compare</button><button type="button" data-view="flat" aria-pressed="false">Flat PBR</button><button type="button" data-view="pom" aria-pressed="false">POM</button><button type="button" data-view="surfel" aria-pressed="false">Surfels + POM</button><button type="button" data-view="basecolor" aria-pressed="false">Base color</button><button type="button" data-view="normal" aria-pressed="false">Normal</button><button type="button" data-view="roughness" aria-pressed="false">Roughness</button><button type="button" data-view="ao" aria-pressed="false">AO</button><button type="button" data-view="height" aria-pressed="false">Height</button>
</div>
<div class="grass-comparison-image" data-comparison-image data-mode="compare" style="--first:33.333%;--second:66.667%">
<img class="grass-compare-surfel" src="assets/aether-gallery/grass-compare-surfel.jpg" alt="Grass meadow viewed from a fixed camera in Plush" width="1920" height="1080">
<img class="grass-compare-pom" src="assets/aether-gallery/grass-compare-pom.jpg" alt="" width="1920" height="1080">
<img class="grass-compare-flat" src="assets/aether-gallery/grass-compare-flat.jpg" alt="" width="1920" height="1080">
<img class="grass-compare-map" data-comparison-map src="assets/aether-gallery/grass-map-basecolor.jpg" alt="" hidden>
<button class="grass-divider grass-divider-first" type="button" data-divider="first" role="slider" aria-label="Flat PBR and POM boundary" aria-valuemin="0" aria-valuemax="67" aria-valuenow="33"><span aria-hidden="true">↔</span></button><button class="grass-divider grass-divider-second" type="button" data-divider="second" role="slider" aria-label="POM and surfel boundary" aria-valuemin="33" aria-valuemax="100" aria-valuenow="67"><span aria-hidden="true">↔</span></button>
<span class="grass-label grass-label-flat" aria-hidden="true">Flat PBR</span><span class="grass-label grass-label-pom" aria-hidden="true">POM</span><span class="grass-label grass-label-surfel" aria-hidden="true">Surfels + POM</span></div>
<figcaption data-comparison-caption>Drag the dividers on the image, or use the arrow keys when a divider is focused. Tabs show each view on its own.</figcaption></figure>
<div class="grass-data"><div><h3>From Aether to Plush</h3><p>Aether captures the meadow orthographically into base color, tangent-space normal, roughness, metallic, ambient occlusion, opacity and physical height maps. The flat view shades those maps on the host surface. POM traces the height field in the shader and offsets the map coordinates to suggest depth at an angle.</p><p>For near-field relief, Aether also captures eight depth slices, including coverage, height and shading data. It compiles those captures into clustered surface samples. Plush culls and draws the samples as surfels close to the camera, transitioning to the POM host farther away. The surfel view shows that combined runtime path, rather than the original grass geometry.</p><p><a href="https://github.com/sharpen3d/Aether">Legacy Aether source ↗</a> · <a href="https://github.com/sharpen3d/PlushEngine">PlushEngine source ↗</a></p></div><div class="grass-data-figures"><figure><a href="assets/aether-gallery/maps_05_grass_meadow.jpg"><img src="assets/aether-gallery/maps_05_grass_meadow.jpg" alt="Grass Meadow exported PBR maps, including color, normal, roughness, ambient occlusion and height" loading="lazy" width="960" height="540"></a><figcaption>Orthographic PBR and height outputs.</figcaption></figure><figure><a href="assets/aether-gallery/grass-meadow-slabs.jpg"><img src="assets/aether-gallery/grass-meadow-slabs.jpg" alt="Coverage masks from the eight Grass Meadow depth slices" loading="lazy"></a><figcaption>Coverage from the eight depth slices used for near-field compilation.</figcaption></figure></div></div></section>'''
    beadboard='''<section class="aether-gallery-feature" aria-labelledby="beadboard-feature"><div class="aether-feature-copy"><p class="eyebrow">Material study</p><h2 id="beadboard-feature">Beadboard wainscot</h2><p>This painted beadboard is built as a one-metre repeating surface. The construction includes the board profiles and joints, cupping, nail holes, raised grain and damage to the paint layers.</p><p>The material captures a green top coat over older cream paint and exposed wood, with wear and grime responding to the surface structure. The images show the material in Plush and the maps exported from Aether.</p></div><figure><img src="assets/aether-gallery/mat_36_beadboard_wainscot.jpg" alt="Beadboard wainscot material rendered in PlushEngine" loading="lazy" width="1600" height="900"><figcaption>Beadboard wainscot in Plush.</figcaption><img src="assets/aether-gallery/maps_36_beadboard_wainscot.jpg" alt="Beadboard wainscot PBR maps exported from Aether" loading="lazy" width="960" height="540"></figure></section>'''
    variation_cards=[]
    for item in variations:
        atlas=(f'<img class="aether-gallery-atlas" src="{esc(item["atlas"])}" alt="PBR map atlas for {esc(item["title"])}" loading="lazy" width="960" height="540">' if item['atlas'] else '')
        variation_cards.append(f'''<article class="aether-gallery-card"><button type="button" data-gallery-card aria-label="Enlarge {esc(item['title'])}"><span class="aether-gallery-media"><img class="aether-gallery-render" src="{esc(item['render'])}" alt="{esc(item['alt'])}" loading="lazy" width="1600" height="900">{atlas}</span><span class="aether-gallery-label"><strong>{esc(item['title'])}</strong><span class="aether-gallery-hint">Hover for maps · tap to enlarge</span></span></button></article>''')
    variation_section=(f'''<details class="aether-gallery-section"><summary>Procedural variations · {len(variation_cards)} studies</summary><p>Aether material variations. These previews show the exported base-color maps; hover or tap to inspect the map sets.</p><div class="aether-gallery-grid">{''.join(variation_cards)}</div></details>''' if variation_cards else '')
    body=f'''<main id="main" class="aether-gallery-page wrap"><a class="back-link" href="aether.html">← Aether</a><header class="aether-gallery-heading"><p class="eyebrow">Rendered in PlushEngine</p><h1>Aether gallery</h1><p>Materials, relief surfaces, and props authored in Aether and rendered through the game engine. Hover a material to see its exported PBR maps; open any work for the full pair.</p></header>{feature}{beadboard}{''.join(sections)}{variation_section}<dialog class="aether-gallery-viewer" data-gallery-viewer><button type="button" aria-label="Close gallery">×</button><div></div></dialog></main>'''
    from aether_portfolio import apply_header
    (ROOT/'aether-gallery.html').write_text(apply_header(page('Aether gallery','A public gallery of Aether materials and props rendered in PlushEngine, with their exported PBR texture sets.',body,active='Work',body_class='project-page aether-page'), 'gallery'))


def case(p):
    if p["id"] == "openvat":
        openvat_case(p)
        return
    if p["id"] == "aether":
        aether_case(p)
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
    games=''.join(study_entry(key,anchor) for key,anchor in [('minesweeperRemastered','minesweeper'),('blink','blink'),('die','dice')])
    effects=PROJECTS['bpxemitters']
    body=f'''<main id="main" class="collection-page wrap"><a class="back-link" href="index.html#work">← Back to the portfolio</a><header class="case-heading"><h1>Experiments</h1><p class="case-description">Environments, game prototypes, and smaller studies with sound and procedural animation. Personal work I still like, gathered in one place.</p></header><nav class="collection-nav" aria-label="Experiment categories">{link('#audio','Sound & animation ↓')}{link('#environment','Environment art ↓')}{link('#games','Game prototypes ↓')}</nav><section class="study-group" id="audio"><h2>Sound & procedural animation</h2>{study_entry('audiovisualizer','audio-geometry')}<article class="study-entry" id="effects"><div class="study-entry-heading"><h3>Procedural effects</h3><p>Geometry Nodes, Python, and sprite output</p></div>{media(effects,'')}<p class="study-description">An earlier Blender tool for particle effects and sprite sequences. I built the Python controls and editable node groups for spawning, motion, scale, rotation, color, and looping output. I’m showing it here as a procedural study; it isn’t a current extension release.</p></article></section><section class="study-group" id="environment"><h2>Environment art</h2>{study_entry('railway','railway')}</section><section class="study-group" id="games"><h2>Game prototypes</h2><div class="game-study-grid">{games}</div></section><section class="earlier-work" id="earlier-work" aria-labelledby="earlier-title"><header><p class="eyebrow">From the archive</p><h2 id="earlier-title">Earlier work</h2><p>Animation, materials, and environments from earlier in my work with 3D.</p><a href="earlier-work.html">Explore the collection →</a></header></section><div class="case-end">{link('index.html#work','← Back to the portfolio','button')}{link('mailto:'+EMAIL,'Email ↗')}</div></main>'''
    (ROOT/'studies.html').write_text(page('Experiments','Personal work by Luke Stilson: environment art, materials, game prototypes, audio-driven Geometry Nodes, and procedural effects.',body,active='Work'))

def redirect_page(path,target,title):
    root='../' if '/' in path else ''
    href=root+target
    body=f'<main id="main" class="document-page wrap"><h1>{esc(title)}</h1><p class="document-intro">This work is now part of a consolidated project page.</p>{link(href,"Continue to the project →","button")}</main>'
    output=page(title,title,body,root)
    output=output.replace('</head>',f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={esc(href)}"><link rel="canonical" href="{esc(href)}"></head>')
    destination=ROOT/path;destination.parent.mkdir(exist_ok=True);destination.write_text(output)

def legacy_pages():
    aliases={'xbake':('aether.html','Aether'),'textureLab':('aether.html','Aether'),'Pixels':('sprite-toolkit.html','Sprite Toolkit'),'zfo':('studio-work.html#onchain','OnChain Studios'),'unboxing':('studio-work.html#onchain','OnChain Studios'),'egaming':('studio-work.html#arrow','Arrow International'),'hellomoto':('studio-work.html#earlier','Earlier client work'),'stackattack':('studio-work.html#earlier','Earlier client work'),'railway':('studies.html#railway','Abandoned Railway'),'audiovisualizer':('studies.html#audio-geometry','Audio & Geometry'),'bpxemitters':('studies.html#effects','Procedural effects'),'minesweeperRemastered':('studies.html#minesweeper','Minesweeper'),'blink':('studies.html#blink','BLiNK'),'hexscapes':('studies.html#games','Game prototypes'),'die':('studies.html#dice','Die!')}
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
    vspx_page()
    other_games_pages()
    earlier_work_page()
    aether_gallery_page()
    devlog_pages()
    for p in PROJECTS.values():
        if p.get('published'): case(p)
    studio_page()
    studies_page()
    legacy_pages()
    resume_page()
    document_page('minesweeper-notes.html','Minesweeper: original concept notes','Original 2024 design notes for an independent concept. These describe ideas and plans, rather than features of a released game.',ARCHIVED['minesweeper'])
    from editor_overrides import apply_all
    apply_all()
    print('Built portfolio: PlushEngine, three Blender tools, studio work, experiments, résumé, and legacy links.')
if __name__=='__main__':main()
