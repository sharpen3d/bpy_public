import bpy
import subprocess

bl_info = {
    "name": "MacOS Terminal Launcher",
    "blender": (2, 80, 0),
    "category": "System",
    "author": "Luke Stilson",
    "version": (1, 0, 0),
    "location": "File > Launch via Terminal",
    "warning": "MacOS Only, verified on Sonoma 14.4.1 | Close and Reopen Blender after activating plugin before using the terminal launcher to confirm plugin settings",
    "doc_url": "http://sharpen3d.com",
    "support": "COMMUNITY"
}

def run_blender_in_terminal():
    blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
    script = (
        f'tell application "Terminal"\n'
        f'    do script "{blender_path}"\n'
        f'    activate\n'
        f'end tell'
    )
    subprocess.run(["osascript", "-e", script])

class ConfirmSaveOperator(bpy.types.Operator):
    bl_idname = "wm.confirm_save"
    bl_label = "New Blender Instance With Terminal"

    def execute(self, context):
        run_blender_in_terminal()
        bpy.ops.wm.quit_blender('EXEC_DEFAULT')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        self.layout.label(text="By Selecting OK, current changes will be lost")
        self.layout.operator("wm.keep_open", text="Keep Current Instance Open")

class KeepOpen(bpy.types.Operator):
    bl_idname = "wm.keep_open"
    bl_label = "Keep Open"
    bl_description = "Launch a new instance of blender with terminal, and keep the current file open in parallel"

    def execute(self, context):
        run_blender_in_terminal()
        return {'FINISHED'}

class OpenBlenderOperator(bpy.types.Operator):
    bl_idname = "wm.open_blender_terminal"
    bl_label = "New Instance From Terminal"
    bl_description = "Discard changes in current file and open a new project with terminal window"

    def execute(self, context):
        bpy.ops.wm.confirm_save('INVOKE_DEFAULT')
        return {'FINISHED'}

def add_menu_item(self, context):
    self.layout.operator(OpenBlenderOperator.bl_idname)

def register():
    bpy.utils.register_class(OpenBlenderOperator)
    bpy.utils.register_class(ConfirmSaveOperator)
    bpy.utils.register_class(KeepOpen)
    bpy.types.TOPBAR_MT_file_new.append(add_menu_item)

def unregister():
    bpy.utils.unregister_class(OpenBlenderOperator)
    bpy.utils.unregister_class(ConfirmSaveOperator)
    bpy.utils.unregister_class(KeepOpen)
    bpy.types.TOPBAR_MT_file_new.remove(add_menu_item)

if __name__ == "__main__":
    register()