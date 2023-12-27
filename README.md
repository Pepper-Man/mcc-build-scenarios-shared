# mcc-build-scenarios-shared
Python script for streamlining the process of building maps with shared resources.
Currently supports ALL titles in MCC, with the exception of CE.

# Requirements
[Python](https://www.python.org/) - preferably 3.10.6 or newer, older versions not tested

# Tool Usage (Normal)
* Place the .py file somewhere on your pc (don't put it in a protected folder!).
* Run the .py file from CMD with **py mcc_build_scenarios_shared.py**.
* Choose the engine you want to build scenarios for with the drop-down menu.
* Click "Add Scenario", and browse to and select your scenario file.
* Add more scenarios in the same way.
* If you wish to remove a scenario from the list, click it (it will be highlighted in blue), and use the "Remove Selected Scenario" button.
* Once you have added all of the scenarios you wish to compile together using shared resources, hit "Compile Scenarios!".
* This process will take a fairly long time. You can monitor the progress in the CMD window.
* The tool will notify you with a message once the process completes successfully.

# Tool Usage (AllMaps.txt)
* This tool now provides the option of using a text file that specifies the scenarios to compile. Use this if you don't want to have to manually add lots of scenarios in the tool the "normal" way if you are having to do it often during testing.
* Create or edit a file named **AllMaps.txt** in the root folder of the relevant editing kit.
* Some engines (H3, ODST) already provide this file, so you can edit it to suit your needs. Others do not, and so you will need to create this txt file yourself.
* Simply write the tags-relative path to the scenario (no file extension), with each scenario on a new line.
* For example, **levels\multi\shrine\shrine**
* Run this tool.
* Tick "Use AllMaps.txt".
* Click "Choose AllMaps.txt". Navigate to the relevant file and select it. It must be named correctly, and in an editing kit folder.
* You will see the filepath for the txt in the box above. Hit the compile button when ready.
* If one or more of the filepaths provided in the AllMaps.txt are invalid/wrong, you will be notified.

# Shared map usage with Excession (Steam Workshop)
* The shared files (shared.map, campaign.map, singleplayer_shared.map etc) need to be placed in a special folder to act as an override for MCC workshop mods.
* This requires mirroring MCC's folder setup for the specific engine, within your mod's folder.
* For example, shared files for Halo 3 **DO NOT** go in "your_mod_folder\maps" with the level map files, but instead need to be placed into "your_mod_folder\halo3\maps".
* Be sure to check the folder structure for each engine. For example, H2 uses "your_mod_folder\halo2\h2_maps_win64_dx11".
* These shared files will get automatically uploaded via Excession and used by your mod, with no further setup needed.

# Additional Notes
* This tool relies on your editing kit folder name to function correctly, to avoid having to manually specify each of their locations. If you have changed the name of your editing kit folder(s), this tool will break.
* Halo 2 shared maps are now supported by MCC as of the September 19th 2023 update. The .map and .dat files are required (put these into your mod folder's "h2_maps_win64_dx11" folder), the .bin files are not required (thanks to Arttumiro for testing this).
