import random

from pathlib import Path
from typing import Dict, List

from config import ResourceType, read_data, write_data
from helpers import boolify


def choose_random_enemies(map_enemies: List[Dict], enemy_categories: Dict, seed) -> Dict:
    random.seed(seed)
    categories = ["Easy", "Medium", "Hard"]
    changes = {}
    for enemy in map_enemies:
        world          = enemy["World"]
        room           = enemy["Room"]
        original_enemy = enemy["Enemy"]
        file           = enemy["File"]
        offset         = enemy["Offset"]
        key = world + " " + room  + " " + original_enemy
        if key not in changes.keys():
            possible_options = []
            for category in categories:
                if enemy[category] == "TRUE":
                    possible_options = possible_options + enemy_categories[category]
            randomized_enemy = random.choice(possible_options)
            changes[key] = [{"randomized_enemy": randomized_enemy, "file": file, "offset": offset}]
        else:
            changes[key].append({"randomized_enemy": changes[key][0]["randomized_enemy"], "file": changes[key][0]["file"], "offset": offset})
    return changes


def compile_enemy_categories(enemy_categories: List[Dict]) -> Dict:
    compiled_enemy_categories = {}
    for enemy in enemy_categories:
        if enemy["Category"] not in compiled_enemy_categories.keys():
            compiled_enemy_categories[enemy["Category"]] = []
        compiled_enemy_categories[enemy["Category"]].append({"enemy": enemy["Enemy"], "value": enemy["String"]})
    return compiled_enemy_categories


def get_enemy_rando_log(changes: Dict) -> str:
    log = ""
    for key in changes.keys():
        for change in changes[key]:
            log = log + "Changed " + str(key) + " to " + change["randomized_enemy"]["enemy"] + "\n"
    return log


def change_ard_bytes(kh1_data_path: Path, changes: Dict) -> None:
    for key in changes.keys():
        for change in changes[key]:
            file = change["file"]
            offset = int(change["offset"], 16)
            change_byte_array = bytearray(change["randomized_enemy"]["value"], "utf-8")
            
            print("Changed " + str(key) + " to " + change["randomized_enemy"]["enemy"])
            print_str = ""
            for byte in change_byte_array:
                print_str = print_str + hex(byte) + " "
            print(print_str)
            
            kh1_data_file_path = kh1_data_path.joinpath(file)
            bytes = read_data(ResourceType.BIN, path=kh1_data_file_path)
            i = 0
            for changed_byte in change_byte_array:
                bytes[offset + i] = change_byte_array[i]
                i = i + 1
            write_data(ResourceType.BIN, bytes, path=kh1_data_file_path, overwrite=True, create_parents=True)


def write_enemies(settings_file: Path | None = None) -> None:
    kh1_data_path = Path("Working")
    settings_data = read_data(ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("randomize_enemies", False)):
        map_enemies = read_data(ResourceType.CSV, "map_enemies")
        enemy_categories = read_data(ResourceType.CSV, "enemy_categories")
        enemy_categories = compile_enemy_categories(enemy_categories)
        changes = choose_random_enemies(map_enemies, enemy_categories, settings_data["seed"])
        change_ard_bytes(kh1_data_path, changes)
        enemy_rando_log = get_enemy_rando_log(changes)
        write_data(kind=ResourceType.PLAINTEXT, data=enemy_rando_log, path_parts=("Working", "enemy_rando_log.txt"), overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_enemies()