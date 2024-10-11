# Changelog

1.8.2 - 2024-10-11

- added: GP v2->v3 modifier type strings
- fixed: some error in new GPv3 API propnames

1.8.0 - 2024-10-06

- added: terms for GPv2 to GPv3
- added: checkbox for icon verification toggle
- fixed: broken detection for invalid icon
- changed: 2.7 term search disabled by default

1.7.0 - 2024-09-07

- added: button to directly write the `blender_manifest.toml` aside `__init__.py` (ask to overwrite if already exists)

1.6.0 - 2024-08-24

- added: initial terms check for new grease pencil API (gpv2 -> gpv3) in Blender 4.3
- changed: separate terms toggle for propeties to annotations
- fixed: permission terminology in manifest

1.5.0 - 2024-06-07

- added: button to create manifest.toml text from bl_info in opened text file
- fixed: bad regex on one search/replace string
- changed: code refactor

1.4.1 - 2022-10-03

- fixed: bgl to new gpu draw suggestions

1.4.0 - 2022-10-01

- added: checkbox to separate specific terms related to upgrade from 2.7
- added: 'quoted' method to match term only if it's quoted (usefull for icons)

1.3.0 - 2022-10-01

- changed: converted to multifile (`__init__`) addon 
- added: support for direct regex pattern replace in terms
- added: term update items for deprecated bgl