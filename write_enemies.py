import random

from pathlib import Path
from typing import Dict, List

from helpers import root_path, read_csv, read_json, write_plaintext, read_bytes, write_bytes


def get_map_enemies() -> List[Dict]:
    map_enemies_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Map Enemies.csv")
    map_enemies = read_csv(file_path=map_enemies_csv_path)
    return map_enemies


def get_enemy_categories() -> List[Dict]:
    enemy_categories_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Enemy Categories.csv")
    enemy_categories = read_csv(file_path=enemy_categories_csv_path)
    return enemy_categories


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


def write_enemy_rando_log(kh1_data_path: Path, enemy_rando_log: str) -> None:
    enemy_rando_path = kh1_data_path.joinpath("enemy_rando_log.txt")
    write_plaintext(file_path=enemy_rando_path, data=enemy_rando_log, overwrite=True, create_parents=True)


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
            bytes = read_bytes(kh1_data_file_path)
            i = 0
            for changed_byte in change_byte_array:
                bytes[offset + i] = change_byte_array[i]
                i = i + 1
            write_bytes(kh1_data_file_path, bytes, overwrite=True, create_parents=True)


def write_enemies(settings_file: Path | None = None) -> None:
    kh1_data_path = root_path().joinpath("Working")
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    if "randomize_enemies" in settings_data.keys():
        if settings_data["randomize_enemies"] != "off":
            map_enemies = get_map_enemies()
            enemy_categories = get_enemy_categories()
            enemy_categories = compile_enemy_categories(enemy_categories)
            changes = choose_random_enemies(map_enemies, enemy_categories, settings_data["seed"])
            change_ard_bytes(kh1_data_path, changes)
            enemy_rando_log = get_enemy_rando_log(changes)
            write_enemy_rando_log(kh1_data_path, enemy_rando_log)


if __name__ == "__main__":
    write_enemies()