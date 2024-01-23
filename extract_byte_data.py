import json

level_json = json.load(open('your_save/Level.sav.json'))
f = open('all_bytes.txt', 'wb')

# Recursively search the whole save for bytes that haven't been decoded yet, decode them, and save it to a file.
def recursive_search(json_object, path=""):
    if type(json_object) == dict:
        for key in json_object:
            if key == 'Byte' and type(json_object[key]) == list:
                level_bytes = bytes(json_object[key]).hex()
                f.write(path.encode('utf-8') + '\n\n'.encode('utf-8') + bytes.fromhex(level_bytes) + '\n\n\n\n\n\n\n'.encode('utf-8'))
            else:
                recursive_search(json_object[key], path + '[' + key + ']')
    elif type(json_object) == list:
        for i in range(len(json_object)):
            recursive_search(json_object[i], path + '[' + str(i) + ']')
    elif type(json_object) == int or type(json_object) == float or type(json_object) == str or type(json_object) == bool:
        pass
    else:
        print('Broke on type :')
        print(type(json_object))

recursive_search(level_json)
f.close()