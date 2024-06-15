import bpy

def current_text(context):
    if context.area.type == "TEXT_EDITOR":
        return context.area.spaces.active.text.as_string()
