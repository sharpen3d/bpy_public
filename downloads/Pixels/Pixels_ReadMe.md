# Blender 2D Management Add-on Documentation

## Overview
This Blender add-on provides a comprehensive set of tools for managing 2D layers, materials, and camera settings within the Blender environment. The primary features include adding 2D planes, managing image textures, setting pivot points, and configuring camera settings for orthographic views. The add-on integrates with Blender’s 3D Viewport UI, adding custom panels and menus for easy access to its functions.

## Installation
1. Download the add-on zip.
2. Open Blender and go to `Edit > Preferences`.
3. Navigate to the `Add-ons` tab.
4. Click `Install` and select the downloaded zip (do not unzip manually).
5. Enable the add-on by checking the checkbox next to it.

## Custom Panels and UI Elements
### 2D Tools Panel
Located in the `VIEW_3D` UI region, this panel provides access to various 2D tools, including options for adding new layers, setting the camera, and managing images.
![2D Tools Panel](pixelspanel.png)

### Composition Panel
Also in the `VIEW_3D` UI region, this panel allows users to adjust camera settings and manage the composition of the scene.
![Composition Panel](comppanel.png)

### Selected Solid Panel
Shows detailed options for the selected solid, including size adjustments, pivot settings, and layout rigging.
![Selected Solid Panel](selectedsolidpanel.png)

## Key Features
### Image Management
- Import images from a specified folder and apply them as textures to custom 2D planes – which I will reference further as ‘Solids’.
- Each Solid is an object created with a 1x1 plane, with script-controlled geometry nodes `bpx_geo` which defines its pixel-perfect size relative to a 2D camera. Materials on each solid are created in a way to respect image color-space.

#### Operators:
- `scene.button2`: Adds a new Solid to the current scene.
- `scene.imagesfromfolder`: Adds images from a folder to the scene as 2D planes.

### Material Management
The add-on includes tools for setting and managing materials, especially focusing on image textures.

#### Panels and Menus:
- `MAT_PT_matmenu`: Panel for material settings.
- `scene.setmat`: Sets a default material for the selected object.
- `scene.matchtexsize`: Matches the plane size to the texture size.
- `scene.fixpix`: Fixes pixel size according to the render settings and camera properties.

### Camera Settings
Configure the camera to an orthographic view and reset its position and rotation.

#### Operators:
- `scene.resetcam`: Resets the camera to an orthographic view with a predefined size and position.
- `scene.selectcam`: Selects the scene’s active camera.

### Image Pivot Points
The add-on provides various operators to set the pivot point of an object to different predefined locations such as center, corners, and edges.

#### Operators:
- `scene.pivotcenter`: Sets pivot to the center.
- `scene.pivotbottomleft`: Sets pivot to the bottom-left corner.
- `scene.pivotbottomright`: Sets pivot to the bottom-right corner.
- `scene.pivottopleft`: Sets pivot to the top-left corner.
- `scene.pivottopright`: Sets pivot to the top-right corner.
- `scene.pivotleftcenter`: Sets pivot to the left-center.
- `scene.pivottopcenter`: Sets pivot to the top-center.
- `scene.pivotrightcenter`: Sets pivot to the right-center.
- `scene.pivotbottomcenter`: Sets pivot to the bottom-center.

### Layout Rigging
Add empties to each point of a selected solid for layout rigging purposes.

#### Operators:
- `scene.layoutrig`: Adds empties to each point of the selected solid.
- `scene.screenlayout`: Adds empties defining the screen size in units.

### Custom Properties
The add-on defines a custom property group for setting the width and height of new 2D layers.
