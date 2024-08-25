### Terms for search and replace suggestions

## direct word:
# suggestion for first and second element in tuples

## if first element is 'regex.quoted':
# second and third element are still direct words but only matched if quoted in text

## if first element is 'regex.sub':
# second element is a regex pattern
# it will be use to search and 'sub' the whole match with the string passed as third
# captured groups, ex: \g<1> ,can be used to transfer elements from matched string.


## Default terms
TERMS = [
    #("scene.object_bases", "view_layer.objects.active"),
    ("INFO_MT_", "TOPBAR_MT_"),
    #("bl_idname", "only needed for Operator"),

    # ("Operator):", "UPPERCASE_OT_snake_case("),
    ### Test on OPS (!no good, need conditions to be usefull!)
    # ('regex.sub',
    #     r"(?:class )?([a-z]*)_([a-z]*)?(\((?:bpy\.types\.)?Operator\):)",
    #     lambda m: r'{}_OT_{}{}'.format(m.group(1).upper(), m.group(2), m.group(3))),

    # ("Panel):", "UPPERCASE_PT_snake_case("),
    # ("Menu):", "UPPERCASE_MT_snake_case("),
    # ("UIList):", "UPPERCASE_UL_snake_case("),
    # ("Operator", "_OT"),
    # ("Panel", "_PT"),
    # ("Menu", "_MT"),
    # ("UIList", "_UL"),
]

## Propeties to annotations instead of assignmet in 3.0+
TERMS_ANNOTATIONS = [
    #("Property", ": (annotation)"),
    ("= StringProperty(", ": StringProperty("),
    ("= BoolProperty(", ": BoolProperty("),
    ("= BoolVectorProperty(", ": BoolVectorProperty("),
    ("= CollectionProperty(", ": CollectionProperty("),
    ("= EnumProperty(", ": EnumProperty("),
    ("= FloatProperty(", ": FloatProperty("),
    ("= FloatVectorProperty(", ": FloatVectorProperty("),
    ("= IntProperty(", ": IntProperty("),
    ("= IntVectorProperty(", ": IntVectorProperty("),
    ("= PointerProperty(", ": PointerProperty("),
    ("= RemoveProperty(", ": RemoveProperty("),
    ("= bpy.props.StringProperty(", ": bpy.props.StringProperty("),
    ("= bpy.props.BoolProperty(", ": bpy.props.BoolProperty("),
    ("= bpy.props.BoolVectorProperty(", ": bpy.props.BoolVectorProperty("),
    ("= bpy.props.CollectionProperty(", ": bpy.props.CollectionProperty("),
    ("= bpy.props.EnumProperty(", ": bpy.props.EnumProperty("),
    ("= bpy.props.FloatProperty(", ": bpy.props.FloatProperty("),
    ("= bpy.props.FloatVectorProperty(", ": bpy.props.FloatVectorProperty("),
    ("= bpy.props.IntProperty(", ": bpy.props.IntProperty("),
    ("= bpy.props.IntVectorProperty(", ": bpy.props.IntVectorProperty("),
    ("= bpy.props.PointerProperty(", ": bpy.props.PointerProperty("),
    ("= bpy.props.RemoveProperty(", ": bpy.props.RemoveProperty("),
]


TERMS_GPU = [
    ## Replace obsolete bgl in 3.4+
    ("import bgl", ""),
    ("bgl.glEnable(bgl.GL_BLEND)", "gpu.state.blend_set('ALPHA')"),
    ("bgl.glDisable(bgl.GL_BLEND)", "gpu.state.blend_set('NONE')"),
    ("bgl.glEnable(bgl.GL_DEPTH_TEST)", "gpu.state.depth_test_set('LESS_EQUAL')"),
    ("bgl.glDisable(bgl.GL_DEPTH_TEST)", "gpu.state.depth_test_set('NONE')"),

    ("gpu.shader.from_builtin('2D_UNIFORM_COLOR')", "gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')"),
    ("gpu.shader.from_builtin('2D_SMOOTH_COLOR')", "gpu.shader.from_builtin('POLYLINE_SMOOTH_COLOR')"),
    
    # ("bgl.glLineWidth(1)", "gpu.state.line_width_set(1.0)"),
    ('regex.sub', r'bgl\.glLineWidth\(([a-zA-Z0-9]+)\)', 'gpu.state.line_width_set(\g<1>.0)'), # search bgl.glLineWidth(1)
    
    # ("bgl.glLineWidth(size)", 'shader.uniform_float("lineWidth", size)'),
    # ('regex.sub', r"bgl\.glLineWidth\(([a-zA-Z0-9]+)\)", 'shader.uniform_float("lineWidth", \g<1>.0)'),
    
    ## two line
    # program_point_size_set: if enabled, the derived point size is taken from the (potentially clipped) shader builtin gl_PointSize.
    # point_size_set(size): Specify the diameter of rasterized points.
    ('regex.sub', r"bgl\.glPointSize\(([a-zA-Z0-9]+)\)", """gpu.state.program_point_size_set(False)
    gpu.state.point_size_set(\g<1>)"""),
]

TERMS_27 = [
    (".prop", "text (keyword)"),
    # (".label(", ".label(text="),
    ('regex.sub', ".label\((?!text=)(.*?)\)", ".label(text=\g<1>)"),

    ("viewport_shade", "shading.type"),
    ("data.meshes.remove", "to_mesh_clear"),
    ("scene.objects.active", "context.active_object",
     "context.view_layer.objects.active"),
    (".draw_type", ".display_type"),
    (".draw_size", ".display_size"),
    ("uv_textures.", "uv_layers."),
    (".transform_apply", "scale="),
    ("view_align", "align='WORLD'"),
    # ("color", "need alpha?"),
    ("keymap_items", "name=name_arg"),
    ("viewnumpad", "view_axis"),
    ("get_rna", "get_rna_type"),
    ("tessface", "loop_triangles"),
    (".ops.delete", "context="),
    ("evaluated_depsgraph_get", "evaluated_get"),
    ("mesh.primitive", "size, layers"),
    ("transform_orientation", "transform_orientation_slots"),
    ("constraint_orientation", "orient_type"),
    ("show_manipulator", "show_gizmo"),
    ("use_weight_color_range", "view.use_weight_color_rang"),
    ("percentage", "factor"),
    ("use_x", "use_axis"),
    ("use_y", "use_axis"),
    ("use_z", "use_axis"),
    ("use_occlude_geometry", "shading.show_xray"),
    ("event_timer_add", "time_step= (keyword)"),
    ("_specials", "_context_menu"),
    ("basis", "noise_basis= (keyword)"),
    ("turbulence_vector", "noise_basis= (keyword)"),
    ("dupli_group", "instance_collection"),
    (".link(", "active_layer_collection"),
    ("scene.objects.unlink(", "collection.objects.unlink("),
    ("wm.addon_", "preferences"),
    ("object.hide", "object.hide_viewport"),
    (".Group(", ".Collection("),
    (".groups", ".collections"),
    ("snap_element", "snap_elements"),
    ("tweak_threshold", "drag_threshold"),
    ("cursor_location", "cursor.location"),
    (".pivot_point", "transform_pivot_point"),
    ("scene.frame_set", "subframe"),
    (".proportional_edit", "use_proportional_edit"),
    ("proportional", "use_proportional_edit"),
    ("user_preferences", "preferences"),
    ("scene_update_pre", "depsgraph_update_pre"),
    ("scene_update_post", "depsgraph_update_post"),
    ("scene.update", "view_layer.update()"),
    ("frame_set", "subframe= (keyword)"),

    ## objects
    # ("Lamp", "light"),
    # ("lamp", "light"),
    ("show_x_ray", "show_in_front"),
    ("popup_menu", "title (keyword)"),
    (".operator", "text (keyword)"),
    ('regex.sub', r"\b(L|l)amp(\b|\.)", r"light\2"),
    (".select", "obj.select_set()"),
    ("backdrop_", "backdrop_offset"),

    ("header_text_set", "_set(None)"),
    ## registers
    ("    bpy.utils.register_module(__name__)", """    for i in classes:
        bpy.utils.register_class(i)"""),
    ("    bpy.utils.unregister_module(__name__)", """    for i in classes:
        bpy.utils.unregister_class(i)"""),
    ("register_module", "register_class"),
    
    ## old icons
    ('regex.quoted', "TOOLS", "UI"), 
    # equivalent to # ('regex.sub', r"('|\")TOOLS(\1)", "\g<1>UI\g<2>"),
    ('regex.quoted', "ZOOMIN", "ADD"),
    ('regex.quoted', "ZOOMOUT", "REMOVE"),
    ('regex.quoted', "NEW", "FILE_NEW"),
    ('regex.quoted', "BBOX", "SHADING_BBOX"),
    ('regex.quoted', "POTATO", "SHADING_TEXTURE"),
    ('regex.quoted', "SMOOTH", "SHADING_RENDERED"),
    ('regex.quoted', "SOLID", "SHADING_SOLID"),
    ('regex.quoted', "WIRE", "SHADING_WIRE"),
    ('regex.quoted', "ORTHO", "XRAY"),
    ('regex.quoted', "BUTS", "PROPERTIES"),
    ('regex.quoted', "IMAGE_COL", "IMAGE"),
    ('regex.quoted', "OOPS", "OUTLINER"),
    ('regex.quoted', "IPO", "GRAPH"),
    ('regex.quoted', "SCRIPTWIN", "PREFERENCES"),
    ('regex.quoted', "CURSOR", "PIVOT_CURSOR"),
    ('regex.quoted', "ROTATECOLLECTION", "PIVOT_INDIVIDUAL"),
    ('regex.quoted', "ROTATECENTER", "PIVOT_MEDIAN"),
    ('regex.quoted', "ROTACTIVE", "PIVOT_ACTIVE"),
    ('regex.quoted', "FULLSCREEN", "WINDOW"),
    ('regex.quoted', "LAMP_DATA", "LIGHT_DATA"),
    ('regex.quoted', "OUTLINER_OB_LAMP", "OUTLINER_OB_LIGHT"),
    ('regex.quoted', "OUTLINER_DATA_LAMP", "OUTLINER_DATA_LIGHT"),
    ('regex.quoted', "LAMP_POINT", "LIGHT_POINT"),
    ('regex.quoted', "LAMP_SUN", "LIGHT_SUN"),
    ('regex.quoted', "LAMP_SPOT", "LIGHT_SPOT"),
    ('regex.quoted', "LAMP_HEMI", "LIGHT_HEMI"),
    ('regex.quoted', "LAMP_AREA", "LIGHT_AREA"),
    ('regex.quoted', "LAMP", "LIGHT"),
    ('regex.quoted', "VISIBLE_IPO_ON", "HIDE_OFF"),
    ('regex.quoted', "VISIBLE_IPO_OFF", "HIDE_ON"),
    ('regex.quoted', "LINK_AREA", "LINKED"),  #removed
    ('regex.quoted', "PLUG", "PLUGIN"),  #removed
    ('regex.quoted', "LINK", "DOT"),  #removed
    ('regex.quoted', "ORTHO", "VIEW_ORTHO"),  #removed
]


## Update from GPv2 to GPv3 API in Blender 4.3
TERMS_GP3 = [
    (".info", ".name"), # Layer name
    ('regex.sub', r"\.co(?!\w)", ".position"),
    (".grease_pencil_modifiers", ".modifiers"), # Layer name
    ('regex.quoted', "GPENCIL", "GREASEPENCIL"), # Type
    ('regex.quoted', "PAINT_GPENCIL", "PAINT_GREASE_PENCIL"), # paint context
    (".active_frame", ".current_frame()"),
    (".strokes", ".drawing.strokes"),
    (".use_cyclic", ".use_cyclic"),
    ("_gpencil_", "_greasepencil_"),
    ("strokes.new()", "-> drawing.add_curves()"),
]
    # ("VIEW3D_MT_gpencil_edit_context_menu", "VIEW3D_MT_greasepencil_edit_context_menu"),
    ## All at once ?

#terms = str(TERMS).split('\n')
#for t in terms:
#    print('("' + t + '", ' + '"foo"),')