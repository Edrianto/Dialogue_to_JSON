import json
import sys
from pathlib import Path


def convert_to_json():
    file_name = check_valid()

    with open(file_name, "r") as file:
        dialogue = file.read().splitlines()
        clean_keys, keys = get_json_keys(dialogue)
        dialogue = delete_header(dialogue)

        dict_to_convert = {}
        current_node = ""

        for line in dialogue:
            if line == "#":
                break
            if line == "\\":
                current_node = ""
                dialogue = delete_header(dialogue)
                continue

            if line == "-":
                continue

            if current_node == "":
                current_node = line
                dict_to_convert[current_node] = {}
            elif not current_node == "" and not line == "\\":
                current_key = clean_keys[dialogue.index(line)-1]
                dict_to_convert[current_node][current_key] = return_value(keys[dialogue.index(line)-1], line)
            

    new_file_name = file_name[0:len(file_name)-4]
    with open(new_file_name+"_converted.json", "w") as file:
        json.dump(dict_to_convert,file,indent=4)


def return_value(current_key: str, line: str):
    is_list = False
    is_dict = False

    # list
    if "[" in current_key:
        lists = line.split("=")

        if not "{" in current_key:
            return lists

        is_list = True
    
    # dict
    if "{" in current_key:
        if is_list:
            dict_result = []
            for element in lists:
                key1 = current_key[current_key.index("{")+1:current_key.index(",")]
                key2 = current_key[current_key.index(",")+1:current_key.index("}")]

                branches = element.split("|")

                branches[0] = branches[0].replace("{", "")
                branches[len(branches)-1] = branches[len(branches)-1].replace("}", "")

                dict_to_append = {}
                dict_to_append[key1] = branches[0]
                dict_to_append[key2] = branches[len(branches)-1]

                dict_result.append(dict_to_append)
            
            return dict_result
        
        is_dict = True
        branches = line.split("|")
        
        branches[0] = branches[0].replace("{", "")
        branches[len(branches)-1] = branches[len(branches)-1].replace("}", "")

    # bool
    if current_key.endswith("!"):
        if is_dict:
            dict_result = {}
            for branch in branches:
                if branch.startswith("not "):
                    dict_result[branch.replace("not ","")] = False
                else:
                    dict_result[branch] = True
            
            return dict_result

    # int
    if current_key.endswith("&"):
        is_int = True
    
    return line


def check_valid():
    if len(sys.argv) != 2:
        sys.exit("Correct Usage : Python dialogue_to_json.py [PATH_OF_FILE_TO_CONVERT]")

    file_name = sys.argv[1]
    file_path = Path(file_name)

    if not file_path.exists():
        sys.exit(file_name+" does not exist")

    if not file_name.endswith(".txt"):
        sys.exit("File needs to be a .txt file")
    
    return file_name

def delete_header(dialogue):
    new_dialogue = list(dialogue)
    
    border = new_dialogue.index("\\")
    del new_dialogue[0:border+1]

    return new_dialogue


def get_json_keys(dialogue):
    keys = []
    clean_keys = []

    for line in dialogue:
        if line == "\\":
            return clean_keys, keys

        keys.append(line)

        if "[" in line:
            clean_keys.append(line[0:line.index("[")])
            continue
        if "{" in line:
            clean_keys.append(line[0:line.index("{")])
            continue

        clean_keys.append(line)


if __name__ == "__main__":
    convert_to_json()