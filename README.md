# Luke Stilson — portfolio

A static portfolio for technical art, tools, studio work, and independent projects. Open `index.html` directly or serve this directory. No installation is needed.

```sh
python3 build.py
python3 -m http.server 8769 --bind 127.0.0.1
```

The homepage leads with PlushEngine: a project title and short description beside the large abstract eye. Luke’s name and role remain in the site header, without a repeated name or tagline in the main content. The eye links are About, Development reel, and Get Started. The eye adds gaze, blinking, and pupil dilation; there is no image inside it or surrounding frame. Links remain visible on touch devices and work without JavaScript. Reduced motion keeps the eye still. The geometry playground from the previous iteration has been removed.

OpenVAT has a full-width feature card with the glossy mark, project links, and compact evidence links. Aether, Attrio CSV, and Sprite Toolkit have three matching cards underneath, with equal dimensions and prominence on desktop and a single column on mobile. `assets/tool-art/sources.json` records earlier artwork sources and crops. The linked replacement OpenVAT image could not be retrieved, so the existing mark from the local OpenVAT site remains temporary. The other cards use the original project previews; Sprite Toolkit’s image is identified as the earlier workflow. Studio work is a direct link to `studio-work.html`. The experiments section follows the tools, features PCA, and links to all experiments at `studies.html`. Résumé and Email remain in the header rather than beneath the name.

- PlushEngine is a personal engine, editor, and runtime. Its project page retains the actual factory editor capture, three feature sections, and optional development footage.
- OpenVAT has compact evidence links for downloads, 80 Level coverage, and community tools. Its standalone project page and OpenVAT.org hold further detail.
- Aether combines the earlier xBake and TextureLab work. Existing media is identified as earlier work; the current Aether repository is linked.
- Attrio CSV links directly to its Blender Extensions listing. Its preview is the author’s Full Demo image from that listing.
- Sprite Toolkit replaces the older Pixels / 2D Tools entry; the media represents the earlier workflow.

`content/projects.json` holds project descriptions, roles, links, and media. `published` controls standalone project pages. The homepage and page templates live in `build.py`. `content/resume.json` contains résumé facts from the supplied 2026 Word document, retained in `downloads/`.

The devlog lives at `devlog/index.html`, with article content in `content/devlog.json`. Entries sort by their source date; the first is featured in the independent experiments section after the Blender tools. PCA is separate from the PlushEngine feature. On mobile the engine, tools, and experiments retain the same order. Studio summaries remain off the homepage.

The first entry, `devlog/pca-shape-keys.html`, adapts Luke’s July 27–30, 2025 BlenderArtists thread, “PCA for Shape Key Reduction.” It preserves the research date and prototype status, including the failed blinks and grouping work. It does not present the early test as a measured runtime improvement or claim a reconstruction-error percentage. The article’s three images are Luke’s original uploads from posts 14, 15, and 18; each links back to its post. Original media URLs are recorded in `content/devlog.json`. The small WebP thumbnail is a resized copy of the basis-shape grid. No community member’s artwork or replies are reproduced.

The older project URLs redirect to consolidated pages. Retired tools remain unlisted archives with `noindex` and no download buttons. Original media and downloads are preserved.

OpenVAT’s `recognition` entries hold evidence and the date of the download-count check. The 15,000+ figure is a conservative Blender Extensions snapshot, not unique users. Update it deliberately.

`assets/portfolio.css` provides the shared design. `assets/portfolio.js` adds the eye interaction, optional résumé printing, and deep-link opening for native disclosures. The older `style.css` and `mobile.css` are retained for archived pages.

The PlushEngine `website` field currently points to `file:///Users/lukestilson/Plush/Webpage/index.html` and opens in a new tab. Change it to `https://plushengine.com` when hosting is ready. The public site is not assumed to be live. `plush-devlog.html` redirects to the general devlog index, preserving the earlier link.

`content/plush-media.json` records media provenance. Editor captures were made from scratch project copies; original recordings and game projects remain untouched. `assets/plush-factory.jpg` is the actual FpsTemplate editor capture resized to 2000px. Feature crops link to full editor captures. The silent 44-second H.264 reel and technical stack remain in native disclosures. Deep links to `#reel` open its disclosure without starting playback. MCP copy distinguishes the editor tool interface, authoring Undo, and C# compilation and recovery.

Attrio preview: https://extensions.blender.org/add-ons/attrio-csv/ — author’s Full Demo thumbnail saved as `assets/attrio-preview.webp`.

This refresh remains local. No commit, push, or deployment is part of this work.
