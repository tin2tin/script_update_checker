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
        # layout.label(text='Tools:')
        layout.operator("text.insert_classes")
        row = layout.row(align=True)

        row.operator("text.convert_bl_info_to_manifest", text='bl_info to manifest', icon='COPYDOWN')
        row.operator("text.convert_bl_info_to_manifest", text='Create Manifest File', icon='FILE_TICK').write_on_disk = True

        col = layout.column(align=True)
        settings = context.scene.script_updater_props
        col.label(text='Include Terms:')
        col.prop(settings, 'check_27', text='From Blender 2.7')
        col.prop(settings, 'check_annotation', text='Properties To Annotation')
        col.prop(settings, 'check_gpv3', text='GPv2 to GPv3')
        col.prop(settings, 'check_icons', text='Icon Names')
        col.prop(settings, 'sequencer', text='Sequencer')

        col.separator()
        col.label(text='Updates:')
        
        row = col.row(align=True)
        row.prop(settings, 'auto_refresh', text='Auto Refresh')

        hint = row.operator("hint.info_note", text='', icon='QUESTION', emboss=False)
        hint.title = "Updater System Infos"
        hint.text = "Click on suggestion text to jump on searched term\
            \nClick on line number to jump and replace immediately (same as Ctrl+ click on text)\
            \nAuto Refresh: Automatically re-run check after replace (usualy faster and safer)"

        layout.operator("text.update_script_button", icon='FILE_REFRESH')
        
        # wm = bpy.context.window_manager
        if not hasattr(bpy.types.Scene, 'update_script'):
            return
        if context.scene.script_updater_props.script_name != bpy.context.space_data.text.filepath:
            return

        box = layout.box()
        # items = wm.update_script
        items = context.scene.update_script
        if not items:
            box.label(text="No replace suggestion", icon='CHECKMARK')
            return

        for it in items:
            cline = it[0] # Line number
            cname = it[1] # Original line
            cword = it[2] # Matched words
            csuggestion = it[3] # Replacement

            box = box.column(align=True)
            row = box.row(align=True)
            row.alignment = 'LEFT'

            ## button to replace
            prop = row.operator(
                "text.update_script_jump",
                text=str(cline),
                # text="",
                # icon='BACK',
                emboss=True) # EVENT_LEFT_ARROW
            prop.line = int(cline)
            prop.cword = str(cword)
            prop.csuggestion = str(csuggestion)
            prop.replace = True

            # line
            # row.label(text="%4d " % cline)

            ## suggestion and 
            prop = row.operator(
                "text.update_script_jump",
                text="%s -> %s" % (cword, csuggestion),
                emboss=False)
            prop.line = int(cline)
            prop.cword = str(cword)
            prop.csuggestion = str(csuggestion)
            

            # row.label(text="")

def show_message_box(_message = "", _title = "Message Box", _icon = 'INFO'):
    '''Show message box with element passed as string or list
    if _message if a list of lists:
        if sublist have 2 element:
            considered a label [text, icon]
        if sublist have 3 element:
            considered as an operator [ops_id_name, text, icon]
        if sublist have 4 element:
            considered as a property [object, propname, text, icon]
    '''

    def draw(self, context):
        layout = self.layout
        for l in _message:
            if isinstance(l, str):
                layout.label(text=l)
            elif len(l) == 2: # label with icon
                layout.label(text=l[0], icon=l[1])
            elif len(l) == 3: # ops
                layout.operator_context = "INVOKE_DEFAULT"
                layout.operator(l[0], text=l[1], icon=l[2], emboss=False) # <- highligh the entry
            elif len(l) == 4: # prop
                row = layout.row(align=True)
                row.label(text=l[2], icon=l[3])
                row.prop(l[0], l[1], text='') 
    
    if isinstance(_message, str):
        _message = [_message]
    bpy.context.window_manager.popup_menu(draw, title = _title, icon = _icon)

class HINT_OT_info_note(bpy.types.Operator):
    bl_idname = "hint.info_note"
    bl_label = "Info Note"
    bl_description = "Info Note"
    bl_options = {"REGISTER", "INTERNAL"}

    text : bpy.props.StringProperty(default='', options={'SKIP_SAVE'})
    title : bpy.props.StringProperty(default='Help', options={'SKIP_SAVE'})
    icon : bpy.props.StringProperty(default='INFO', options={'SKIP_SAVE'})

    @classmethod
    def description(cls, context, properties):
        return properties.text

    def execute(self, context):
        ## Split text in list of lines
        lines = self.text.split('\n')
        show_message_box(_message=lines, _title=self.title, _icon=self.icon)
        return {"FINISHED"}

classes = (
    HINT_OT_info_note,
    TEXT_PT_show_update_ui,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

