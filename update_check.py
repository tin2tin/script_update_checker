import re, bpy
from bpy.props import IntProperty, StringProperty, BoolProperty
from bpy.types import Context, OperatorProperties

from .fn import current_text
from .terms import TERMS, TERMS_27, TERMS_ANNOTATIONS, TERMS_GP3

## Code to use property group instead of list to store search-replace items
## (would allow to change "done" value, and show what ahs been replaced, but maybe overkill to add now...)
# class TEXT_PGT_update_script_item(bpy.types.PropertyGroup):
#     line_number : IntProperty(name="Line Number", default=0)
#     line : StringProperty(name="Line", default="")
#     search : StringProperty(name="Search", default="")
#     replace : StringProperty(name="Replace", default="")
#     done : BoolProperty(name="Done", default=False,
#                         description="Show if the term has been replaced")

def check_files(txt) -> list:
    '''Return a list of lists of search-replace match in text:
    [line number (int), original full line, matched string, replacement suggestion]
    '''

    settings = bpy.context.scene.script_updater_props

    # Build Terms
    term_list = []
    
    term_list += TERMS

    if settings.check_27:
        term_list += TERMS_27

    if settings.check_annotation:
        term_list += TERMS_ANNOTATIONS

    if settings.check_gpv3:
        term_list += TERMS_GP3

    suggestions = []
    txt = str(txt)
    split_file = txt.split('\n')

    # Collect valid icon names
    ## Using identifier
    # current_bl_icons = [i.identifier
    #     for i in bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items
    #     if i.identifier != 'NONE']

    ## Using .keys()
    current_bl_icons = [
        i for i in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"]
        .enum_items.keys() if i != 'NONE'
    ]

    for i, line in enumerate(split_file, 1):
        if line != '':
            if settings.check_icons:
                # Check for removed icons
                icon_list = re.findall(r'icon\s{,2}=\s{,2}(?:\'|\")([A-Z_]+)(?:\'|\")', line)
                if icon_list and icon_list[0] not in current_bl_icons:
                    suggestions.append([int(i), line, icon_list[0], 'Icon missing. Replace it.'])
                    # break

            for t in term_list:
                if t[0].startswith('regex.'):
                    pattern, repl = t[1], t[2]
                    
                    if t[0].split('.')[-1] == 'quoted':
                        # Case where Word must be surrounded by quotes to be valid
                        # pattern and repl are actually raw words
                        pattern = r"('|\")" + pattern + r"(\1)"
                        repl = r"\g<1>" + repl + r"\g<2>"
                    
                    res = re.search(pattern, line)
                    if not res:
                        continue

                    # print('pattern: ', pattern) # Dbg
                    # print('repl: ', repl) # Dbg
                    if t[0].split('.')[-1] in ('sub', 'quoted'):
                        string = res.group(0)
                        # print('string: ', string) # Dbg
                        suggestion = re.sub(pattern, repl, string)
                        # print('suggestion: ', suggestion) # Dbg
                        suggestions.append([int(i), line, string, suggestion])
                    

                else:
                    if t[0] in line:
                        #print("%4d" % i, line, '||', t[0], '-', t[1])
                        suggestions.append([int(i), line, t[0], t[1]])
                        break
    return suggestions


class TEXT_OT_update_script_button(bpy.types.Operator):
    """Run Update Script"""
    bl_idname = "text.update_script_button"
    bl_label = "Run Update Script Check"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filename = bpy.context.space_data.text.filepath
        bpy.context.scene.script_updater_props.script_name = filename
        
        ## Create new attribute
        # wm = bpy.context.window_manager
        # wm.update_script = check_files(current_text(context))

        if hasattr(bpy.types.Scene, 'update_script'):
            del bpy.types.Scene.update_script
            # bpy.types.Scene.update_script.clear()
        bpy.types.Scene.update_script = check_files(current_text(context))
        print(len(context.scene.update_script))
        # context.scene.update_script = check_files(current_text(context))
        return {'FINISHED'}


class TEXT_OT_insert_classes_button(bpy.types.Operator):
    """Insert collection of classes"""
    bl_idname = "text.insert_classes"
    bl_label = "Insert Classes"

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

class TEXT_OT_update_script_jump(bpy.types.Operator):
    """Jump to line"""
    bl_idname = "text.update_script_jump"
    bl_label = "Update_script Jump"
    bl_description = 'Click to set search replace on current word + suggestion pair\
    \nCtrl+Click for Ddrect replace and add undo'

    line : IntProperty(default=0, options={'HIDDEN'})
    cword : StringProperty(default="", options={'HIDDEN'})
    csuggestion : StringProperty(default="", options={'HIDDEN'})

    replace : BoolProperty(default=False, options={'SKIP_SAVE'})

    @classmethod
    def description(cls, context, properties) -> str:
        if properties.replace:
            return 'Click to replace current (same as Ctrl + Click on suggestion)'
        return cls.bl_description

    def invoke(self, context, event):
        if not self.replace:
            # if not forced, check if ctrl is pressed
            self.replace = event.ctrl
        return self.execute(context)

    def execute(self, context):
        line = self.line
        cword = self.cword
        csuggestion = self.csuggestion

        if line > 0:
            bpy.ops.text.jump(line=line)
            bpy.context.space_data.find_text = cword
            bpy.context.space_data.replace_text = csuggestion
            bpy.ops.text.find()
            if self.replace:
                bpy.ops.text.replace()
                bpy.ops.text.jump(line=line)

                ## add undo step if replace is done and auto_refresh is off
                bpy.ops.ed.undo_push(message=f"Replace {cword} by {csuggestion}")

                if bpy.context.scene.script_updater_props.auto_refresh:
                    bpy.ops.text.update_script_button()

        self.line = -1

        return {'FINISHED'}


class TEXT_PGT_script_update_checker_settings(bpy.types.PropertyGroup) :
    check_27 : BoolProperty(
        name='Include 2.7 Terms', default=False,
        description='Search for terms specific to blender 2.7 version')
    
    check_annotation : BoolProperty(
        name='Prop To Annotations', default=True,
        description='Search for properties assignement to annotation (= replaced by : on properties since blender 2.8)')
    
    check_gpv3 : BoolProperty(
        name='GPv2 to GPv3', default=True,
        description='Grease pencil API from v2 to v3 (changed at Blender 4.3)')
    
    check_icons : BoolProperty(
        name='Icons Name', default=True,
        description='Check icon name\
            \n(Should use the targeted Blender version for the script!)')

    auto_refresh : BoolProperty(
        name='Auto Refresh', default=True,
        description='Automatically re-run the script when a replace has been made using operator')

    script_name : bpy.props.StringProperty()


classes = (
    # TEXT_PGT_update_script_item, # unused
    TEXT_PGT_script_update_checker_settings,
    TEXT_OT_update_script_jump,
    TEXT_OT_update_script_button,
    TEXT_OT_insert_classes_button,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.script_updater_props = bpy.props.PointerProperty(type = TEXT_PGT_script_update_checker_settings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    if hasattr(bpy.types.Scene, 'script_updater_props'):
        del bpy.types.Scene.script_updater_props

    if hasattr(bpy.types.Scene, 'update_script'):
        del bpy.types.Scene.update_script