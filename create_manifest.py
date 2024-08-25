## create manifest file from bl_info from init file

import bpy
import re
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
    bl_description = "Convert bl_info to manifest.toml format and save to clipboard"
    bl_options = {"REGISTER", "INTERNAL"}

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
        print('--- text to use in manifest.toml in addon root folder ---')
        print(manifest_text)
        
        bpy.context.window_manager.clipboard = manifest_text
        self.report({'INFO'}, 'Text saved to cliboard, paste in a "manifest.toml" file')
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
