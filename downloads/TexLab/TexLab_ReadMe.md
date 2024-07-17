# TexLab Documentation

## Overview
TexLab is a Blender add-on that provides tools for managing and exporting standard PBR texture sets for Unity and Unreal Engine. It allows users to flexibly create detailed normal, roughness, metallic, emission, basecolor, and opacity maps with a non-destructive workflow. This tool is highly expandable will continue to be iterated upon to include further functionality.

## Installation
1. Download the `texlab.zip` file.
2. Open Blender.
3. Go to `Edit > Preferences`.
4. Select `Add-ons` and click `Install`.
5. Locate and select the `texlab.py` file, then click `Install Add-on`.
6. Enable the addon by checking the box next to `Texture Laboratory`.

## Workflow
### Step 1: Setting Up Your Object
1. **Select Your Object**: In the main scene `Scene`, select the object you want to texture.
2. Be sure this is the only object selected (target is Active Object).

### Step 2: Export UV Layout and Setup Scene
1. **Export UV Layout**: Create a UV layout for your object and set up a new scene for it.
2. In the `3D Viewport > N panel > TexLab`, click on `Export UV Layout and Setup Scene`.
3. This will create a new scene specifically for working with the UV layout of your object.

### Step 3: Working in the UV Layout Scene
1. **View Pass Selection**: Choose the view pass you want to work with from the `TexLab Settings` panel.
   - Available view passes: Physical, Basecolor, Roughness, Metallic, Emission, Normal, Ambient Occlusion.
2. **Render and Update Normal Map**: Render the UV layout and update the normal map.
   - Click on `Render UV Layout and Update Normal Map` in the `TexLab` panel.
3. **Render and Update Images**: Render the UV layout and update all associated images.
   - Click on `Render Full Material for YourObjectName` in the `TexLab` panel.

### Step 4: Applying Materials
1. **Apply Materials to Objects**: Use the `TexLab Materials` panel to apply materials to your object.
   - Select the desired material from the list.
   - Click `Apply To Active` to apply the selected material to the active object.
   - Click `Apply to Selected` to apply the selected material to all selected objects.

## Additional Tools
- **Create New TexLab Material**: Create a new material using the `texLab_master` node group.
  - Click on `New Texlab Material` in the `TexLab Materials` panel.
- **New Normal Mesh**: Create a new mesh object for normal mapping.
  - Click on `New Normal Mesh` in the `TexLab` panel.

## Detailed Functions
- **set_frame**
  - **Description**: Sets the frame for the view pass.

- **save_uv_layout**
  - **Description**: Saves the UV layout of an object to a file.

- **setup_uv_scene**
  - **Description**: Sets up a new scene for the UV layout of an object.

- **render_and_update_normal**
  - **Description**: Renders the UV layout and updates the normal map for a scene.

- **render_and_update_images**
  - **Description**: Renders the UV layout and updates the images for a scene.

- **setup_3d_view**
  - **Description**: Sets up the 3D view for a scene.

- **setup_geometry_nodes**
  - **Description**: Sets up geometry nodes for a scene.
