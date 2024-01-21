# Palworld Host Save Fix

### **\*Experimental\***

Palworld save files treat the co-op host differently. This fix makes the co-op host like any other player. Useful for migrating maps to dedicated servers and potentially to another player's computer.

If you have a `00000000000000000000000000000001.sav` file in `<your_save_folder>/Players` and your co-op host can't use their original save, this is the tool for you.

Prerequisites:
- Palworld Dedicated Server is installed and running
- Python 3
- [uesave-rs](https://github.com/trumank/uesave-rs)

Usage: `python fix-host-save.py <uesave.exe> <save_path> <host_guid>`    
`<uesave.exe>` - Path to your uesave.exe    
`<save_path>` - Path to your save folder    
`<host_guid>` - GUID of your host

Example: `python fix-host-save.py C:\Users\<username>\.cargo\bin\uesave.exe C:\Users\<username>\Desktop\my_pal_save XXXXXXXX000000000000000000000000`

How to get a co-op save to work with your dedicated server:
1. Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to your dedicated server.
2. Confirm you can connect to your save on the dedicated server and everything is how it should be.
3. If you can connect to your dedicated server and your save, the co-op host must create a new character. A new entry should appear in `<your_dedicated_server_save_path>/Players`.
4. The name of that new `.sav` file is your host's real GUID. We will need this for the script to work.
5. Copy the dedicated server save which has the new `.sav` file into a temporary folder and keep the path to the temporary folder for running the script.
6. If you have not already done so, install [uesave-rs](https://github.com/trumank/uesave-rs) and get the path to its install location.
7. **Make a backup of your save!** This is an experimental script and has known bugs so always keep a backup copy of your save.
8. Run the script with the information you've gathered and the fix will be applied.

Known Bugs: Guilds are bugged on the co-op host's character. Transferring ownership from the co-op host's character to another character and leaving the guild using co-op before applying the fix is a confirmed workaround.

Credit to [cheahjs](https://gist.github.com/cheahjs/300239464dd84fe6902893b6b9250fd0) for his very useful script helping me to make this fix!

Appreciate any help testing and resolving bugs.