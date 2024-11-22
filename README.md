# Script Update Checker
Check scripts for functions which needs to be updated to the latest Blender.

## Where

Find it in the Text Editor Sidebar.

## How

1. Open the script in question in the Text Editor and execute the operator in the sidebar. 
2. All items with issues will be listed in the sidebar. 
3. Click on an issue to go to that line. 
4. Fix the line.

## Addtional feature

In `Update Script` panel you will also find:
- `Insert Classes` : Create a tuple listing *classes* names in current text at cursor position. 
- `bl_info to manifest` : Get infos from *bl_info* in current text and reformat for Blender 4.2+ Extensions info format.  
Text is added to clipboard, ready to paste in a `blender_manifest.toml` file at the root of the addon.  
- `Create manifest file` : Directly write the `blender_manifest.toml` file on disk, in the same folder of the loaded text file (it will ask to overwrite if the manifest already exists)

## GPv2 to GPv3 update notes

Following the full rewrite of Grease pencil shipped in Blender 4.3+, the API terms updater include search and replaces for Grease pencil V2 to V3.
 
Changes and API equivalences are listed in the [official GP migration page](https://developer.blender.org/docs/release_notes/4.3/grease_pencil_migration/).  


The addons works well with the search & replace to update parts of yours script, but of course it does not cover all the things to change.

Also, you might want to affect multiple files at once using an external IDE.  
So here is a list of search and replaces, _regexes_ and extra notes as a complement for the official migration page.  
It's still recommended to apply the replaces one by one to avoid false-positive replace.  

> Note: This is provided "as is", no one is responsible if there are error or if it breaks your script ;)

### Search and replace

|                 | Search                     | Replace            |
| --------------- | -------------------------- | ------------------ |
| layer name      | `.info`                    | `.name`            |
| modifier access | `.grease_pencil_modifiers` | `.modifiers`       |
| active frame    | `.active_frame`            | `.current_frame()` |

#### Regex search and replace

Those marked with `/!\` in _notes_ column must be handled with extra care

> Before replacing _context modes_ below, first replace `mode_set` operator (if any) from `GPENCIL_EDIT` to `EDIT`.  
> This will avoid replacing it by the `context_mode` name by mistake:
> `bpy.ops.object.mode_set(mode='EDIT_GPENCIL')` > to > `bpy.ops.object.mode_set(mode='EDIT')`

|                    | Search                                            | Replace                | Notes                                                            |
| ------------------ | ------------------------------------------------- | ---------------------- | ---------------------------------------------------------------- |
| GP type string     | `('\|")GPENCIL(\1)`                               | `$1GREASEPENCIL$1`     | quotes avoid matching `GPENCIL` within strings                   |
| context modes      | `('\|")(PAINT\|EDIT\|SCULPT\|WEIGHT)_GPENCIL(\1)` | `$1$2_GREASE_PENCIL$1` | `/!\` ops `object.mode_set` use just "EDIT"                        |
| position attribute | `\.co(?!\w)`                                      | `.position`            | `/!\` vertices and fcurvce points still use `.co`                |
| drawing container  | `(?<!drawing)\.strokes`                           | `.drawing.strokes`     | Regex check if 'drawing' keyword is already there                |
| obsolete update    | `.*(?:points\|strokes).update\(\))`               | `\1# \2`               | Comment point/stroke update(), empty the replace field to remove |


#### Modifiers

For most modifier type, just a prefix change, `GP_` becomes `GREASE_PENCIL_`. Here is a regex for those:

search : `('\|")GP_(LATTICE|BUILD|NOISE|TIME|TEXTURE|DASH|ENVELOPE|LENGTH|MIRROR|MULTIPLY|OUTLINE|SIMPLIFY|SUBDIV|ARMATURE|HOOK|OFFSET|SMOOTH|COLOR|OPACITY|TINT|ARRAY)(\1)`  
replace: `$1GP_$2$1`

List of other modifier type with name changed:

| Search                | Replace                                 |
| --------------------- | --------------------------------------- |
| `GP_WEIGHT_PROXIMITY` | `GREASE_PENCIL_VERTEX_WEIGHT_PROXIMITY` |
| `GP_WEIGHT_ANGLE`     | `GREASE_PENCIL_VERTEX_WEIGHT_ANGLE`     |
| `GP_LINEART`          | `LINEART`                               |
| `GP_THICK`            | `GREASE_PENCIL_THICKNESS`               |

> /!\ special case:  `SHRINKWRAP` becomes `GREASE_PENCIL_SHRINKWRAP` but in 4.2 the name was the same for other object type (not GP only), so cannot be batch replaced.

#### Operators

|                     | Blender 4.2                             | Blender 4.3                            |
| ------------------- | --------------------------------------- | -------------------------------------- |
| vertex group assign | `bpy.ops.gpencil.vertex_group_assign()` | `bpy.ops.object.vertex_group_assign()` |


#### bpy.types

| Blender 4.2                            | Blender 4.3                                      |
| -------------------------------------- | ------------------------------------------------ |
| `VIEW3D_MT_edit_gpencil_transform`     | `VIEW3D_MT_transform`                            |
| `VIEW3D_MT_edit_gpencil_stroke`        | `VIEW3D_MT_edit_greasepencil_stroke`             |
| `VIEW3D_MT_brush_gpencil_context_menu` | `VIEW3D_MT_brush_context_menu`                   |
| `GPENCIL_MT_layer_context_menu`        | `GREASE_PENCIL_MT_grease_pencil_add_layer_extra` |
| `GPENCIL_MT_cleanup`                   | `VIEW3D_MT_edit_greasepencil_cleanup`            |
| `VIEW3D_MT_gpencil_edit_context_menu`  | `VIEW3D_MT_greasepencil_edit_context_menu`       |


#### Replace with tweaks needed

|                  | Search            | Replace                                                             | Notes                                                                |
| ---------------- | ----------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Multiframe  mode | `.use_multiedit`  | `context.scene.tool_settings.use_grease_pencil_multi_frame_editing` | Not stored on GP.data anymore, now a scene setting                   |
| Remove Stroke    | `strokes.remove(` | `drawing.remove_strokes(indices=(0,))`                              | Not using a stroke object, but a list of stroke indices in drawing.  |
| Add strokes      | `strokes.new()`   | `drawing.add_strokes([0])`                                          | int sequence: [2,4] will add one stroke with 2 points and one with 4 |



## About Script Update Checker addon

nBurn writes:
"Add-on update helper script

I found I was regularly overlooking outdated code when doing add-on updates, so I made a very basic helper script to speed up the update process. This script goes through an add-on files and look for lines that might have outdated 2.7x code. If possibly outdated code is found, the code and its line number are printed in the console along with a small note on what to look at.

Please keep in mind this script will not catch everything and tends to generate a lot of false positives, but it has saved me quite a bit of time when updating add-ons for 2.8."

His commandline version is found here: 
https://blenderartists.org/t/2-80-cheat-sheet-for-updating-add-ons/1148974/48
