"""Build the Aether portfolio page and source-derived public API reference."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
E = lambda value: html.escape(str(value), quote=True)

def aether_header(root='', active='aether'):
    items = [('aether', 'Aether', 'aether.html'), ('gallery', 'Gallery', 'aether-gallery.html'), ('api', 'API Reference', 'aether-api/index.html'), ('github', 'Legacy Aether GitHub ↗', 'https://github.com/sharpen3d/Aether')]
    links = ''.join(f'<a href="{E(href if href.startswith("https:") else root+href)}"'+(' class="on" aria-current="page"' if key == active else '')+f'>{E(label)}</a>' for key,label,href in items)
    return f'<header class="bar aether-bar"><div class="project-identity"><a class="mark" href="{root}aether.html"><span>Aether</span></a><a class="creator-link" href="https://lukestilson.com/">by Luke Stilson</a></div><nav aria-label="Main navigation">{links}</nav></header>'

def apply_header(doc, active):
    header = aether_header(active=active)
    doc, count = re.subn(r'<header class="site-header">.*?</header>', lambda _: header, doc, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError('Expected portfolio header on Aether page')
    return doc.replace('</head>', '<link rel="stylesheet" href="assets/aether-ui/nav.css?v=1"></head>', 1)

def build_page(page, project):
    body = '''<main id="main" class="aether-detail wrap"><a class="back-link" href="index.html#work">← Back to the portfolio</a>
<header class="ad-head"><p class="eyebrow">Blender material authoring · In development</p><h1>Aether</h1><div class="ad-pair"><div><p class="ad-lede">Object texturing and seamless materials, built in Blender.</p><p>I started Aether in 2025, bringing my xBake and TextureLab workflows together. I use it to build surface detail with geometry, Geometry Nodes and shaders, then capture the result as texture maps.</p><p>The current Aether is unreleased. The GitHub repository contains an older preview.</p><nav class="ad-links"><a class="button" href="aether-gallery.html">View the render gallery →</a><a href="aether-api/index.html">API reference →</a><a href="https://github.com/sharpen3d/Aether">Legacy Aether GitHub ↗</a></nav></div><figure><a href="assets/aether-ui/workspace.png"><img class="ad-screen" src="assets/aether-ui/workspace.png" alt="Aether's Blender workspace with UV canvas, object preview and shader editor"></a><figcaption>The Aether workspace in Blender 5.2.3.</figcaption></figure></div></header>
<section class="ad-compact wall-plate-feature" aria-labelledby="surface-detail-title"><div class="ad-pair"><div><p class="eyebrow">Object texturing</p><h2 id="surface-detail-title">Surface Detail from Geometry</h2><p>Aether uses Geometry Nodes to bring the evaluated object into texture space using its UVs, while keeping the source position, normal and material index available to drive detail.</p><p>For these wall plates, switches, screws and outlet details are real geometry in the authoring scene. Aether captures that construction and its materials into maps I can review on the object.</p><p>I’ve also tested the height map with parallax occlusion mapping in Plush. POM shifts texture coordinates with the viewing angle to suggest depth on a flat surface.</p><a href="aether-gallery.html#props">See the wall plates in the gallery →</a></div><figure><a href="aether-gallery.html#props"><img src="assets/aether-gallery/obj_03_wall_plates.jpg" alt="Wall plates rendered in Plush" loading="lazy"></a><figcaption>Wall plates · Rendered in Plush</figcaption></figure></div><div class="wall-plate-captures"><figure><a href="assets/aether-ui/wall-plates-geometry-clean.png"><img src="assets/aether-ui/wall-plates-geometry-clean.png" alt="Blender solid view of the wall plate geometry on the Aether texture canvas" loading="lazy"></a><figcaption>The authored geometry on the texture-space canvas.</figcaption></figure><figure><a href="assets/aether-ui/wall-plates-material-clean.png"><img src="assets/aether-ui/wall-plates-material-clean.png" alt="Blender Shader Editor showing part of the Aether wall plate material" loading="lazy"></a><figcaption>Part of the plate material, routed through Aether’s master shader.</figcaption></figure></div></section>
<section class="ad-compact"><div class="ad-pair"><div><p class="eyebrow">Seamless materials</p><h2>Building a tile</h2><p>For a repeating material, the canvas is a tile. I can model boards or bricks, scatter grass with Geometry Nodes, and use procedural shaders for finer surface detail.</p><p>Aether repeats the evaluated geometry across tile edges, so the same seeded shapes continue onto the next tile. I can change the construction and capture a new set of maps.</p><a href="aether-api/operators/aether-repeat-geometry.html">Geometry repeat →</a></div><figure><a href="aether-gallery.html#exterior-materials"><img src="assets/aether-gallery/mat_05_grass_meadow.jpg" alt="Grass meadow material rendered in Plush"></a><figcaption>Grass meadow · Rendered in Plush</figcaption></figure></div></section>
<section class="ad-compact"><div class="ad-pair"><div><p class="eyebrow">Capture and preview</p><h2>From the scene to maps</h2><p>An orthographic camera captures the texture-space scene into base color, normal, roughness, AO, height and other outputs. Layers can contribute to individual maps and cast AO independently.</p><p>I check a fast preview on the receiver, then export separate or packed maps. The sidebar keeps the layer, preview and output controls together.</p><a href="aether-api/operators/exportmap-render-all-maps.html">Map export →</a></div><figure><a href="assets/aether-ui/output-controls.png"><img class="ad-screen" src="assets/aether-ui/output-controls.png" alt="Aether layer and texture output controls in Blender"></a><figcaption>Layer and output controls · Blender 5.2.3</figcaption></figure></div></section>
<section class="ad-compact"><div class="ad-pair"><div><p class="eyebrow">Development workflow</p><h2>Working through MCP</h2><p>I’m using MCP as a common way to work across my tools. A small set of reusable operations lets an assistant inspect a project, find an extension’s API and the working standards I’ve built up over years, run Blender Python, call operators and reload code. The extensions remain independent, and the work happens in the actual Blender session.</p><p>That gives compatible clients a path to the same tools whether the model runs locally or in the cloud. I can give a smaller model the specific API, project context and standards it needs, rather than the entire codebase. Focused context can reduce token use and helps different models follow the same established workflows, though the results still depend on the model and task.</p><p>Aether’s API is generated from operator docstrings and Blender property declarations, like Plush’s source-derived reference. The assistant can query the current source; this website shows a generated snapshot.</p><a href="aether-api/index.html">Browse the API →</a></div><figure><a href="assets/aether-ui/workspace.png"><img class="ad-screen" src="assets/aether-ui/workspace.png" alt="Blender workspace used to edit Aether materials"></a><figcaption>The workspace used for authoring and review.</figcaption></figure></div></section>
<section class="ad-compact"><div class="ad-pair"><div><p class="eyebrow">Recent work</p><h2>Materials and props in Plush</h2><p>The gallery collects recent renders and map sets, including material variations and wall plates. It also compares flat PBR, parallax occlusion and experimental near-field surfels on the same grass surface.</p><a class="button" href="aether-gallery.html">Explore the gallery →</a></div><figure><a href="aether-gallery.html"><img src="assets/aether-gallery/mat_36_beadboard_wainscot.jpg" alt="Painted beadboard material rendered in Plush"></a><figcaption>Beadboard wainscot · Rendered in Plush</figcaption></figure></div></section></main>'''

    doc=page('Aether — material authoring and baking', 'Aether is my Blender workflow for object texturing and seamless material authoring, baking and export.', body, active='Work', body_class='project-page')
    doc=doc.replace('</head>', '<link rel="stylesheet" href="assets/aether-ui/aether.css?v=1"></head>', 1)
    (ROOT/'aether.html').write_text(apply_header(doc, 'aether'))

def build_api():
    data=json.loads((ROOT/'content/aether-api.json').read_text())
    root=ROOT/'aether-api'; (root/'operators').mkdir(parents=True,exist_ok=True); (root/'settings').mkdir(exist_ok=True)
    ops=sorted(data['operators'],key=lambda x:x['id']); groups=data['settings']
    slug=lambda s: re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
    nav={'stamp':'Aether '+data['aether_version']+' development','sections':[{'t':'Start','g':[{'a':'','i':[{'n':'API home','u':'index.html','s':'Aether API reference'}]}]},{'t':'Operators','g':[{'a':'Blender operators','i':[{'n':o['id'],'u':'operators/'+slug(o['id'])+'.html','s':o.get('label','')+' · '+o.get('status','')} for o in ops]}]},{'t':'Settings','g':[{'a':'RNA properties','i':[{'n':g,'u':'settings/'+slug(g)+'.html','s':'Aether settings for '+g,'m':[[p['name'],slug(p['name'])] for p in props]} for g,props in groups.items()]}]}]}
    (root/'nav.js').write_text('window.PLUSH_API = '+json.dumps(nav,ensure_ascii=False)+';\n')
    def layout(title, current, content):
        prefix='../' if '/' in current else ''
        site='../../' if prefix else '../'
        return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} · Aether API</title><link rel="stylesheet" href="{site}assets/aether-api/style.css"><link rel="stylesheet" href="{site}assets/authorship.css?v=2"><link rel="stylesheet" href="{site}assets/aether-ui/nav.css?v=1"></head><body class="api" data-root="{site}" data-api="{prefix}" data-page="{E(current)}">{aether_header(site, 'api')}<div class="api-layout"><aside class="side"><button class="api-browse-toggle" id="api-browse-toggle" type="button" aria-controls="api-browser-content" aria-expanded="true" hidden>Browse API</button><div class="side-content" id="api-browser-content"><div class="search"><input id="q" type="search" aria-label="Search API operators and settings" placeholder="Search operators and settings" autocomplete="off" spellcheck="false"><kbd>/</kbd></div><nav id="tree" aria-label="API"></nav></div></aside><main class="doc">{content}<footer class="stamp">Aether {E(data['aether_version'])} · source-derived development snapshot</footer></main></div><script src="{prefix}nav.js"></script><script src="{site}assets/aether-api/api.js"></script><footer class="author-footer" data-author-credit><div class="author-inner"><p>© 2026 <a href="https://lukestilson.com/">Luke Stilson</a></p><nav aria-label="Author links"><a href="{site}index.html">Portfolio ↗</a><a href="https://github.com/sharpen3d">GitHub ↗</a></nav></div></footer></body></html>'''
    home='''<h1>API reference</h1><p>Reference for Aether’s Blender operators and RNA settings, generated from the add-on’s operator docstrings and property declarations. The source parser produces Markdown and JSON without running Blender; the website presents a versioned snapshot of that data. The MCP lookup separately queries the current source.</p><p>Enable Aether before calling <code>bpy.ops</code>. Operators can require a particular scene, selection, mode or editor context; check each entry. File writes are outside Blender Undo. Internal Python helpers are not a supported public API.</p><div class="table"><table><thead><tr><th scope="col">Reference</th><th scope="col">Contents</th></tr></thead><tbody><tr><td>Operators</td><td>Identifiers, context, effects, limits and operator properties</td></tr><tr><td>Settings</td><td>RNA properties, descriptions, declared defaults and ranges</td></tr></tbody></table></div><p>Use the sidebar to browse or search. Experimental and placeholder entries are labeled; placeholders do not provide a working action.</p><p><a href="api.json">Download the machine-readable reference</a> · <a href="../aether.html">About Aether</a></p>'''
    (root/'index.html').write_text(layout('API reference','index.html',home)); (root/'api.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    def properties(props):
        if not props:return '<p>This operator declares no Aether-specific keyword properties. It may use scene, object, modifier, or editor settings instead; see its context and related settings below.</p>'
        rows=[]
        for p in props:
            detail=[]
            for k in ('default','min','max','subtype','unit','size'):
                if k in p:detail.append(k+': '+str(p[k]))
            if 'default' not in p: detail.append('default: Blender RNA default')
            if isinstance(p.get('items'), list):
                detail.append('choices: '+', '.join(str(item[0]) for item in p['items'] if item))
            elif isinstance(p.get('items'), dict):
                detail.append('choices: source expression '+str(p['items'].get('expression', 'dynamic')))

            rows.append(f'<tr id="{slug(p["name"])}"><td><code>{E(p["name"])}</code></td><td>{E(p.get("type",""))}</td><td>{E(p.get("description", ""))}<br><small>{E(" · ".join(detail))}</small></td></tr>')
        return '<div class="table"><table><thead><tr><th scope="col">Property</th><th scope="col">Type</th><th scope="col">Description and declaration</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
    # These are settings used by the implementation, not operator keyword arguments.
    related={
        'exportmap.create_bake_scene': [('MapExportSettings',['source_object','uv_map']),('Scene',['export_settings','custom_object_name','export_output_directory'])],
        'aether.bake_source_maps': [('Scene',['aether_target_obj','aether_source_obj','aether_use_highpoly','aether_source_map_directory','aether_bake_uv_map','aether_bake_resolution','aether_bake_samples','aether_bake_margin','aether_bake_normal','aether_bake_normal_obj','aether_bake_ao','aether_bake_position','aether_bake_curvature','aether_bake_material_id','aether_bake_cage_extrusion_scale','aether_bake_max_ray_distance_scale'])],
        'aether.open_export_dir': [('Scene',['aether_target_obj','aether_source_map_directory'])],
        'aether.add_live_surface': [('Scene',['export_settings','aether_target_obj']),('MapExportSettings',['source_object','uv_map'])],
        'aether.scatter_collection': [('Scene',['aether_scatter_collection'])],
        'aether.export_near_field': [('Scene',['export_output_directory','aether_nearfield_slabs','aether_ao_strength','aether_height_bump','export_map_list'])],
        'exportmap.render_all_maps': [('Scene',['export_map_list','export_output_directory','custom_object_name','delimiter','aether_capture_sampling','aether_capture_samples','aether_capture_samples_ao','aether_height_mode','aether_height_min','aether_height_max','aether_height_bump','aether_ao_strength']),('MapExportItem',['map_type','map_name','bit_depth','color_space','channel_format','normal_convention','bake_ao','pack_rgb','pack_r','pack_g','pack_b','pack_a'])],
        'exportmap.render_active_map_preview': [('Scene',['aether_preview_mode','aether_preview_resolution_percentage','aether_inpaint_distance','export_map_list','export_map_index'])],
        'aether.preview_layer_result': [('Scene',['aether_preview_mode','aether_preview_resolution_percentage','export_map_list']),('LayerSettings',['enabled','base_color','normal','roughness','metallic','ao','opacity','cast_ao'])],
        'exportmap.add_map': [('Scene',['export_map_list','export_map_index']),('MapExportItem',['map_type','map_name'])],
        'exportmap.remove_map': [('Scene',['export_map_list','export_map_index'])],
        'exportmap.apply_map_settings': [('Scene',['export_map_list','export_map_index','aether_preview_mode'])],
        'exportmap.load_preset': [('Scene',['export_map_list','export_map_index'])],
        'aether.layer_preset': [('Object',['aether_layer']),('LayerSettings',['enabled','base_color','normal','roughness','metallic','ao','opacity','cast_ao'])],
        'aether.feather_layer': [('Object',['aether_feather']),('FeatherSettings',['enabled','width','curve','opacity'])],
        'aether.fit_feather': [('Object',['aether_feather']),('FeatherSettings',['center','size','coordinates'])],
        'aether.height_use_measured': [('Object',['aether_height']),('LayerHeightSettings',['measured_min','measured_max','target_min','target_max'])],
        'aether.add_region': [('Scene',['aether_regions','aether_region_index']),('AetherRegion',['kind','name','uv_min','uv_max'])],
        'aether.remove_region': [('Scene',['aether_regions','aether_region_index'])],
        'node.add_triplanar_from_template': [('Scene',['aether_triplanar_space'])],
    }
    modifier_controls={
        'aether.repeat_geometry': [('Tile Width / Tile Height','1.0 each','Distance between copies in canvas units.'),('Repeat Radius','1','Radius 1 creates the center tile and its eight neighbors.'),('World XY','True','Align offsets with the top-down canvas even if the source is transformed.'),('Realize Copies','False','Turn instances into geometry when downstream operations require it.')],
        'aether.scatter_collection': [('Source Collection','None','Direct child objects used as instances.'),('Density','40.0','Scatter points per square metre.'),('Seed','0','Stable point, choice and transform variation.'),('Tile Width / Tile Height','1.0 each','Center-tile dimensions in metres; match the repeat modifier.'),('Scale Min / Scale Max','0.8 / 1.2','Range for uniform source scale.'),('Axis Scale','(1, 1, 1)','Additional local XYZ scale.'),('Rotation Min / Rotation Max','0 / 2π radians','Range for rotation around Z.'),('Tilt','0.15 radians','Maximum absolute X/Y tilt.'),('Height Offset','0.0','Point height in canvas Z, in metres.'),('Realize Instances','False','Convert instances to geometry for mesh-only downstream operations.')],
    }
    def related_settings(operator):
        groups_for_op=related.get(operator,[])
        if not groups_for_op:return '<p>Other context, including selection and editor state, is described above. Browse the RNA settings in the sidebar for scene and object controls.</p>'
        out='<p>These are configured on the scene or object; they are not passed to the operator as keyword arguments.</p>'
        for owner,names in groups_for_op:
            available={p['name']:p for p in groups[owner]}
            assert all(name in available for name in names), (operator,owner,names)
            out+=f'<h3>{E(owner)}</h3><ul>'+''.join(f'<li><a href="../settings/{slug(owner)}.html#{slug(name)}"><code>{E(name)}</code></a> — {E(available[name].get("description",""))}</li>' for name in names)+'</ul>'
        return out
    for op in ops:
        path='operators/'+slug(op['id'])+'.html'; desc=op.get('description',''); paragraphs=''.join('<p>'+E(p).replace('\n','<br>')+'</p>' for p in desc.split('\n\n') if p.strip())
        arguments=', '.join(p['name']+'=...' for p in op['properties'])
        guidance='<p>Each <code>...</code> is a placeholder for a value; see the properties below.</p>' if arguments else ''
        mod=''
        if op['id'] in modifier_controls:
            rows=''.join(f'<tr><td>{E(name)}</td><td><code>{E(default)}</code></td><td>{E(description)}</td></tr>' for name,default,description in modifier_controls[op['id']])
            mod='<h2>Resulting Geometry Nodes modifier inputs</h2><p>These are editable inputs on the created modifier, not keyword arguments to the operator.</p><div class="table"><table><thead><tr><th>Input</th><th>Default</th><th>Meaning</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
        txt=f'<h1>{E(op["id"])}</h1><p class="meta">{E(op.get("label",""))} · {E(op.get("status","current"))}</p><div class="code" data-lang="Python"><pre><code>bpy.ops.{E(op["id"])}({E(arguments)})</code></pre></div>{guidance}{paragraphs}<h2>Operator properties</h2>{properties(op.get("properties",[]))}<h2>Related settings</h2>{related_settings(op["id"])}{mod}<h2>Source</h2><p><code>{E(op.get("source",""))}:{E(op.get("line",""))}</code></p>'
        (root/path).write_text(layout(op['id'],path,txt))
    for group,props in groups.items():
        path='settings/'+slug(group)+'.html'; access={'Scene':'bpy.context.scene','Object':'bpy.context.object','MapExportSettings':'bpy.context.scene.export_settings','MapExportItem':'bpy.context.scene.export_map_list[index]','LayerSettings':'bpy.context.object.aether_layer','LayerHeightSettings':'bpy.context.object.aether_height','FeatherSettings':'bpy.context.object.aether_feather','AetherRegion':'bpy.context.scene.aether_regions[index]'}.get(group);txt=f'<h1>{E(group)}</h1><p>Declared Aether RNA properties for <code>{E(group)}</code>.</p>'+ (f'<p>Access through <code>{E(access)}</code>, when the required scene and object are available.</p>' if access else '')+properties(props);(root/path).write_text(layout(group,path,txt))
