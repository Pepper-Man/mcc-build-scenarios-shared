import os
import glob
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

#-------------------------------------- GLOBAL VARIABLES BEGIN ----------------------------------

h2ek_path = ""
h3ek_path = ""
odstek_path = ""
hrek_path = ""
h4ek_path = ""
h2amp_path = ""

#-------------------------------------- GLOBAL VARIABLES END ------------------------------------

#-------------------------------------- GLOBAL FUNCTIONS BEGIN ----------------------------------

def run_executable_in_another_directory(executable_path, arguments):
    executable_folder = os.path.dirname(executable_path)
    os.chdir(executable_folder)
    arguments.insert(0, str(executable_path))
    subprocess.run(arguments)
    
def update_tasks(progress_var, stage, total_stages, window):
    progress_var.set(stage / total_stages * 100)

#-------------------------------------- GLOBAL FUNCTIONS END ------------------------------------

#-------------------------------------- H2 BEGIN ------------------------------------------------

def h2(scenarios_list, window):
    # Progress bar
    progress_label = tk.Label(window, text="Progress: ")
    progress_label.grid(row=9, column=1, padx=20, pady=5)
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100)
    progress_bar.grid(row=9, column=1, padx=20, pady=5, columnspan=3, sticky="ew")
    update_tasks(progress_var, 0, 5, window)
    window.update()
    
    print("Halo 2")
    
    platform = "win64"
    no_extra_prints = "-batch"
    build_flags = "compress|resource_sharing|multilingual_sounds"
    build_flags_sp = "compress|resource_sharing|multilingual_sounds|remastered_support"
    build_flags_mp = "compress|resource_sharing|multilingual_sounds|mp_tag_sharing"
    
    engine_path = h2ek_path
    tool_exe = os.path.join(engine_path, "tool.exe")
    maps_folder = os.path.join(engine_path, "h2_maps_win64_dx11")
    
    # 1 - Delete everything from maps to avoid stale data corrupting the process
    print("Delete everything from maps to avoid stale data corrupting the process")
    shutil.rmtree(maps_folder, ignore_errors=True)
    update_tasks(progress_var, 1, 5, window)
    window.update()
        
    # 2 - Generate mainmenu.map
    print("Generate mainmenu.map")
    argument_list = [no_extra_prints, "build-cache-file", "scenarios\\ui\\mainmenu\\mainmenu", platform, build_flags]
    run_executable_in_another_directory(tool_exe, argument_list)
    update_tasks(progress_var, 2, 5, window)
    window.update()
    
    # 3 - Generate shared.map
    print("Generate shared.map")
    argument_list = [no_extra_prints, "build-cache-file", "scenarios\\shared\\shared", platform, build_flags]
    run_executable_in_another_directory(tool_exe, argument_list)
    update_tasks(progress_var, 3, 5, window)
    window.update()
    
    # 4 - Generate single_player_shared.map
    print("Generate single_player_shared.map")
    argument_list = [no_extra_prints, "build-cache-file", "scenarios\\shared\\single_player_shared", platform, build_flags]
    run_executable_in_another_directory(tool_exe, argument_list)
    update_tasks(progress_var, 4, 5, window)
    window.update()
    
    # 5 - Generate cache files
    print("Generate cache files")
    for map in scenarios_list:
        if "solo" in map:
            argument_list = [no_extra_prints, "build-cache-file", map, platform, build_flags_sp]
        else:
            argument_list = [no_extra_prints, "build-cache-file", map, platform, build_flags_mp]
        
        run_executable_in_another_directory(tool_exe, argument_list)
        
    update_tasks(progress_var, 5, 5, window)
    window.update()
        
    print("\n\nFinished successfully. Built map files are in \"H2EK\\h2_maps_win64_dx11\"")
    messagebox.showinfo("Success", "Finished successfully. Built map files are in \"H2EK\\h2_maps_win64_dx11\"")

#-------------------------------------- H2 END --------------------------------------------------


#-------------------------------------- H3/ODST/REACH BEGIN -------------------------------------

def preH4(scenarios_list, engine):
    if engine == "Halo 3":
        print("Halo 3")
        engine_path = h3ek_path
    if engine == "Halo 3: ODST":
        print("ODST")
        engine_path = odstek_path
    if engine == "Halo Reach":
        print("Reach")
        engine_path = hrek_path
    
    short_name = os.path.basename(engine_path)
    tool_exe = os.path.join(engine_path, "tool.exe")
    map_languages = os.path.join(engine_path, "AllLanguages.txt")
    maps_folder = os.path.join(engine_path, "maps")
    
    sound_codex = os.path.join(
        engine_path, "cache_builder", "sounds_file_codex.bin")
    dvd_prop_list = os.path.join(
        engine_path, "cache_builder", "dvd_prop_list.txt")
    platform_is_pc = True
    target_platform = "pc"

    LANGUAGE = "english"
    VERSION = "0"
    SHARED_SOUNDS = "use-shared-sounds"
    DEDICATED_SERVER = ""
    USE_FMOD_DATA = "use-fmod-data" if platform_is_pc else ""

    # Create the cache builder folder if necessary
    print("Create the cache builder folder if necessary")
    cache_builder_folder = os.path.join(engine_path, "cache_builder")
    os.makedirs(cache_builder_folder, exist_ok=True)

    # 1 - Delete everything from cache_builder to avoid stale data corrupting the process
    print("Delete everything from cache_builder to avoid stale data corrupting the process")
    shutil.rmtree(cache_builder_folder, ignore_errors=True)

    # 2 - Delete maps and RSA manifests from the maps folder
    print("Delete maps and RSA manifests from the maps folder")
    for file in os.listdir(maps_folder):
        if file.endswith(".map") or file.startswith("security"):
            os.remove(os.path.join(maps_folder, file))

    # 3 Build sound index for all maps
    print("Build sound index for all maps")

    # ODST specific command:
    if engine == "Halo 3: ODST":
        print("Running build-cache-file-cache-sounds-index. This can appear to freeze for a while, please be patient.")
        run_executable_in_another_directory(tool_exe, ["build-cache-file-cache-sounds-index", "shared"])

    for map in scenarios_list:
        if os.path.exists(sound_codex):   
            argument_list = ["build-cache-file-cache-sounds-index", map, "append", target_platform]
            run_executable_in_another_directory(tool_exe, argument_list)
        else:
            argument_list = ["build-cache-file-cache-sounds-index", map, target_platform]
            run_executable_in_another_directory(tool_exe, argument_list)

    # 4 Build sound cache files
    print("Build sound cache files")
    language_files = [LANGUAGE] if platform_is_pc else [
        line.strip() for line in open(map_languages, "r")]

    for language_file in language_files:
        argument_list = ["build-cache-file-cache-sounds", target_platform, language_file, VERSION, USE_FMOD_DATA, DEDICATED_SERVER]
        run_executable_in_another_directory(tool_exe, argument_list)

    # 5 - Generate full shared.map
    print("Generate full shared.map")
    argument_list = ["build-cache-file-cache-shared-first", target_platform, LANGUAGE, VERSION, "optimizable", SHARED_SOUNDS, USE_FMOD_DATA, DEDICATED_SERVER]
    run_executable_in_another_directory(tool_exe, argument_list)

    # 6 - Generate full campaign.map
    print("Generate full campaign.map")
    argument_list = ["build-cache-file-cache-campaign-second", target_platform, LANGUAGE, VERSION, "optimizable", USE_FMOD_DATA, DEDICATED_SERVER]
    run_executable_in_another_directory(tool_exe, argument_list)

    # 7 - Generate intermediate files for levels
    print("Generate intermediate files for levels")

    for map in scenarios_list:
        scenario_relative_path = os.path.join(
            engine_path, "tags", f"{map}.scenario")
        if os.path.exists(scenario_relative_path):
            argument_list = ["build-cache-file-language-version-optimizable-use-sharing", LANGUAGE, VERSION, map, target_platform, SHARED_SOUNDS, USE_FMOD_DATA, DEDICATED_SERVER]
            run_executable_in_another_directory(tool_exe, argument_list)
        else:
            print(f"Missing {scenario_relative_path}")

    # 8 - Create dvd_prop_list.txt
    print("Create prop list")
    with open(dvd_prop_list, "w") as prop_list:
        for map in scenarios_list:
            map_name = os.path.splitext(os.path.basename(map))[0]
            prop_list.write(
                f"..\cache_builder\\to_optimize\\{map_name}.cache_file_resource_gestalt\n")

    # 9 - Copy shared.map and campaign.map to optimize directory
    print("Copy shared.map and campaign.map to optimize directory")
    dest_folder = os.path.join(cache_builder_folder, "to_optimize")
    os.makedirs(dest_folder, exist_ok=True)

    shared_map_src = os.path.join(maps_folder, "shared.map")
    campaign_map_src = os.path.join(maps_folder, "campaign.map")
    language_map_src = os.path.join(maps_folder, f"{LANGUAGE}.map")

    shutil.copy2(shared_map_src, os.path.join(dest_folder, "shared.map"))
    if os.path.exists(campaign_map_src):
        shutil.copy2(campaign_map_src, os.path.join(dest_folder, "campaign.map"))

    if os.path.exists(language_map_src):
        shutil.copy2(language_map_src, os.path.join(
            dest_folder, f"{LANGUAGE}.map"))

    # 10 - Generate shared intermediate files
    print("Generate shared intermediate files")
    argument_list = ["generate-final-shared-layout", dvd_prop_list, target_platform, DEDICATED_SERVER]
    run_executable_in_another_directory(tool_exe, argument_list)

    # 11 - Generate optimized level cache files
    print("Generate optimized level cache files")
    for map in scenarios_list:
        scenario_relative_path = os.path.join(
            engine_path, "tags", f"{map}.scenario")
        if os.path.exists(scenario_relative_path):
            argument_list = ["build-cache-file-generate-new-layout", map, target_platform, USE_FMOD_DATA, DEDICATED_SERVER]
            run_executable_in_another_directory(tool_exe, argument_list)
        else:
            print(f"Missing {scenario_relative_path}")

    # 12 - Generate optimized shared.map
    print("Generate optimized shared.map")
    argument_list = ["build-cache-file-link", "shared", target_platform, USE_FMOD_DATA, DEDICATED_SERVER]
    run_executable_in_another_directory(tool_exe, argument_list)

    # 13 - Generate optimized campaign.map
    print("Generate optimized campaign.map")
    argument_list = ["build-cache-file-link", "campaign", target_platform, USE_FMOD_DATA, DEDICATED_SERVER]
    run_executable_in_another_directory(tool_exe, argument_list)

    print("\n\nFinished successfully. Built map files are in \"" + short_name + "\\maps\"")
    messagebox.showinfo("Success", "Finished successfully. Built map files are in \"" + short_name + "\\maps\"")

#-------------------------------------- H3/ODST/REACH END ---------------------------------------

#-------------------------------------- HALO 4 BEGIN --------------------------------------------

def build_cache_sharing(arg, tool_path):
    run_executable_in_another_directory(tool_path, ["build-cache-file-language-version-optimizable-use-sharing", "english", "0", arg, "pc"])

def generate_new_layout(arg, tool_path):
    fileName = os.path.splitext(os.path.basename(arg))[0]
    run_executable_in_another_directory(tool_path, ["build-cache-file-generate-new-layout", fileName, "pc"])
    
def h4plus(selected_scens, engine):
    
    if engine == "Halo 4":
        print("Halo 4")
        engine_path = h4ek_path
    if engine == "Halo 2: AMP":
        print("H2AMP")
        engine_path = h2amp_path
    
    short_name = os.path.basename(engine_path)
    tool_path = os.path.join(engine_path, "tool.exe")
    
    # Delete old cach_builder folder, remove existing .map files
    shutil.rmtree(os.path.join(engine_path, "cache_builder"), ignore_errors=True)
    files_to_delete = os.path.join(engine_path, "maps", "*.map")
    for f in glob.glob(files_to_delete):
        os.remove(f)
    
    # Build shared and campaign maps
    run_executable_in_another_directory(tool_path, ["build-cache-file-cache-shared-first", "english", "0", "pc"])
    run_executable_in_another_directory(tool_path, ["build-cache-file-cache-campaign-second", "english", "0", "pc"])
    
    for scenario in selected_scens:
        build_cache_sharing(scenario, tool_path)
        
    # Copy maps
    shutil.copy(os.path.join(engine_path, "maps", "shared.map"), os.path.join(engine_path, "cache_builder", "to_optimize"))
    if os.path.exists(os.path.join(engine_path, "maps", "campaign.map")):
        shutil.copy(os.path.join(engine_path, "maps", "campaign.map"), os.path.join(engine_path, "cache_builder", "to_optimize"))
    
    # Remove old dvd_prop_list
    dvd_prop_list = os.path.join(engine_path, "built_dvd_prop_list.txt")
    if os.path.exists(dvd_prop_list):
        os.remove(dvd_prop_list)
        
    for filename in glob.glob(os.path.join(engine_path, "cache_builder\\to_optimize\\*.cache_file_resource_gestalt")):
        with open(dvd_prop_list, "a") as file:
            file.write(f"../cache_builder/to_optimize/{os.path.basename(filename)}\n")
            
    # Build the final sharing layout file
    run_executable_in_another_directory(tool_path, ["generate-final-shared-layout", dvd_prop_list, "pc"])
    
    # Finalise maps
    for filename in glob.glob(os.path.join(engine_path, "cache_builder\\to_optimize\\*.cache_file_resource_gestalt")):
        generate_new_layout(filename, tool_path)
        
    # And relink
    run_executable_in_another_directory(tool_path, ["build-cache-file-link", "shared", "pc"])
    run_executable_in_another_directory(tool_path, ["build-cache-file-link", "campaign", "pc"])
    
    print("\n\nFinished successfully. Built map files are in \"" + short_name + "\\maps\"")
    messagebox.showinfo("Success", "Finished successfully. Built map files are in \"" + short_name + "\\maps\"")

#-------------------------------------- HALO 4 END ----------------------------------------------

def open_scenario_file(text_box, engine):
    global h2ek_path, h3ek_path, odstek_path, hrek_path, h4ek_path, h2amp_path
    
    def add_path():
        text_box.insert(tk.END, file_path + "\n")
    
    file_path = filedialog.askopenfilename(filetypes=[("Scenario Files", "*.scenario")])
    file_path_full = file_path
    if file_path:
        # Extract the desired part of the file path
        file_path = os.path.normpath(file_path)  # Normalize path separators
        index = file_path.find("\\tags\\")
        if index != -1:
            file_path = file_path[index + 6:-9]  # Strip "/tags/" and ".scenario" extension
        
        # Check if filepath is already added
        if text_box.search(file_path, "1.0", tk.END):
            print("Scenario already added")
            messagebox.showwarning("Warning", "Scenario already added, not adding it again!")
        else:
            # Check if filepath is valid for the given engine
            if engine.get() == "Halo 2":
                if "H2EK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if h2ek_path == "":
                        index = file_path_full.find("/H2EK/")
                        if index != -1: 
                            h2ek_path = os.path.normpath(file_path_full[:index + len("/H2EK/")])
                            print(h2ek_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
            elif engine.get() == "Halo 3":
                if "H3EK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if h3ek_path == "":
                        index = file_path_full.find("/H3EK/")
                        if index != -1: 
                            h3ek_path = os.path.normpath(file_path_full[:index + len("/H3EK/")])
                            print(h3ek_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
            elif engine.get() == "Halo 3: ODST":
                if "H3ODSTEK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if odstek_path == "":
                        index = file_path_full.find("/H3ODSTEK/")
                        if index != -1: 
                            odstek_path = os.path.normpath(file_path_full[:index + len("/H3ODSTEK/")])
                            print(odstek_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
            elif engine.get() == "Halo Reach":
                if "HREK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if hrek_path == "":
                        index = file_path_full.find("/HREK/")
                        if index != -1: 
                            hrek_path = os.path.normpath(file_path_full[:index + len("/HREK/")])
                            print(hrek_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
            elif engine.get() == "Halo 4":
                if "H4EK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if h4ek_path == "":
                        index = file_path_full.find("/H4EK/")
                        if index != -1: 
                            h4ek_path = os.path.normpath(file_path_full[:index + len("/H4EK/")])
                            print(h4ek_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
            elif engine.get() == "Halo 2: AMP":
                if "H2AMPEK/tags" not in file_path_full:
                    messagebox.showerror("Error", "Scenario filepath does not look valid for selected engine!")
                else:
                    add_path()
                    if h2amp_path == "":
                        index = file_path_full.find("/H2AMPEK/")
                        if index != -1: 
                            h2amp_path = os.path.normpath(file_path_full[:index + len("/H2AMPEK/")])
                            print(h2amp_path)
                        else:
                            messagebox.showerror("Error", "Please contact the developer, this should not have happened")
                            exit(-3)
    else:
        print("Something has gone horribly wrong here")
        exit(-1)

def remove_selected_line(text_box):
    selected_index = text_box.tag_ranges("highlight")
    if selected_index:
        line_start, line_end = selected_index
        line_content = text_box.get(line_start, line_end)
        text_box.delete(line_start, line_end)
        print("Removed line:", line_content.strip())
        
def compile_scenarios(text_box, engine, window):
    # Check that text box isn't empty
    if text_box.get("1.0", "end-1c") == "":
        print("Empty")
        messagebox.showerror("Error", "No scenarios added. Aborting compile process.")
    else:
        scenarios_list = text_box.get("1.0", "end-1c").splitlines()
        print("Compiling scenarios")
        if engine.get() in ["Halo 3", "Halo 3: ODST", "Halo Reach"]:
            preH4(scenarios_list, engine.get())
        elif engine.get() == "Halo 2":
            h2(scenarios_list, window)
        elif engine.get() in ["Halo 4", "Halo 2: AMP"]:
            h4plus(scenarios_list, engine.get())
        else:
            print("Something else has gone horrifically wrong")
            exit(-2)
        
        
def main():
    global progress_var
    
    def highlight_line(event):
        # Remove the "highlight" tag from any previously highlighted line
        text_box.tag_remove("highlight", "1.0", "end")
        # Add the "highlight" tag to the clicked line
        text_box.tag_add("highlight", "current linestart", "current lineend+1c")
        
    # Window creation
    window = tk.Tk()
    window.title('MCC Build Optimized Maps Tool')
    window.geometry('550x650')
    window.resizable(width=False, height=False)

    # Information header
    header_font = font.Font(size=10, weight='bold')
    info_label = tk.Label(window, text='Supported: H2, H3, ODST, HR, H4, H2AMP', font=header_font)
    info_label.grid(row=0, column=1, padx=5, pady=5)

    # Get engine version
    style = ttk.Style()
    style.theme_use('vista')
    selected_engine = tk.StringVar(window)
    selected_engine.set("Halo 3") # Default to H3
    folder_label = tk.Label(window, text='Select engine version:')
    folder_label.grid(row=2, column=1, padx=5, pady=5)
    ek_entry = ttk.Combobox(window, textvariable=selected_engine, values=["Halo 2", "Halo 3", "Halo 3: ODST", "Halo Reach", "Halo 4", "Halo 2: AMP"], state="readonly")
    ek_entry.grid(row=3, column=1, padx=20, pady=5)

    # Text box
    selected_label = tk.Label(window, text='Selected scenario paths:')
    selected_label.grid(row=4, column=1, padx=5, pady=5)
    text_box = tk.Text(window, wrap=tk.WORD, height=10, width=50)
    text_box.tag_configure("highlight", background="blue", foreground="white")
    text_box.bind("<1>", highlight_line)
    text_box.grid(row=5, column=1, padx=20, pady=5)
    
    # Add button
    add_button = tk.Button(window, text="Add Scenario", command=lambda : open_scenario_file(text_box, ek_entry))
    add_button.grid(row=6, column=1, padx=20, pady=5)
    
    # Remove button
    remove_button = tk.Button(window, text="Remove Selected Scenario", command=lambda : remove_selected_line(text_box))
    remove_button.grid(row=7, column=1, padx=20, pady=5)
    
    # Compile button
    compile_button = tk.Button(window, text="Compile Scenarios!", command=lambda : compile_scenarios(text_box, ek_entry, window))
    compile_button.grid(row=8, column=1, padx=20, pady=30)
    
    
    
    window.mainloop()

if __name__ == "__main__":
    main()
