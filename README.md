# Palworld Host Save Fix

### **\*Experimental\***

Palworld save files treat the co-op host differently. This fix makes the co-op host like any other player. Useful for migrating maps to dedicated servers and potentially to another player's computer.

If you have a `00000000000000000000000000000001.sav` file in `<your_save_folder>\Players` and your co-op host can't use their original save, this is the tool for you.

Prerequisites:
- Palworld Dedicated Server is installed, running, and you're able to join it.
- Python 3
- [uesave-rs](https://github.com/trumank/uesave-rs)
- Follow the workaround for the \[Guild bug\] and the \[Viewing Cage bug\] in co-op before moving the save

Usage: `python fix-host-save.py <uesave.exe> <save_path> <host_guid>`    
`<uesave.exe>` - Path to your uesave.exe    
`<save_path>` - Path to your save folder    
`<host_guid>` - GUID of your host

Example: `python fix-host-save.py C:\Users\John\.cargo\bin\uesave.exe C:\Users\John\Desktop\my_temporary_folder\2E85FD38BAA792EB1D4C09386F3A3CDA 6E80B1A6000000000000000000000000`

How to get a co-op save to work with your dedicated server:
1. Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to your dedicated server.
2. Confirm you can connect to your save on the dedicated server and everything is how it should be.
3. Afterwards, the co-op host must create a new character on the dedicated server. A new entry should appear in `<your_dedicated_server_save_path>\Players`.
4. The name of that new `.sav` file is your host's real GUID. We will need your host's real GUID for the script to work.
5. Copy the entire dedicated server save under `PalServer\Pal\Saved\SaveGames\0\<your_save_here>` (it must be the save with the co-op host's new character!) into a temporary folder and keep the path to the temporary folder for running the script.
6. If you have not already done so, install [uesave-rs](https://github.com/trumank/uesave-rs) and get the file path to its install location. If it does not have `uesave.exe` at the end, it's wrong.
7. **Make a backup of your save!** This is an experimental script and has known bugs so always keep a backup copy of your save.
8. Run the script with the information you've gathered and the fix will be applied.
9. Have the co-op host join the server with their fixed character.
10. Enter the guild you left and transfer guild ownership back if you had it before.
11. Follow the \[Pal bug\] workaround to fix your Pals.

Known Bugs:
- \[Guild bug\] Guild membership doesn't work properly on the co-op host's character. Details: This is likely happening because there's some guild configuration being missed in the character migration from the 00001 save to the new save.
- \[Pal bug\] Pals owned by the co-op host won't do anything at the base. Details: This is caused by the Pals not being registered with the correct guild which means it's probably related to the \[Guild bug\].
- \[Viewing Cage bug\] The Viewing Cage [isn't officially supported](https://tech.palworldgame.com/dedicated-server-guide#qa) on dedicated servers so if you have built one, it needs to be removed from your co-op save before migrating it to your dedicated server.

Workarounds:
- \[Guild bug\] In co-op, before moving the save, transfer ownership from the co-op host's character to another character and have the co-op host's character leave the guild.
- \[Pal bug\] On the dedicated server, after the co-op host's character is restored, have the co-op host's character go into their base, drop and pick up every single Pal they own, including the base workers. This will re-register the Pals with the correct guild.
- \[Viewing Cage bug\] If you have built a Viewing Cage, it needs to be removed from your co-op save before migrating it to your dedicated server.

Note: This does not fix the issue with normal (non-host) players being forced to create new characters. It is specifically for when the host is forced to create a new character. However, it can be repurposed to solve that problem for those who are technical enough. To do so, you must have all the normal players you want to fix create new characters, record the old and new GUIDs for each player, modify the `host_sav_path` in the script to point to the old GUID for a player, use that player's new GUID as input to the script, and run the script. Do that for every player and in the end, every player should have their data restored. However, these players will probably have the same bugs as the host does so make sure to follow the workarounds for them.

Credit to [cheahjs](https://gist.github.com/cheahjs/300239464dd84fe6902893b6b9250fd0) for his very useful script helping me to make this fix!

Appreciate any help testing and resolving bugs.