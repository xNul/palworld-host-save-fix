# Palworld Host Save Fix

> ### :warning: This tool is experimental. Be careful of data loss and *always* make a backup. :warning:

Fixes the bug which forces a player to create a new character when they already have a save.

*Note: If you have an advanced co-op map with level 30-40+ characters and can't get the fix to work for you, please open an issue and send the save to me. I have some major and more complete changes in the works but I need mid to late game saves to make sure I get everything and people to confirm it's working correctly before I release.*

## Table of Contents

- [Abstract](#abstract)
- [Usage](#usage)
- [Migration Examples](#migration-examples)
  - [How to migrate a co-op save to a Windows dedicated server](#how-to-migrate-a-co-op-save-to-a-windows-dedicated-server)
  - [How to migrate a Windows/Linux dedicated server save to a Linux/Windows dedicated server](#how-to-migrate-a-windowslinux-dedicated-server-save-to-a-linuxwindows-dedicated-server)
  - [How to migrate a Windows dedicated server save to co-op](#how-to-migrate-a-windows-dedicated-server-save-to-co-op)
- [Finding Player GUIDs](#finding-player-guids)
- [Known bugs](#known-bugs)
  - [\[Guild bug\]](#guild-bug)
  - [\[Pal bug\]](#pal-bug)
  - [\[Viewing Cage bug\]](#viewing-cage-bug)
  - [\[Left Click bug\]](#left-click-bug)

## Abstract 

Palworld save files are different depending on the type of server you are running. Co-op, Windows dedicated server, Linux dedicated server, SteamCMD dedicated server, all of these are different types of Palworld servers and if you try to migrate a save file from one type of server to another, you can run into a player save bug which forces you to create a new character.

For example:
- Moving a Windows co-op save to a Windows dedicated server will force the host to create a new character and lose their save.
- Moving a Windows dedicated server save to a Linux dedicated server will force all players to create a new character and lose their save.
- Moving a Linux dedicated server save to a Windows dedicated server will force all players to create a new character and lose their save.
- Moving a Windows co-op save to a Linux dedicated server will force all players to create a new character and lose their save.
- Etc.

The bug happens because players are identified and correlated to their save via their GUID. These different types of servers generate player GUIDs differently so when a player joins, the server generates a new GUID that doesn't match the old save's GUID and because of this, doesn't realize the player already has a save.

To fix this bug, we've made a script that takes the GUID of the player on the new server and applies it to the player save from the old server so that the new server will use the player save from the old server.

## Usage

Dependencies:
- Python >=3.10
- Clone the repository with `git clone https://github.com/xNul/palworld-host-save-fix`
- Install the python packages with `pip install -r requirements.txt`

Using the GUI:
- Open Command Prompt in the folder
- Run command `python gui.py`
- Browse for your save folder
- Select the new character to overwrite and the old character you want to fix/keep from the dropdowns
- Enable the guild fix if required
- Hit the button to run the command
- Read the warning in Command Prompt and press enter

Command:    
```
python fix_host_save.py <save_path> <new_guid> <old_guid> <guild_fix>
```      
`<save_path>` - Path to your save folder    
`<new_guid>` - GUID of the player on the new server    
`<old_guid>` - GUID of the player from the old server    
`<guild_fix>` - True or False. Apply the fix for the [\[Guild bug\]](#guild-bug).

Example:    
```
python fix_host_save.py "C:\Users\John\Desktop\my_temporary_folder\2E85FD38BAA792EB1D4C09386F3A3CDA" 6E80B1A6000000000000000000000000 00000000000000000000000000000001 False
```

## Migration Examples

### How to migrate a co-op save to a Windows dedicated server
*Only my co-op host isn't able to use their character on the dedicated server.*

Prerequisites:
- Install the dependencies [above](#usage).
- The dedicated server is installed, running, and you're able to join it.
- Follow the workaround [below](#guild-bug) for the \[Guild bug\] in co-op before moving the save.
- If you have a Viewing Cage, follow the workaround [below](#viewing-cage-bug) for the \[Viewing Cage bug\] in co-op before moving the save.

Steps:
1. Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to your dedicated server at `PalServer\Pal\Saved\SaveGames\0`.
2. In the `PalServer\Pal\Saved\Config\WindowsServer\GameUserSettings.ini` file, change the `DedicatedServerName` to match your save folder's name. For example, if your save folder's name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the `DedicatedServerName` changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.
3. Delete `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\WorldOption.sav` to allow modification of `PalWorldSettings.ini`. Players will have to choose their respawn point again, but nothing else is affected as far as I can tell.
4. Confirm you can connect to your save on the dedicated server and that the world is the one you want. You can connect to the dedicated server and check the world with a character that does not belong to the co-op host.
5. Afterwards, the co-op host must create a new character on the dedicated server. A new `.sav` file should appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players`.
6. The name of that new `.sav` file is the co-op host's new GUID. We will need the co-op host's new GUID for the script to work.
7. Shut the server down and then copy the entire save folder in the dedicated server at `PalServer\Pal\Saved\SaveGames\0\<your_save_here>` (it must be the save folder with the co-op host's new character!) into a temporary folder and remember the path for the temporary folder because it's needed to run the script.
8. **Make a backup of your save folder!** This is an experimental script and has known bugs so always keep a backup copy of your save folder.
9. Run the script using the command in the [Usage section](#usage) with the information you've gathered, using `00000000000000000000000000000001` as the co-op host's old GUID, and make sure to set `<guild_fix>` to `False`.
10. Copy the save folder from the temporary folder back to the dedicated server. Move the save folder you had in the dedicated server somewhere else or rename it to something different.
11. Start the server back up and have the co-op host join the server with their fixed character.
12. If, after 5 minutes of play, your Pals won't attack for you or do work in the base, follow the [\[Pal bug\] workaround](#pal-bug) to fix them.

### How to migrate a Windows/Linux dedicated server save to a Linux/Windows dedicated server
*No player, co-op host or otherwise, is able to use their character on the dedicated server.*

Note: This method relies on the \[Guild bug\] fix even though the fix itself has bugs because with this migration process, every player loses access to their character and they all have to be fixed so there is no 'good' character who can hold the guild for other players as in the co-op to dedicated server migration process [above](#how-to-migrate-a-co-op-save-to-a-windows-dedicated-server). Progress on the \[Guild bug\] fix is ongoing and it will hopefully be completely fixed soon.

Prerequisites:
- Install the dependencies [above](#usage).
- The new dedicated server is installed, running, and you're able to join it.

Steps:
1. Copy the save folder from your old dedicated server to your new dedicated server.
2. In the `PalServer\Pal\Saved\Config\WindowsorLinuxServer\GameUserSettings.ini` file of the new server, change the `DedicatedServerName` to match your save folder's name. For example, if your save folder's name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the `DedicatedServerName` changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.
3. Start the new server and have every player create a new character. When a player creates a new character, a new `.sav` file will appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players`. The name of that new `.sav` file is the player's new GUID. Make sure to keep track of all old GUIDs, new GUIDs, and which player they belong to.
4. Shut the server down and then copy the entire save folder from the new server at `PalServer\Pal\Saved\SaveGames\0\<your_save_here>` (it must be the save folder with all the new characters!) into a temporary folder and remember the path for the temporary folder because it's needed to run the script.
5. **Make a backup of your save folder!** This is an experimental script and has known bugs so always keep a backup copy of your save folder.
6. For each player's corresponding new GUID and old GUID pair, run the script using the command in the [Usage section](#usage) and make sure to set `<guild_fix>` to `True`.
7. Copy the save folder from the temporary folder back to the dedicated server. Move the save folder you had in the dedicated server somewhere else or rename it to something different.
8. Start the server back up and have each player join the server with their fixed character.
9. If, after 5 minutes of play, a player's Pals won't attack for them or do work in their base, have them follow the [\[Pal bug\] workaround](#pal-bug) to fix them.

### How to migrate a Windows dedicated server save to co-op

1. Copy the save from the dedicated server to a temporary folder.
2. Start a new co-op game and create a new character, copy the new character `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>\Players\00000000000000000000000000000001.sav` to `<your_temporary_folder>\<your_save_here>\Players`.
3. Run the script while using `00000000000000000000000000000001` as the `<new_guid>` and the character you want to be host as the `<old_guid>`.
4. Once complete, you can copy the save folder from the temporary folder to `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames`.
5. Start the game and you should be able to play normally, friends can join in without any issue since there guid remains the same.

## Finding Player GUIDs

If you are having trouble figuring out which GUID is associated to a player, you can try using the following steps:

1. Set an admin password in the older server's `PalServer\Pal\Saved\Config\WindowsorLinuxServer\PalWorldSettings.ini` file.
2. Connect to the older server, open chat, and type `/adminpassword <your_admin_password>`.
3. Open chat and run `/showplayers` (or you can click `esc` and go to the options page to see and copy your own ID after entering the admin password).
4. Record the `playeruid` field for each player. 
5. Use a tool to convert the `playeruid` number to 8-character hexadecimal GUID prefix. For example, you can run
```bash
python -c "print(format(<your_player_id_number>, '08x'))"
```
6. The output of the command is the prefix player's GUID (i.e. find the `.sav` file that starts with the output).
7. Repeat the steps for the new server if needed.

## Known bugs

### \[Guild bug\]

Details: Guild membership doesn't work properly after fixing a character. This is likely happening because there's some guild configuration being missed in the character migration from the old save to the new save.

Workaround: \[Co-op Only\] In co-op, before moving the save, transfer ownership from the co-op host's character to another character and have the co-op host's character leave the guild. Fixes the issue entirely. Doesn't work when all players lose their save data because there is no working player to hold the guild.

### \[Pal bug\]

Details: Pals owned by the player won't do anything at the base. This is likely caused by the Pals not being registered with the correct guild.

Workaround: On the new server, after the save has been fixed, have each player's character go into their base, drop on the ground and pick up every single Pal they own, including the base workers. This can be done using the "Drop" button in the Party menu. This will re-register the Pals with the correct guild and fix the issue entirely.

### \[Viewing Cage bug\]

Details: The Viewing Cage [isn't officially supported](https://tech.palworldgame.com/dedicated-server-guide#qa) on dedicated servers so if you have built one in co-op, it needs to be removed from your co-op save before migrating it to your dedicated server.

Workaround: \[Co-op Only\] If you have built a Viewing Cage, it needs to be removed from your co-op save before migrating it to your dedicated server.

### \[Left Click bug\]

Details: After applying the fix, some players experience a bug where you can't hold your left mouse button to attack. It seems like this only happens if you didn't do the [\[Guild bug\] workaround](#guild-bug) but I'm not sure.

Workaround: If you leave the guild and rejoin, it goes away. Thanks [/u/skalibran](https://www.reddit.com/r/Palworld/comments/19axeqs/autoswing_not_working/kiq85zr/)!

### Credit to [cheahjs](https://gist.github.com/cheahjs/300239464dd84fe6902893b6b9250fd0) for his very useful script helping me to make this fix!

### Appreciate any help testing and resolving bugs.
