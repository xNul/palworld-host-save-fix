import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk

from fix_host_save import sav_to_json

player_cache = {}
config_file = 'config.json'

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    if foldername != '':
        player_cache = {}
        entry.delete(0, tk.END)
        entry.insert(0, foldername)
        save_config()
        update_guid_dropdowns()

def update_guid_dropdowns():
    folder_path = entry_save.get()
    players_folder = os.path.join(folder_path, 'Players')
    if os.path.exists(players_folder) and os.path.isdir(players_folder):
        # List all files and remove the '.sav' extension.
        filename_guids = [
            os.path.splitext(f)[0]
            for f in os.listdir(players_folder)
            if os.path.isfile(os.path.join(players_folder, f)) and f.endswith('.sav')
        ]
        
        global player_cache
        if set(filename_guids) != set(player_cache.keys()):
            level_json = sav_to_json(folder_path + '/Level.sav')
            player_cache = find_player_info(level_json, filename_guids)
        
        usernames = list(player_cache.values())
        if not combo_new_guid.get() in usernames:
            combo_new_guid.set('')
        if not combo_old_guid.get() in usernames:
            combo_old_guid.set('')
        combo_new_guid['values'] = usernames
        combo_old_guid['values'] = usernames

def find_player_info(level_json, filename_guids):
    player_info = {}
    character_save_parameter_map = level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value']
    guid_data = {
        '{}-{}-{}-{}-{}'.format(guid[:8], guid[8:12], guid[12:16], guid[16:20], guid[20:]).lower():str(guid)
        for guid in filename_guids
    }

    for i in range(len(character_save_parameter_map)):
        player_uid = character_save_parameter_map[i]['key']['PlayerUId']['value']
        save_parameter = character_save_parameter_map[i]['value']['RawData']['value']['object']['SaveParameter']['value']

        if player_uid in guid_data.keys() and 'IsPlayer' in save_parameter and save_parameter['IsPlayer']['value'] == True:
            nickname = save_parameter['NickName']['value']
            level = str(save_parameter['Level']['value']) if 'Level' in save_parameter else '0'

            formatted_player_guid = str(player_uid)
            filename_guid = guid_data.pop(formatted_player_guid)
            player_info[filename_guid] = f"[{formatted_player_guid[:8]}] {nickname} (Lvl. {level})"
    
    player_info = dict(sorted(player_info.items(), key=lambda item: str(item[1])[11:].lower()))
    player_info.update({
        filename_guid:f"[{formatted_guid[:8]}] External Player"
        for formatted_guid, filename_guid in guid_data.items()
    })
    
    return player_info

def run_command():
    save_path = entry_save.get()
    new_guid = list(guid_cache.keys())[combo_new_guid.current()]
    old_guid = list(guid_cache.keys())[combo_old_guid.current()]
    guild_fix = guild_fix_var.get()
    
    command = (
        f'python fix_host_save.py "{save_path}" {new_guid.replace(".sav", "")} {old_guid.replace(".sav", "")} {guild_fix}'
    )
    subprocess.run(command, shell=True)
    update_guid_dropdowns()

def save_config():
    config = {
        'save_path': entry_save.get(),
        'new_guid': combo_new_guid.get(),
        'old_guid': combo_old_guid.get(),
        'guild_fix': guild_fix_var.get(),
    }
    with open(config_file, 'w') as f:
        json.dump(config, f)

def on_entry_change(event):
    save_config()

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            entry_save.insert(0, config.get('save_path', ''))
            update_guid_dropdowns()
            combo_new_guid.set(config.get('new_guid', ''))
            combo_old_guid.set(config.get('old_guid', ''))
            guild_fix_var.set(config.get('guild_fix', ''))

app = tk.Tk()
app.geometry("350x250")
app.resizable(False, False) 
app.title('Fix Host Save Command GUI')

# Save folder path.
tk.Label(app, text='Path to save folder:').pack()
entry_save = tk.Entry(app, width=50)
entry_save.pack()
entry_save.bind('<KeyRelease>', on_entry_change)
button_browse_save = tk.Button(
    app, text='Browse', command=lambda: browse_folder(entry_save)
)
button_browse_save.pack()

# New GUID selection.
tk.Label(app, text='The new character to overwrite:').pack()
combo_new_guid = ttk.Combobox(app, postcommand=update_guid_dropdowns, width=40)
combo_new_guid.pack()

# Old GUID selection.
tk.Label(app, text='The old character to fix/keep:').pack()
combo_old_guid = ttk.Combobox(app, postcommand=update_guid_dropdowns, width=40)
combo_old_guid.pack()

# Guild fix selection.
guild_fix_var = tk.BooleanVar()
cb_guild_fix = tk.Checkbutton(app, text='Guild fix', variable=guild_fix_var, height=2)
cb_guild_fix.pack()

# Run command button.
run_button = tk.Button(app, text='Run Command', command=run_command)
run_button.pack()

load_config()

app.mainloop()
