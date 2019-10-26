'''
name: update_check_280.py
author: nBurn
description: Simple script to help prep 2.7x Blender addons for 2.80
version: 0, 0, 0
first released: 2019-09-08
last updated: 2019-09-08
UI added: 2019-10-26 by tin2tin

LICENSE (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Except as contained in this notice, the name of the author shall not be used
in advertising or otherwise to promote the sale, use or other dealings in
this Software without prior written authorization.

'''

bl_info = {
    "name": "Update Script",
    "author": "nBurn, tin2tin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Text Editor > Sidebar > Update Script",
    "description": "Runs 2.80 update checks on current document",
    "warning": "",
    "wiki_url": "",
    "category": "Text Editor",
}

TERMS = (
    ("color", "need alpha?"),
    ("viewnumpad", "view_axis"),
    ("get_rna", "get_rna_type"),
    ("viewport_shade", "shading.type"),
    ("TOOLS", "UI"),
    ("LAMP", "light"),
    ("Lamp", "light"),
    ("lamp", "light"),
    (".select", "obj.select_set()"),
    ("backdrop_", "backdrop_offset"),
    ("tessface", "loop_triangles"),
    ("user_preferences", "preferences"),
    (".ops.delete", "context="),
    #("evaluated_get", "foo"),
    ("evaluated_depsgraph_get", "evaluated_get"),
    ("data.meshes.remove", "to_mesh_clear"),
    ("scene.objects.active", "context.active_object", "context.view_layer.objects.active"),
    #("scene.object_bases", "view_layer.objects.active"),
    ("scene.frame_set", "subframe"),
    (".proportional_edit", "use_proportional_edit"),
    ("proportional", "use_proportional_edit"),
    (".prop", "text (keyword)"),
    (".label", "align, text (keywords)"),
    ("row", "align (keyword)"),
    ("show_x_ray", "show_in_front"),
    ("popup_menu", "title (keyword)"),
    (".operator", "text (keyword)"),
    ("object.hide", "object.hide_viewport"),
    (".Group(", ".Collection("),
    (".groups", ".collections"),
    ("dupli_group", "instance_collection"),
    (".link(", "active_layer_collection"),
    ("scene.objects.unlink(", "collection.objects.unlink("),
    (".draw_type", ".display_type"),
    (".draw_size", ".display_size"),
    ("uv_textures.", "uv_layers."),
    (".transform_apply", "scale="),
    ("view_align", "align='WORLD'"),
    ("mesh.primitive", "size, layers"),
    ("transform_orientation", "transform_orientation_slots"),
    ("constraint_orientation", "orient_type"),
    ("show_manipulator", "show_gizmo"),
    ("use_weight_color_range", "view.use_weight_color_rang"),
    ("wm.addon_", "preferences"),
    ("percentage", "factor"),
    ("use_x", "use_axis"),
    ("use_y", "use_axis"),
    ("use_z", "use_axis"),
    ("scene_update_pre", "depsgraph_update_pre"),
    ("scene_update_post", "depsgraph_update_post"),
    ("scene.update", "view_layer.update()"),
    ("use_occlude_geometry", "shading.show_xray"),
    ("event_timer_add", "time_step= (keyword)"),
    ("frame_set", "subframe= (keyword)"),
    ("INFO_MT_", "TOPBAR_MT_"),
    ("_specials", "_context_menu"),
    ("basis", "noise_basis= (keyword)"),
    ("turbulence_vector", "noise_basis= (keyword)"),
    ("tweak_threshold", "drag_threshold"),
    ("cursor_location", "cursor.location"),
    ("snap_element", "snap_elements"),
    (".pivot_point", "transform_pivot_point"),
    ("header_text_set", "_set(None)"),
    ("register_module", "register_class"),
    #("bl_idname", "only needed for Operator"),
    ("Property", ": (annotation)"),
    ("Operator", "_OT"),
    ("Panel", "_PT"),
    ("Menu", "_MT"),
    ("UIList", "_UL"),
    ("keymap_items", "name=name_arg"),
)

#terms = str(TERMS).split('\n')
#for t in terms:
#    print('("' + t + '", ' + '"foo"),')

import os, sys, re, bpy
from bpy.props import PointerProperty, IntProperty, StringProperty, BoolProperty


def check_files(txt):

    classes = []
    txt = str(txt)
    split_file = txt.split('\n')

    for i, line in enumerate(split_file, 1):
        if line != '':
            for t in TERMS:
                if t[0] in line:
                    print("%4d" % i, line, '||', t[0], '-', t[1])
                    classes.append([int(i), line, t[0], t[1]])
                    break
    return classes


def current_text(context):
    if context.area.type == "TEXT_EDITOR":
        return context.area.spaces.active.text.as_string()


class TEXT_OT_update_script_button(bpy.types.Operator):
    """Run Update Script"""
    bl_idname = "text.update_script_button"
    bl_label = "Run Update Script Check"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        filename = bpy.context.space_data.text.filepath
        bpy.types.Scene.update_script_name = filename
        bpy.types.Scene.update_script = check_files(current_text(context))

        return {'FINISHED'}


class TEXT_PT_show_update_script(bpy.types.Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Update Script"
    bl_label = "Update Script"

    @classmethod
    def poll(cls, context):
        return context.area.spaces.active.type == "TEXT_EDITOR" and context.area.spaces.active.text

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        layout.operator("text.update_script_button")
        if bpy.types.Scene.update_script_name == bpy.context.space_data.text.filepath:
            items = bpy.types.Scene.update_script
            for it in items:
                cline = it[0]
                cname = it[1]
                cword = it[2]
                layout = layout.column(align=True)
                row = layout.row(align=True)
                row.alignment = 'LEFT'
                row.label(text="%4d:" % cline)
                prop = row.operator("text.update_script_jump", text="%s -> %s" % (cword, csuggestion), emboss=False)
                prop.line = int(cline)
                row.label(text="")


class TEXT_OT_update_script_jump(bpy.types.Operator):
    """Jump to line"""
    bl_idname = "text.update_script_jump"
    bl_label = "Update_script Jump"

    line: IntProperty(default=0, options={'HIDDEN'})
    character: IntProperty(default=0, options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        line = self.line
        character = self.character

        if line > 0:
            bpy.ops.text.jump(line=line)
        self.line = -1

        return {'FINISHED'}


classes = (
    TEXT_PT_show_update_script,
    TEXT_OT_update_script_jump,
    TEXT_OT_update_script_button,
    )


def register():

    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.update_script = bpy.props.StringProperty()
    bpy.types.Scene.update_script_name = bpy.props.StringProperty()


def unregister():

    for i in classes:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.update_script
    del bpy.types.Scene.update_script_name


if __name__ == "__main__":
    register()
