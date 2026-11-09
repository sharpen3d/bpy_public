#!/usr/bin/env python3
"""Sync the public Aether gallery from the rendered Plush gallery and Aether map sets."""
from pathlib import Path
import json
import shutil

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
LAB = WORKSPACE / "GameProjects/_Labs/AetherGallery"
SOURCE_IMAGES = LAB / "Reports/gallery/img"
STAGED = LAB / "Authoring/staged"
OUTPUT = ROOT / "assets/aether-gallery"
MAP_ROLES = ("BaseColor", "Normal", "Roughness", "Metallic", "AO", "Height", "Opacity")
OBJECT_TITLES = {
    "utility_box": "Utility box · trim and decals",
    "utility_box_hero": "Utility box · hero material",
    "03_wall_plates": "Wall plates", "04_floor_register": "Floor register",
    "05_cardboard_box": "Cardboard box", "06_cardboard_boxes": "Cardboard boxes",
}

def title(name):
    text = name.split("_", 1)[1] if name[:2].isdigit() else name
    return text.replace("_", " ").capitalize()

def newer(source, destination):
    return not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime

def make_atlas(name, maps_dir, destination):
    sources = [(role, maps_dir / f"{name}_{role}.png") for role in MAP_ROLES]
    sources = [(role, path) for role, path in sources if path.exists()]
    if not sources:
        return False
    if destination.exists() and destination.stat().st_mtime >= max(path.stat().st_mtime for _, path in sources):
        return True
    canvas = Image.new("RGB", (960, 540), "#111316")
    draw = ImageDraw.Draw(canvas)
    for index, (role, path) in enumerate(sources):
        x, y = (index % 4) * 240, (index // 4) * 270
        with Image.open(path) as source:
            tile = ImageOps.fit(source.convert("RGB"), (240, 270), method=Image.Resampling.LANCZOS)
        canvas.paste(tile, (x, y))
        draw.rectangle((x, y + 242, x + 240, y + 270), fill="#08090b")
        draw.text((x + 10, y + 250), role, fill="#f2f0e9")
    canvas.save(destination, "JPEG", quality=82, optimize=True, progressive=True)
    return True

def sync_gallery():
    materials = json.loads((STAGED / "materials.json").read_text())
    order = (STAGED / "shots.txt").read_text().split()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for token in order:
        kind, name = token.split(":", 1)
        if kind == "sheet" or name in {"15_brick_red", "utility_box", "utility_box_hero", "04_floor_register", "05_cardboard_box"}:
            continue
        source = SOURCE_IMAGES / f"{kind}_{name}.jpg"
        if not source.exists():
            continue
        render = OUTPUT / source.name
        if newer(source, render):
            shutil.copy2(source, render)
        material, atlas = materials.get(name), None
        if material:
            atlas_file = OUTPUT / f"maps_{name}.jpg"
            if make_atlas(name, Path(material["maps"]), atlas_file):
                atlas = f"assets/aether-gallery/{atlas_file.name}"
        section = {"mat": "Interior materials" if name[:2].isdigit() and int(name[:2]) >= 25 else "Exterior materials",
                   "relief": "Near-field relief", "sheet": "Trim sheets and atlases", "obj": "Props"}[kind]
        label = OBJECT_TITLES.get(name, title(name))
        entries.append({"section": section, "title": label,
                        "render": f"assets/aether-gallery/{render.name}", "atlas": atlas,
                        "alt": f"{label} rendered in PlushEngine"})
    return entries

def sync_grass_comparison():
    """Refresh the fixed-camera Plush captures when they are re-rendered."""
    captures = LAB / "Reports/features/grass-meadow/comparison"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for mode in ("flat", "pom", "surfel"):
        source = captures / f"{mode}.png"
        target = OUTPUT / f"grass-compare-{mode}.jpg"
        if source.exists() and newer(source, target):
            with Image.open(source) as image:
                image.convert("RGB").save(target, "JPEG", quality=88, optimize=True, progressive=True)


    # Keep individual orthographic maps current alongside the fixed-camera views.
    maps = WORKSPACE / "Blender/Aether/Projects/Materials/05_grass_meadow/maps"
    for role in ("BaseColor", "Normal", "Roughness", "AO", "Height"):
        source = maps / f"05_grass_meadow_{role}.png"
        target = OUTPUT / f"grass-map-{role.lower()}.jpg"
        if source.exists() and newer(source, target):
            with Image.open(source) as image:
                preview = image.point(lambda value: value / 257).convert("L") if image.mode.startswith("I;16") else image
                picture = ImageOps.contain(preview.convert("RGB"), (1536, 1536), Image.Resampling.LANCZOS)
                picture.save(target, "JPEG", quality=90, optimize=True, progressive=True)

def sync_variations():
    """Stage completed Aether variation captures without claiming they are Plush renders."""
    root = WORKSPACE / 'Blender/Aether/Projects/MaterialVariations/20261109'
    if not root.exists():
        return []
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = []
    for blend in sorted(root.glob('*/*/*.blend')):
        name = blend.stem
        maps = blend.parent / 'maps'
        manifest = maps / f'{name}_maps.json'
        base = maps / f'{name}_BaseColor.png'
        if not manifest.exists() or not base.exists() or manifest.stat().st_mtime < blend.stat().st_mtime:
            continue
        render = OUTPUT / f'variation_{name}.jpg'
        if newer(base, render):
            with Image.open(base) as source:
                picture = ImageOps.contain(source.convert('RGB'), (900, 900), Image.Resampling.LANCZOS)
            canvas = Image.new('RGB', (1600, 900), '#191d1c')
            canvas.paste(picture, ((1600-picture.width)//2, (900-picture.height)//2))
            canvas.save(render, 'JPEG', quality=84, optimize=True, progressive=True)
        atlas_file = OUTPUT / f'maps_{name}.jpg'
        atlas = f'assets/aether-gallery/{atlas_file.name}' if make_atlas(name, maps, atlas_file) else None
        label = {'32_wallpaper_peeling_v01': 'Wallpaper · lightly worn', '32_wallpaper_peeling_v02': 'Wallpaper · heavily damaged', '32_wallpaper_peeling_v03': 'Wallpaper · exposed plaster'}.get(name, title(name))
        result.append({'title': label, 'render': f'assets/aether-gallery/{render.name}', 'atlas': atlas,
                       'alt': f'{label} base-color capture from Aether'})
    return result

if __name__ == "__main__":
    print(f"Synced {len(sync_gallery())} public Aether gallery images")
