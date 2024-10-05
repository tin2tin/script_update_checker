## create manifest file from bl_info from init file

import bpy
import re

from bpy.types import Context, OperatorProperties
from .fn import current_text
from pathlib import Path
from time import strftime

def parse_bl_info(text):
    '''return dict of bl_info (as dict)
    None if no bl_info dict found
    '''

    res = re.search(r'bl_info\s?=\s?(\{.*?\})', text, flags=re.DOTALL)
    if not res:
        return
    bl_info_txt = res.group(1)
    bl_info_d = eval(bl_info_txt)

    # for k, v in bl_info_d.items():
    #     print(k, v)
    return bl_info_d


def bl_dict_to_manifest(bl_dict):
    text_list = []
    
    text_list.append('schema_version = "1.0.0"')
    text_list.append('')
    
    fp = bpy.context.space_data.text.filepath

    if fp:
        folder_name = Path(bpy.context.space_data.text.filepath).parent.name
        text_list.append(f'id = "{folder_name}"')
    else:
        text_list.append(f'id = "!folder_name_here!"')

    if version := bl_dict.get("version"):
        version = '.'.join([str(i) for i in version])
        text_list.append(f'version = "{version}"')
    else:
        text_list.append(f'id = "1.0.0"')

    text_list.append(f'name = "{bl_dict.get("name")}"')
    
    text_list.append(f'tagline = "{bl_dict.get("description")}"')


    if author := bl_dict.get("author"):
        text_list.append(f'maintainer = "{author.split(",")[0]}" # Add <mail>')

    text_list.append('type = "add-on"')
    
    text_list.append("""
# Optional: add-ons can list which resources they will require and description:
# * "files" (for access of any filesystem operations)
# * "network" (for internet access)
# * "clipboard" (to read and/or write the system clipboard)
# * "camera" (to capture photos and videos)
# * "microphone" (to capture audio)
# permissions = ["files", "network"])
# [permissions]
# network = "Automatic download"
# files = "Write json data"
""")

    text_list.append(f'website = {bl_dict.get("doc_url")}')
    
    text_list.append('')
    text_list.append('# https://docs.blender.org/manual/en/dev/extensions/tags.html')
    # text_list.append(f'tags = ["Animation", "Sequencer"]')
    text_list.append(f'tags = ["{bl_dict.get("category")}",]')

    text_list.append('blender_version_min = "4.2.0"')
    text_list.append('license = ["SPDX:GPL-2.0-or-later"]')

    text_list.append('')
    text_list.append('# Copyright - Optional: required by some licenses, can have multiple line')
    text_list.append(f'copyright = ["{strftime("%Y")} {bl_dict.get("author")}",]')

    text_list.append("""
# Optional list of supported platforms. If omitted, the extension will be available in all operating systems.
# platforms = ["windows-amd64", "macos-arm64", "linux-x86_64"]
# Other supported platforms: "windows-arm64", "macos-x86_64"

# Optional: bundle 3rd party Python modules.
# https://docs.blender.org/manual/en/dev/extensions/python_wheels.html
# wheels = [
#   "./wheels/hexdump-3.3-py3-none-any.whl",
#   "./wheels/jsmin-3.0.1-py3-none-any.whl"
# ]

# Optional: build setting.
# https://docs.blender.org/manual/en/dev/extensions/command_line_arguments.html#command-line-args-extension-build
# [build]
# paths_exclude_pattern = [
#   "/.git/"
#   "__pycache__/"
# ]
""")

    return '\n'.join(text_list)

class TEXT_OT_convert_bl_info_to_manifest(bpy.types.Operator):
    bl_idname = "text.convert_bl_info_to_manifest"
    bl_label = "convert bl_info to manifest"
    bl_description = "Convert bl_info to blender_manifest.toml format and save to clipboard or create file"
    bl_options = {"REGISTER", "INTERNAL"}

    write_on_disk : bpy.props.BoolProperty(default=False, options={'SKIP_SAVE'})

    @classmethod
    def description(cls, context, properties):
        if properties.write_on_disk:
            return f"Convert bl_info and save into a blender_manifest.toml file\
                \nCurrent file needs to be saved on disk"
        else:
            return f"Convert bl_info in current file to a manifest formatting and save to clipboard\
                \nNeed to be placed in a file blender_manifest.toml"

    def invoke(self, context, event):
        if not context.area.spaces.active.text:
            self.report({'ERROR'}, 'No text in area')
            return {"CANCELLED"}

        if not self.write_on_disk:
            return self.execute(context)
        
        if not context.area.spaces.active.text.filepath:
            self.report({'ERROR'}, 'Current text is not saved on disk')
            return {"CANCELLED"}
        
        self.manifest_path = Path(context.area.spaces.active.text.filepath).parent / 'blender_manifest.toml'
        if self.manifest_path.exists():
            return context.window_manager.invoke_props_dialog(self, width=500)
            
        return self.execute(context)
    
    def draw(self, context):
        layout=self.layout
        # layout.use_property_split = True
        col = layout.column()
        col.label(text='"blender_manifest.toml" file already exists !')
        col.label(text="Overwrite file ?")
        col.separator()
        col.label(text=str(self.manifest_path))

    def execute(self, context):
        text = current_text(context)
        if not text:
            self.report({'ERROR'}, 'No text to parse')
            return {'CANCELLED'}
        
        bl_dict = parse_bl_info(text)
        if not bl_dict:
            self.report({'ERROR'}, 'Could not find (or parse) bl_info')
            return {'CANCELLED'}

        manifest_text = bl_dict_to_manifest(bl_dict)
        print('--- text to use in blender_manifest.toml in addon root folder ---')
        print(manifest_text)

        if self.write_on_disk:
            with self.manifest_path.open('w') as fd:
                fd.write(manifest_text)
            self.report({'INFO'}, f'manifest file written at: {self.manifest_path}')
        else:
            bpy.context.window_manager.clipboard = manifest_text
            self.report({'INFO'}, 'Text saved to cliboard, paste in a "blender_manifest.toml" file')
        return {"FINISHED"}

classes = (
    TEXT_OT_convert_bl_info_to_manifest,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
