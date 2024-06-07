import re, bpy
from bpy.props import IntProperty, StringProperty, BoolProperty

from .fn import current_text
from .terms import TERMS, TERMS_27


def check_files(txt) -> list:

    suggestions = []
    txt = str(txt)
    split_file = txt.split('\n')

    # Collect valid icon names
    current_bl_icons = [
        i for i in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"]
        .enum_items.keys() if i != 'NONE'
    ]

    for i, line in enumerate(split_file, 1):
        if line != '':
            # Check for removed icons
            icon = re.findall(r'icon\s{,2}=\s{,2}(?:\'|\")([A-Z_]+)(?:\'|\")', line)
            if icon not in current_bl_icons and icon != []:
                suggestions.append([int(i), line, icon[0], 'Icon missing. Replace it.'])
                # break
            
            # Check for Terms
            if bpy.context.scene.check_27:
                # add terms relative to upgrade from 2.7
                term_list = TERMS + TERMS_27
            else:
                term_list = TERMS

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

                    print('pattern: ', pattern)
                    print('repl: ', repl)
                    if t[0].split('.')[-1] in ('sub', 'quoted'):
                        string = res.group(0)
                        print('string: ', string)
                        suggestion = re.sub(pattern, repl, string)
                        print('suggestion: ', suggestion)
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

    def execute(self, context):
        filename = bpy.context.space_data.text.filepath
        bpy.context.scene.update_script_name = filename
        ## Create new attribute 
        bpy.types.Scene.update_script = check_files(current_text(context))

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

    line: IntProperty(default=0, options={'HIDDEN'})
    cword: StringProperty(default="", options={'HIDDEN'})
    csuggestion: StringProperty(default="", options={'HIDDEN'})

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
    TEXT_OT_update_script_jump,
    TEXT_OT_update_script_button,
    TEXT_OT_insert_classes_button,
)


def register():
    bpy.types.Scene.check_27 = BoolProperty(
        name='Include 2.7 Terms', default=True,
        description='search for terms specific to blender 2.7 version')
    
    # bpy.types.Scene.update_script = bpy.props.StringProperty() # registered on the fly in operator
    bpy.types.Scene.update_script_name = bpy.props.StringProperty()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    if hasattr(bpy.types.Scene, 'update_script'):
        del bpy.types.Scene.update_script

    # if hasattr(bpy.types.Scene, 'update_script_name'):
    del bpy.types.Scene.update_script_name
    del bpy.types.Scene.check_27
