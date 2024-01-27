# Palworld Host Save Fix

> ### :warning: This tool is experimental. Be careful of data loss and *always* make a backup.

Fixes the bug which forces a player to create a new character when they already have a save.

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
- Python 3
- [uesave-rs](https://github.com/trumank/uesave-rs)

### Migrate server

Command:    
`python fix_host_save.py <uesave.exe> <save_path> <new_guid> <old_guid>`    
`<uesave.exe>` - Path to your uesave.exe    
`<save_path>` - Path to your save folder    
`<new_guid>` - GUID of the player on the new server    
`<old_guid>` - GUID of the player from the old server

Example:    
`python fix_host_save.py "C:\Users\John\.cargo\bin\uesave.exe" "C:\Users\John\Desktop\my_temporary_folder\2E85FD38BAA792EB1D4C09386F3A3CDA" 6E80B1A6000000000000000000000000 00000000000000000000000000000001`

### Change Co-op host

Prepare:

Fill `uesave_path`、`save_path` and `player_list` in *config.json*, for example:

```json
{
  "uesave_path": "C:\\Users\\John\\.cargo\\bin\\uesave.exe",
  "save_path": "C:\\Users\\John\\Desktop\\my_temporary_folder\\2E85FD38BAA792EB1D4C09386F3A3CDA",
  "player_list": [
    {
      "GUID": "6E80B1A6000000000000000000000000",
      "name": "Arthur"
    },
    {
      "GUID": "F5A892D9000000000000000000000000",
      "name": "John"
    },
    {
      "GUID": "",
      "name": ""
    },
    {
      "GUID": "",
      "name": ""
    },
    {
      "GUID": "",
      "name": ""
    },
    {
      "GUID": "",
      "name": ""
    }
  ]
}
```

Command:

`python change_coop_host.py John`

## How to migrate a co-op save to a Windows dedicated server

Prerequisites:
- Install the dependencies [above](#usage).
- The dedicated server is installed, running, and you're able to join it.
- If you have a Viewing Cage, follow the workaround [below](#viewing-cage-bug) for the \[Viewing Cage bug\] in co-op before moving the save.

Steps:
1. Copy your desired save's folder from `C:\Users\<username>\AppData\Local\Pal\Saved\SaveGames\<random_numbers>` to your dedicated server.
2. In the `PalServer\Pal\Saved\Config\WindowsServer\GameUserSettings.ini` file, change the `DedicatedServerName` to match your save's folder name. For example, if your save's folder name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the `DedicatedServerName` changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.
3. Delete `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\WorldOption.sav` to allow modification of `PalWorldSettings.ini`. Players will have to choose their respawn point again, but nothing else is affected as far as I can tell.
4. Confirm you can connect to your save on the dedicated server and that the world is the one in the save. You can check the world with a character that belongs to a regular player from the co-op.
5. Afterwards, the co-op host must create a new character on the dedicated server. A new `.sav` file should appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players`.
6. The name of that new `.sav` file is the co-op host's new GUID. We will need the co-op host's new GUID for the script to work.
7. Shut the server down and then copy the entire dedicated server save at `PalServer\Pal\Saved\SaveGames\0\<your_save_here>` (it must be the save with the co-op host's new character!) into a temporary folder and remember the path for the temporary folder because it's needed to run the script.
8. If you have not already done so, install [uesave-rs](https://github.com/trumank/uesave-rs) and get the file path to its install location. If the path does not have `uesave.exe` at the end, it's wrong.
9. **Make a backup of your save!** This is an experimental script and has known bugs so always keep a backup copy of your save.
10. Run the script using the command in the [Usage section](#usage) with the information you've gathered and using `00000000000000000000000000000001` as the co-op host's old GUID.
11. Copy the save from the temporary folder back to the dedicated server. Move the save you had in the dedicated server somewhere else or rename it to something different.
12. Start the server back up and have the co-op host join the server with their fixed character.
13. If, after 5 minutes of play, your Pals won't attack for you or do work in the base, follow the [\[Pal bug\] workaround](#pal-bug) to fix them.

## How to migrate a Windows/Linux dedicated server save to a Linux/Windows dedicated server

Prerequisites:
- Install the dependencies [above](#usage).
- The new dedicated server is installed, running, and you're able to join it.

Steps:
1. Copy the save from your old dedicated server to your new dedicated server.
2. In the `PalServer\Pal\Saved\Config\WindowsorLinuxServer\GameUserSettings.ini` file of the new server, change the `DedicatedServerName` to match your save's folder name. For example, if your save's folder name is `2E85FD38BAA792EB1D4C09386F3A3CDA`, the `DedicatedServerName` changes to `DedicatedServerName=2E85FD38BAA792EB1D4C09386F3A3CDA`.
3. Start the new server and have every player create a new character. When a player creates a new character, a new `.sav` file will appear in `PalServer\Pal\Saved\SaveGames\0\<your_save_here>\Players`. The name of that new `.sav` file is the player's new GUID. Make sure to keep track of all old GUIDs, new GUIDs, and which player they belong to.
4. Shut the server down and then copy the entire new server save at `PalServer\Pal\Saved\SaveGames\0\<your_save_here>` (it must be the save with all the new characters!) into a temporary folder and remember the path for the temporary folder because it's needed to run the script.
5. If you have not already done so, install [uesave-rs](https://github.com/trumank/uesave-rs) and get the file path to its install location. If the path does not have `uesave.exe` at the end, it's wrong.
6. **Make a backup of your save!** This is an experimental script and has known bugs so always keep a backup copy of your save.
7. For each player's corresponding new GUID and old GUID pair, run the script using the command in the [Usage section](#usage).
8. Copy the save from the temporary folder back to the dedicated server. Move the save you had in the dedicated server somewhere else or rename it to something different.
9. Start the server back up and have each player join the server with their fixed character.
10. If, after 5 minutes of play, a player's Pals won't attack for them or do work in their base, have them follow the [\[Pal bug\] workaround](#pal-bug) to fix them.

## How to migrate a Windows dedicated server save to co-op

[Apparently this is possible](https://github.com/xNul/palworld-host-save-fix/issues/12#issuecomment-1904052304) but I haven't tried it yet. Instructions should be very similar to "How to migrate a co-op save to a Windows dedicated server" but where you use the `00000000000000000000000000000001` GUID as the new GUID and the player's current GUID on the dedicated server as the old GUID.

If someone wants to make sure this kind of migration works and then create the instructions to do it, I'd accept a PR for them.

## How to change host in Local 4-player Co-op game

Prerequisites:

- Install the dependencies [above](#usage).
- The original host need to get a standard GUID, by joining a friend's world or building and joining a dedicated server, more details can refer to the tutorial above.

Steps:

1. **Make a backup of your save**
2. Fill `uesave_path`、`save_path` and `player_list` in *config.json*, `player_list` should include all players who have joined this save, you can add more GUID-name pairs if needed. Note that all GUID are standard GUID, not `00000000000000000000000000000001`.
3. Run *change_coop_host.py* with a `host` parameter, which can be a GUID or just a nickname for convenience, after that this guy will become the new host.
4. Send this new save to the new host, and replace *LocalData.sav* from this new save file with that from the original save file of the new host, since *LocalData.sav* saves personal map and tutorial data.
5. Let the new host starts the game and invites you and other friends.

## Known bugs

### ~~\[Guild bug\]~~

**\*\* Has likely been fixed by https://github.com/xNul/palworld-host-save-fix/pull/18. \*\***

~~Details: Guild membership doesn't work properly after fixing a character. This is likely happening because there's some guild configuration being missed in the character migration from the old save to the new save.~~

~~Workaround: \[Co-op Only\] In co-op, before moving the save, transfer ownership from the co-op host's character to another character and have the co-op host's character leave the guild. Fixes the issue entirely. Doesn't work when all players lose their save data because there is no working player to hold the guild.~~

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