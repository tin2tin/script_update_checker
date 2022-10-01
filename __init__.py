'''
Original authors notes:
name: update_check_280.py
author: nBurn
description: Simple script to help prep 2.7x Blender addons for 2.80
version: 0, 1, 2
first released: 2019-09-08
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
    "name": "Script Update Checker",
    "author": "nBurn, tin2tin, Pullusb",
    "version": (1, 3, 0),
    "blender": (3, 3, 0),
    "location": "Text Editor > Sidebar > Text > Update Script",
    "description": "Runs  on current document",
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
    ("ZOOMIN", "ADD"),
    ("ZOOMOUT", "REMOVE"),
    ("NEW", "FILE_NEW"),
    ("BBOX", "SHADING_BBOX"),
    ("POTATO", "SHADING_TEXTURE"),
    ("SMOOTH", "SHADING_RENDERED"),
    ("SOLID", "SHADING_SOLID"),
    ("WIRE", "SHADING_WIRE"),
    ("ORTHO", "XRAY"),
    ("BUTS", "PROPERTIES"),
    ("IMAGE_COL", "IMAGE"),
    ("OOPS", "OUTLINER"),
    ("IPO", "GRAPH"),
    ("SCRIPTWIN", "PREFERENCES"),
    ("CURSOR", "PIVOT_CURSOR"),
    ("ROTATECOLLECTION", "PIVOT_INDIVIDUAL"),
    ("ROTATECENTER", "PIVOT_MEDIAN"),
    ("ROTACTIVE", "PIVOT_ACTIVE"),
    ("FULLSCREEN", "WINDOW"),
    ("LAMP_DATA", "LIGHT_DATA"),
    ("OUTLINER_OB_LAMP", "OUTLINER_OB_LIGHT"),
    ("OUTLINER_DATA_LAMP", "OUTLINER_DATA_LIGHT"),
    ("LAMP_POINT", "LIGHT_POINT"),
    ("LAMP_SUN", "LIGHT_SUN"),
    ("LAMP_SPOT", "LIGHT_SPOT"),
    ("LAMP_HEMI", "LIGHT_HEMI"),
    ("LAMP_AREA", "LIGHT_AREA"),
    ("LAMP", "LIGHT"),
    ("VISIBLE_IPO_ON", "HIDE_OFF"),
    ("VISIBLE_IPO_OFF", "HIDE_ON"),
    ("LINK_AREA", "LINKED"),  #removed
    ("PLUG", "PLUGIN"),  #removed
    ("LINK", "DOT"),  #removed
    ("ORTHO", "VIEW_ORTHO"),  #removed
    ("GAME", "Icon missing. Replace it."),
    ("DOTSUP", "Icon missing. Replace it."),
    ("DOTSDOWN", "Icon missing. Replace it."),
    ("INLINK", "Icon missing. Replace it."),
    ("EDIT", "Icon missing. Replace it."),
    ("RADIO", "Icon missing. Replace it."),
    ("GO_LEFT", "Icon missing. Replace it."),
    ("TEMPERATURE", "Icon missing. Replace it."),
    ("SNAP_SURFACE", "Icon missing. Replace it."),
    ("MANIPUL", "Icon missing. Replace it."),
    ("BORDER_LASSO", "Icon missing. Replace it."),
    ("MAN_TRANS", "Icon missing. Replace it."),
    ("MAN_ROT", "Icon missing. Replace it."),
    ("MAN_SCALE", "Icon missing. Replace it."),
    ("RENDER_REGION", "Icon missing. Replace it."),
    ("RECOVER_AUTO", "Icon missing. Replace it."),
    ("SAVE_COPY", "Icon missing. Replace it."),
    ("OPEN_RECENT", "Icon missing. Replace it."),
    ("LOAD_FACTORY", "Icon missing. Replace it."),
    ("ALIGN", "Icon missing. Replace it."),
    ("SPACE2", "Icon missing. Replace it."),
    ("ROTATE", "Icon missing. Replace it."),
    ("SAVE_AS", "Icon missing. Replace it."),
    ("BORDER_RECT", "Icon missing. Replace it."),
    ("ROTACTIVE", "Icon missing. Replace it."),
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
    ("scene.objects.active", "context.active_object",
     "context.view_layer.objects.active"),
    #("scene.object_bases", "view_layer.objects.active"),
    ("scene.frame_set", "subframe"),
    (".proportional_edit", "use_proportional_edit"),
    ("proportional", "use_proportional_edit"),
    (".label(", ".label(text="),
    (".label", "align, text (keywords)"),
    (".row(True)", ".row(align=True)"),
    (".row(False)", ".row(align=False)"),
    #    ("row", "align (keyword)"),
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
    ("    bpy.utils.register_module(__name__)", """    for i in classes:
        bpy.utils.register_class(i)"""),
    ("    bpy.utils.unregister_module(__name__)", """    for i in classes:
        bpy.utils.unregister_class(i)"""),
    ("register_module", "register_class"),
    #("bl_idname", "only needed for Operator"),
    #("Property", ": (annotation)"),
    (" = StringProperty(", ": StringProperty("),
    (" = BoolProperty(", ": BoolProperty("),
    (" = BoolVectorProperty(", ": BoolVectorProperty("),
    (" = CollectionProperty(", ": CollectionProperty("),
    (" = EnumProperty(", ": EnumProperty("),
    (" = FloatProperty(", ": FloatProperty("),
    (" = FloatVectorProperty(", ": FloatVectorProperty("),
    (" = IntProperty(", ": IntProperty("),
    (" = IntVectorProperty(", ": IntVectorProperty("),
    (" = PointerProperty(", ": PointerProperty("),
    (" = RemoveProperty(", ": RemoveProperty("),
    (" = bpy.props.StringProperty(", ": bpy.props.StringProperty("),
    (" = bpy.props.BoolProperty(", ": bpy.props.BoolProperty("),
    (" = bpy.props.BoolVectorProperty(", ": bpy.props.BoolVectorProperty("),
    (" = bpy.props.CollectionProperty(", ": bpy.props.CollectionProperty("),
    (" = bpy.props.EnumProperty(", ": bpy.props.EnumProperty("),
    (" = bpy.props.FloatProperty(", ": bpy.props.FloatProperty("),
    (" = bpy.props.FloatVectorProperty(", ": bpy.props.FloatVectorProperty("),
    (" = bpy.props.IntProperty(", ": bpy.props.IntProperty("),
    (" = bpy.props.IntVectorProperty(", ": bpy.props.IntVectorProperty("),
    (" = bpy.props.PointerProperty(", ": bpy.props.PointerProperty("),
    (" = bpy.props.RemoveProperty(", ": bpy.props.RemoveProperty("),
    (".prop", "text (keyword)"),
    ("Operator):", "UPPERCASE_OT_snake_case("),
    #    ("Operator", "_OT"),
    ("Panel):", "UPPERCASE_PT_snake_case("),
    #    ("Panel", "_PT"),
    ("Menu):", "UPPERCASE_MT_snake_case("),
    #    ("Menu", "_MT"),
    ("UIList):", "UPPERCASE_UL_snake_case("),
    #    ("UIList", "_UL"),
    ("keymap_items", "name=name_arg"),

    ## Replace obsolete bgl in 3.4
    ("bgl.glEnable(bgl.GL_BLEND)", "gpu.state.blend_set('ALPHA')"),
    ("bgl.glDisable(bgl.GL_BLEND)", "gpu.state.blend_set('NONE')"),
    ("gpu.shader.from_builtin('2D_UNIFORM_COLOR')", "gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')"),
    ("gpu.shader.from_builtin('2D_SMOOTH_COLOR')", "gpu.shader.from_builtin('POLYLINE_SMOOTH_COLOR')"),
    # ("bgl.glLineWidth(1)", "gpu.state.line_width_set(1.0)"),
    ('regex.sub', r'bgl\.glLineWidth\(([a-zA-Z0-9]+)\)', 'gpu.state.line_width_set(\g<1>.0)'), # search bgl.glLineWidth(1)
    # ("bgl.glLineWidth(size)", 'shader.uniform_float("lineWidth", size)'),
    ('regex.sub', r"bgl\.glLineWidth\(([a-zA-Z0-9]+)\)", 'shader.uniform_float("lineWidth", \g<1>.0)'),
    ('regex.sub', r"bgl\.glPointSize\([a-zA-Z0-9]+\)", """gpu.state.program_point_size_set(False)
    gpu.state.point_size_set(\g<1>)"""),

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

    #collect valid icon names
    current_bl_icons = [
        i for i in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"]
        .enum_items.keys() if i != 'NONE'
    ]

    for i, line in enumerate(split_file, 1):
        if line != '':
            # Check for removed icons
            icon = re.findall(r'icon\s{,2}=\s{,2}(?:\'|\")([A-Z_]+)(?:\'|\")', line)
            if icon not in current_bl_icons and icon != []:
                classes.append([int(i), line, icon[0], 'Icon missing. Replace it.'])
                # break
            
            # Check for Terms
            for t in TERMS:
                if t[0].startswith('regex.'):
                    pattern, repl = t[1], t[2]
                    
                    res = re.search(pattern, line):
                    if not res:
                        continue

                    if t[0].endswith('sub'):
                        string = res.group(0)
                        suggestion = re.sub(pattern, repl, string)
                        classes.append([int(i), line, string, suggestion])

                else:
                    if t[0] in line:
                        #print("%4d" % i, line, '||', t[0], '-', t[1])
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


class TEXT_OT_insert_classes_button(bpy.types.Operator):
    """Insert collection of classes"""
    bl_idname = "text.insert_classes"
    bl_label = "Insert Classes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        st = context.space_data
        txt = st.text.as_string()
        if not txt: return []

        classes = []
        tipoclass = "class "

        lines = str(txt).splitlines()

        for i in range(len(lines)):
            line = lines[i]

            ### find classes
            find = line.find(tipoclass)
            if find == 0:
                class_name = line[len(tipoclass):line.find("(")]

                classes.append(class_name)
                #print(line, find, class_name)
                continue
        if len(classes):
            sorted(classes)
            bpy.ops.text.insert(text="classes = (\n")
            for i in range(len(classes)):
                bpy.ops.text.insert(text="    " + str(classes[i]) + ",\n")
            bpy.ops.text.insert(text="    )\n")

        return {'FINISHED'}


class TEXT_PT_show_update_script(bpy.types.Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Text"
    bl_label = "Update Script"

    @classmethod
    def poll(cls, context):
        return context.area.spaces.active.type == "TEXT_EDITOR" and context.area.spaces.active.text

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        layout.operator("text.update_script_button")
        box = layout.box()

        if bpy.types.Scene.update_script_name == bpy.context.space_data.text.filepath:
            items = bpy.types.Scene.update_script
            for it in items:
                cline = it[0]
                cname = it[1]
                cword = it[2]
                csuggestion = it[3]
                box = box.column(align=True)
                row = box.row(align=True)
                row.alignment = 'LEFT'
                row.label(text="%4d " % cline)
                prop = row.operator(
                    "text.update_script_jump",
                    text="%s -> %s" % (cword, csuggestion),
                    emboss=False)
                prop.line = int(cline)
                prop.cword = str(cword)
                prop.csuggestion = str(csuggestion)
                row.label(text="")
        layout.operator("text.insert_classes")


class TEXT_OT_update_script_jump(bpy.types.Operator):
    """Jump to line"""
    bl_idname = "text.update_script_jump"
    bl_label = "Update_script Jump"

    line: IntProperty(default=0, options={'HIDDEN'})
    cword: StringProperty(default="", options={'HIDDEN'})
    csuggestion: StringProperty(default="", options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        line = self.line
        cword = self.cword
        csuggestion = self.csuggestion

        if line > 0:
            bpy.ops.text.jump(line=line)
            bpy.context.space_data.find_text = cword
            bpy.context.space_data.replace_text = csuggestion
            bpy.ops.text.find()
        self.line = -1

        return {'FINISHED'}


classes = (
    TEXT_PT_show_update_script,
    TEXT_OT_update_script_jump,
    TEXT_OT_update_script_button,
    TEXT_OT_insert_classes_button,
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
