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
        row = layout.row(align=True)

        row.operator("text.convert_bl_info_to_manifest", text='bl_info to manifest', icon='COPYDOWN')
        row.operator("text.convert_bl_info_to_manifest", text='Create Manifest File', icon='FILE_TICK').write_on_disk = True

        col = layout.column()
        settings = context.scene.script_updater_props
        col.label(text='Include Terms:')
        col.prop(settings, 'check_27', text='From Blender 2.7')
        col.prop(settings, 'check_annotation', text='Properties To Annotation')
        col.prop(settings, 'check_gpv3', text='GPv2 to GPv3')
        
        layout.operator("text.update_script_button")
        
        # wm = bpy.context.window_manager
        if not hasattr(bpy.types.Scene, 'update_script'):
            return
        if context.scene.script_updater_props.script_name != bpy.context.space_data.text.filepath:
            return

        box = layout.box()
        # items = wm.update_script
        items = context.scene.update_script
        for it in items:
            cline = it[0] # Line number
            cname = it[1] # Original line
            cword = it[2] # Matched words
            csuggestion = it[3] # Replacement

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

