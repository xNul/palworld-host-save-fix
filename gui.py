import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import json
import os

config_file = 'config.json'

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)
    save_config()

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, foldername)
    save_config()
    update_guid_dropdowns(foldername)

def update_guid_dropdowns(folder_path):
    players_folder = os.path.join(folder_path, "Players")
    if os.path.exists(players_folder) and os.path.isdir(players_folder):
        file_names = [f for f in os.listdir(players_folder) if os.path.isfile(os.path.join(players_folder, f))]
        combo_new_guid['values'] = file_names
        combo_old_guid['values'] = file_names

def run_command():
    uesave_path = entry_uesave.get()
    save_path = entry_save.get()
    new_guid = combo_new_guid.get()
    old_guid = combo_old_guid.get()
    command = f'python fix-host-save.py "{uesave_path}" "{save_path}" {new_guid} {old_guid}'
    subprocess.run(command, shell=True)

def save_config():
    config = {
        'uesave_path': entry_uesave.get(),
        'save_path': entry_save.get(),
        'new_guid': combo_new_guid.get(),
        'old_guid': combo_old_guid.get()
    }
    with open(config_file, 'w') as f:
        json.dump(config, f)

def on_entry_change(event):
    save_config()

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            entry_uesave.insert(0, config.get('uesave_path', ''))
            entry_save.insert(0, config.get('save_path', ''))
            update_guid_dropdowns(config.get('save_path', ''))
            combo_new_guid.set(config.get('new_guid', ''))
            combo_old_guid.set(config.get('old_guid', ''))

app = tk.Tk()
app.title("Fix Host Save Command GUI")

# Uesave.exe path
tk.Label(app, text="Path to uesave.exe:").pack()
entry_uesave = tk.Entry(app, width=50)
entry_uesave.pack()
entry_uesave.bind("<KeyRelease>", on_entry_change)
button_browse_uesave = tk.Button(app, text="Browse", command=lambda: browse_file(entry_uesave))
button_browse_uesave.pack()

# Save folder path
tk.Label(app, text="Path to save folder:").pack()
entry_save = tk.Entry(app, width=50)
entry_save.pack()
entry_save.bind("<KeyRelease>", on_entry_change)
button_browse_save = tk.Button(app, text="Browse", command=lambda: browse_folder(entry_save))
button_browse_save.pack()

# New GUID selection
tk.Label(app, text="New GUID:").pack()
combo_new_guid = ttk.Combobox(app)
combo_new_guid.pack()

# Old GUID selection
tk.Label(app, text="Old GUID:").pack()
combo_old_guid = ttk.Combobox(app)
combo_old_guid.pack()

# Run command button
run_button = tk.Button(app, text="Run Command", command=run_command)
run_button.pack()

load_config()

app.mainloop()
