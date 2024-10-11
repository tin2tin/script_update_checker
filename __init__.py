'''
authors notes:
name: update_check_280.py
author: nBurn
description: Simple script to help prep 2.7x Blender addons for 2.80
version: 0, 1, 2
first released: 2019-09-08
UI added: 2019-10-26 by tin2tin
Updated 2019/2022 by Samuel Bernou

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
    "author": "nBurn, tin2tin, Samuel Bernou",
    "version": (1, 8, 1),
    "blender": (3, 3, 0),
    "location": "Text Editor > Sidebar > Text > Update Script",
    "description": "Runs check on current document for updates",
    "warning": "",
    "wiki_url": "",
    "category": "Text Editor",
}

from . import (
    update_check,
    create_manifest,
    ui,
    )

modules = (
    update_check,
    create_manifest,
    ui,
    )

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()
