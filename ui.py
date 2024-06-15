import bpy

class TEXT_PT_show_update_ui(bpy.types.Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Text"
    bl_label = "Update Script"

    @classmethod
    def poll(cls, context):
        return context.area.spaces.active.type == "TEXT_EDITOR" and context.area.spaces.active.text

    def draw(self, context):
        layout = self.layout
        layout.operator("text.insert_classes")
        layout.operator("text.convert_bl_info_to_manifest", icon='COPYDOWN')

        layout.prop(context.scene, 'check_27', text='Include Terms From Blender 2.7')
        layout.operator("text.update_script_button")
        

        if not hasattr(bpy.types.Scene, 'update_script'):
            return
        if context.scene.update_script_name != bpy.context.space_data.text.filepath:
            return

        box = layout.box()
        items = context.scene.update_script
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

classes = (
    TEXT_PT_show_update_ui,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

