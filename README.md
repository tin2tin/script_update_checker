# Script Update Checker
Check scripts for functions which needs to be updated to the latest Blender.

## Where

Find it in the Text Editor Sidebar.

# How

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

## About

nBurn writes:
"Add-on update helper script

I found I was regularly overlooking outdated code when doing add-on updates, so I made a very basic helper script to speed up the update process. This script goes through an add-on files and look for lines that might have outdated 2.7x code. If possibly outdated code is found, the code and its line number are printed in the console along with a small note on what to look at.

Please keep in mind this script will not catch everything and tends to generate a lot of false positives, but it has saved me quite a bit of time when updating add-ons for 2.8."

His commandline version is found here: 
https://blenderartists.org/t/2-80-cheat-sheet-for-updating-add-ons/1148974/48