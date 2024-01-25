import argparse
import json
import os
from pathlib import Path
import sys

from fix_host_save import sav_to_json, json_to_sav, clean_up_files

# GUID of current host is 00..01, we need to get his standard GUID.
def old_host(player_list, player_save_path):
    all_guid_list = [player['GUID'] for player in player_list]
    current_guid_list = [save.stem for save in player_save_path.iterdir()]
    old_host = set(all_guid_list) - set(current_guid_list)
    return old_host.pop()

# Get new host's standard GUID.
def new_host(name_or_guid, player_list):
    for player in player_list:
        if player['name'] == name_or_guid or player['GUID'] == name_or_guid:
            return player['GUID']
    return None

def change_guid(old_guid, new_guid, save_path, uesave_path):
    # Apply expected formatting for the GUID.
    new_guid_formatted = '{}-{}-{}-{}-{}'.format(new_guid[:8], new_guid[8:12], new_guid[12:16], new_guid[16:20], new_guid[20:]).lower()
    old_level_formatted = ''
    new_level_formatted = ''
    
    # Player GUIDs in a guild are stored as the decimal representation of their GUID.
    # Every byte in decimal represents 2 hexidecimal characters of the GUID
    # 32-bit little endian.
    for y in range(8, 36, 8):
        for x in range(y-1, y-9, -2):
           temp_old = str(int(old_guid[x-1] + old_guid[x], 16))+',\n'
           temp_new = str(int(new_guid[x-1] + new_guid[x], 16))+',\n'
           old_level_formatted += temp_old
           new_level_formatted += temp_new
        
    old_level_formatted = old_level_formatted.rstrip("\n,")
    new_level_formatted = new_level_formatted.rstrip("\n,")
    old_level_formatted = list(map(int, old_level_formatted.split(",\n")))
    new_level_formatted = list(map(int, new_level_formatted.split(",\n")))
    
    level_sav_path = save_path + '/Level.sav'
    old_sav_path = save_path + '/Players/'+ old_guid + '.sav'
    new_sav_path = save_path + '/Players/' + new_guid + '.sav'
    level_json_path = level_sav_path + '.json'
    old_json_path = old_sav_path + '.json'

    # Convert save files to JSON so it is possible to edit them.
    sav_to_json(uesave_path, level_sav_path)
    sav_to_json(uesave_path, old_sav_path)
    print('Converted save files to JSON')
    
    # Parse our JSON files.
    with open(old_json_path) as f:
        old_json = json.load(f)
    with open(level_json_path) as f:
        level_json = json.load(f)
    print('JSON files have been parsed')
    
    # Replace all instances of the old GUID with the new GUID.
    
    # Player data replacement.
    old_json["root"]["properties"]["SaveData"]["Struct"]["value"]["Struct"]["PlayerUId"]["Struct"]["value"]["Guid"] = new_guid_formatted
    old_json["root"]["properties"]["SaveData"]["Struct"]["value"]["Struct"]["IndividualId"]["Struct"]["value"]["Struct"]["PlayerUId"]["Struct"]["value"]["Guid"] = new_guid_formatted
    old_instance_id = old_json["root"]["properties"]["SaveData"]["Struct"]["value"]["Struct"]["IndividualId"]["Struct"]["value"]["Struct"]["InstanceId"]["Struct"]["value"]["Guid"]
    
    # Level data replacement.
    instance_ids_len = len(level_json["root"]["properties"]["worldSaveData"]["Struct"]["value"]["Struct"]["CharacterSaveParameterMap"]["Map"]["value"])
    for i in range(instance_ids_len):
        instance_id = level_json["root"]["properties"]["worldSaveData"]["Struct"]["value"]["Struct"]["CharacterSaveParameterMap"]["Map"]["value"][i]["key"]["Struct"]["Struct"]["InstanceId"]["Struct"]["value"]["Guid"]
        if instance_id == old_instance_id:
            level_json["root"]["properties"]["worldSaveData"]["Struct"]["value"]["Struct"]["CharacterSaveParameterMap"]["Map"]["value"][i]["key"]["Struct"]["Struct"]["PlayerUId"]["Struct"]["value"]["Guid"] = new_guid_formatted
            break
    
    # Guild data replacement.
    group_ids_len = len(level_json["root"]["properties"]["worldSaveData"]["Struct"]["value"]["Struct"]["GroupSaveDataMap"]["Map"]["value"])
    for i in range(group_ids_len):
        group_id = level_json["root"]["properties"]["worldSaveData"]["Struct"]["value"]["Struct"]["GroupSaveDataMap"]["Map"]["value"][i]
        if group_id["value"]["Struct"]["Struct"]["GroupType"]["Enum"]["value"] == "EPalGroupType::Guild":
           group_raw_data =  group_id["value"]["Struct"]["Struct"]["RawData"]["Array"]["value"]["Base"]["Byte"]["Byte"]
           raw_data_len = len(group_raw_data)
           for i in range(raw_data_len-15):
               if group_raw_data[i:i+16] == old_level_formatted:
                  group_raw_data[i:i+16] = new_level_formatted
    print('Changes have been made')
    
    # Dump modified data to JSON.
    with open(old_json_path, 'w') as f:
        json.dump(old_json, f, indent=2)
    with open(level_json_path, 'w') as f:
        json.dump(level_json, f, indent=2)
    print('JSON files have been exported')
    
    # Convert our JSON files to save files.
    json_to_sav(uesave_path, level_json_path)
    json_to_sav(uesave_path, old_json_path)
    print('Converted JSON files back to save files')
    
    # Clean up miscellaneous GVAS and JSON files which are no longer needed.
    clean_up_files(level_sav_path)
    clean_up_files(old_sav_path)
    print('Miscellaneous files removed')
    
    # We must rename the patched save file from the old GUID to the new GUID for the server to recognize it.
    if os.path.exists(new_sav_path):
        os.remove(new_sav_path)
    os.rename(old_sav_path, new_sav_path)
    print(f'Changed GUID {old_guid} -> {new_guid}')


def main():
    parser = argparse.ArgumentParser(description='Change host in local 4-player co-op game.')
    parser.add_argument('host', help='GUID or name of new co-op host')
    args = parser.parse_args()

    # Warn the user about potential data loss.
    print('WARNING: Running this script WILL change your save files and could \
potentially corrupt your data. It is HIGHLY recommended that you make a backup \
of your save folder before continuing. Press enter if you would like to continue.')
    input('> ')

    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r') as file:
        config = json.load(file)

    uesave_path = config['uesave_path']
    save_path = config['save_path']
    player_list = config['player_list']
    player_list = [player for player in player_list if player['GUID'] != '']
    print(f'uesave_path: {uesave_path}')
    print(f'save_path: {save_path}')
    print(f'player_list: {player_list}')

    # uesave_path must point directly to the executable, not just the path it is located in.
    if not os.path.exists(uesave_path) or not os.path.isfile(uesave_path):
        print('ERROR: Your given <uesave_path> of "' + uesave_path + '" is invalid. It must point directly to the executable. For example: C:\\Users\\Bob\\.cargo\\bin\\uesave.exe')
        exit(1)
    
    # save_path must exist in order to use it.
    if not os.path.exists(save_path):
        print('ERROR: Your given <save_path> of "' + save_path + '" does not exist. Did you enter the correct path to your save folder?')
        exit(1)
    
    # player_list must have at least 2 players.
    if len(player_list) < 2:
        print('ERROR: You must have at least 2 players in your <players> list, add more players to your config.json file.')
        exit(1)

    # host must be a valid GUID or name.
    if args.host not in [player['GUID'] for player in player_list] and args.host not in [player['name'] for player in player_list]:
        print('ERROR: Your given <host> of "' + args.host + '" is not a valid GUID or name. Please refer to your config.json file.')
        exit(1)
    
    old_host_guid = old_host(player_list, Path(save_path)/'Players')
    new_host_guid = new_host(args.host, player_list)
    change_guid('00000000000000000000000000000001', old_host_guid, save_path, uesave_path)
    change_guid(new_host_guid, '00000000000000000000000000000001', save_path, uesave_path)
    print('Host change has been applied! Have fun!')

if __name__ == '__main__':
    main()
