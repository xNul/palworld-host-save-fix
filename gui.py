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
    folder_path = ent_save_folder.get()
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
        if not cmb_new_guid.get() in usernames:
            cmb_new_guid.set('')

        if not cmb_old_guid.get() in usernames:
            cmb_old_guid.set('')

        cmb_new_guid['values'] = usernames
        cmb_old_guid['values'] = usernames

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

            player_info[filename_guid] = f'{nickname} (Lvl. {level})'
    
    player_info = dict(sorted(player_info.items(), key=lambda item: str(item[1]).lower()))
    player_info.update({
        filename_guid:formatted_guid
        for formatted_guid, filename_guid in guid_data.items()
    })
    
    return player_info

def run_command():
    save_path = ent_save_folder.get()
    new_guid = list(player_cache.keys())[cmb_new_guid.current()]
    old_guid = list(player_cache.keys())[cmb_old_guid.current()]
    guild_fix = guild_fix_var.get()
    
    command = f'python fix_host_save.py "{save_path}" {new_guid.replace(".sav", "")} {old_guid.replace(".sav", "")} {guild_fix}'
    subprocess.run(command, shell=True)
    update_guid_dropdowns()

def save_config():
    config = {
        'save_path': ent_save_folder.get(),
        'new_guid': cmb_new_guid.get(),
        'old_guid': cmb_old_guid.get(),
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
            ent_save_folder.insert(0, config.get('save_path', ''))
            update_guid_dropdowns()
            cmb_new_guid.set(config.get('new_guid', ''))
            cmb_old_guid.set(config.get('old_guid', ''))
            guild_fix_var.set(config.get('guild_fix', ''))

app = tk.Tk()
app.geometry('350x250')
app.resizable(False, False) 
app.title('Fix Host Save Command GUI')

# Save folder path.
lbl_save_folder = tk.Label(app, text='Path to save folder:')
lbl_save_folder.pack()

ent_save_folder = tk.Entry(app, width=50)
ent_save_folder.pack()
ent_save_folder.bind('<KeyRelease>', on_entry_change)

btn_browse_folder = tk.Button(
    app, text='Browse', command=lambda: browse_folder(ent_save_folder)
)
btn_browse_folder.pack(pady=(0, 10))

# New GUID selection.
lbl_new_guid = tk.Label(app, text='The new character to overwrite:')
lbl_new_guid.pack()

cmb_new_guid = ttk.Combobox(app, postcommand=update_guid_dropdowns, width=40)
cmb_new_guid.pack(pady=(0, 10))

# Old GUID selection.
lbl_old_guid = tk.Label(app, text='The old character to fix/keep:')
lbl_old_guid.pack()

cmb_old_guid = ttk.Combobox(app, postcommand=update_guid_dropdowns, width=40)
cmb_old_guid.pack(pady=(0, 10))

# Guild fix selection.
guild_fix_var = tk.BooleanVar()

chk_guild_fix = tk.Checkbutton(app, text='Guild fix', variable=guild_fix_var, height=2)
chk_guild_fix.pack()

# Run command button.
btn_run_command = tk.Button(app, text='Run command', command=run_command)
btn_run_command.pack()

load_config()

app.mainloop()
