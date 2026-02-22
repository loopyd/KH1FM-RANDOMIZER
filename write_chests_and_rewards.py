import json
from typing import Dict, List, Tuple
from pathlib import Path

from config import APVersion
from helpers import read_bytes, read_json, root_path, read_csv, read_plaintext, write_plaintext, write_bytes


def get_chest_definitions() -> List[Dict]:
    chest_definitions_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Chest Items.csv")
    chest_definitions = read_csv(file_path=chest_definitions_csv_path)
    return chest_definitions


def get_rewards_definitions() -> List[Dict]:
    reward_definitions_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Battle Table Reward Items.csv")
    reward_definitions = read_csv(file_path=reward_definitions_csv_path)
    for reward in reward_definitions:
        if reward["Chest Reference"] == "Link":
            reward["AP Location ID"] = None
        if reward["AP Location ID"] == "":
            reward["AP Location ID"] = None
    return reward_definitions


def get_battle_table(kh1_data_path: Path) -> bytearray:
    battle_table_path = kh1_data_path.joinpath("btltbl.bin")
    battle_data = read_bytes(battle_table_path)
    return battle_data


def get_replacement_short_item(item_index: int) -> int:
    short_value = item_index * 0x10
    return short_value


def get_replacement_short_reward(reward_index: int) -> int:
    short_value = (reward_index * 0x10) + 0xE
    return short_value


def get_chest_replacement(item_id: int, reward_definitions: List[Dict], location_id: int, location_name: str) -> Tuple[int, List[Dict]]:
    item_id = item_id % 264000
    if item_id > 1000 and item_id < 2000: # Stock Item
        replacement_short = get_replacement_short_item(item_id % 1000)
    elif item_id > 2000 and item_id < 4000: # Ability
        reward_index = get_unused_reward_index(reward_definitions)
        reward_definitions[reward_index]["AP Location ID"] = location_id
        reward_definitions[reward_index]["AP Location Name"] = location_name
        replacement_short = get_replacement_short_reward(reward_index)
    else:
        print("Not normal item, replacing with generic AP Item")
        replacement_short = get_replacement_short_item(230)
    return replacement_short, reward_definitions


def get_reward_replacement(item_id: int) -> List[int]:
    item_id = item_id % 264000
    if item_id > 1000 and item_id < 2000: # Regular Item
        return [0xF0, item_id % 1000]
    elif item_id > 2000 and item_id < 3000: # Shared Ability
        return [0xB1, item_id % 2000]
    elif item_id > 3000 and item_id < 4000: # Sora Ability
        return [0x01, item_id % 3000]
    else:
        print("Not normal item, replacing with generic AP Item")
        return [0xF0, 230]


def get_unused_reward_index(reward_definitions: List[Dict]) -> int:
    i = 0
    while i < len(reward_definitions):
        if reward_definitions[i]["AP Location ID"] is None:
            return i
        i = i + 1


def get_all_chest_replacements(chest_definitions: List[Dict], reward_definitions: List[Dict], seed_json_data: Dict) -> Tuple[Dict, List[Dict]]:
    replacements = {}
    for chest_definition in chest_definitions:
        print("Getting replacement byte for chest location: " + chest_definition["AP Location Name"] + " with offset " + chest_definition["Offset"])
        if chest_definition["AP Location ID"] in seed_json_data.keys():
            replacement_short, reward_definitions = get_chest_replacement(seed_json_data[chest_definition["AP Location ID"]], reward_definitions, chest_definition["AP Location ID"], chest_definition["AP Location Name"])
        else:
            print("Location ID not found in seed JSON data, replacing with Potion")
            replacement_short, reward_definitions = get_chest_replacement(2641001, reward_definitions, None, None)
        print("Replacement short: " + str(replacement_short))
        replacements[int(chest_definition["Offset"], 16)] = replacement_short
    return replacements, reward_definitions


def get_all_reward_replacements(reward_definitions: List[Dict], seed_json_data: Dict) -> Dict:
    replacements = {}
    for reward in reward_definitions:
        if reward["AP Location ID"] is not None:
            print("Getting replacement byte for reward location: " + reward["AP Location Name"] + " with offset " + reward["Offset"])
            if reward["AP Location ID"] in seed_json_data.keys():
                replacement_bytes = get_reward_replacement(seed_json_data[reward["AP Location ID"]])
            else:
                print("Location ID not found in seed JSON data, replacing with Potion")
                replacement_bytes = [0xF0, 1]
            replacements[int(reward["Offset"], 16)] = replacement_bytes
            print("Replacement bytes: " + str(replacement_bytes))
    return replacements


def get_chest_template_lua() -> str:
    chest_template_path = root_path().joinpath("Template Luas", "1fmRandoChests.lua")
    chests_lua_str = read_plaintext(file_path=chest_template_path)
    return chests_lua_str


def update_chest_lua(chests_lua_str: str, replacements: Dict) -> str:
    return chests_lua_str.replace("chests = {}", "chests = " + json.dumps(replacements).replace("{\"", "{[").replace("\":", "] =").replace(", \"", ", ["))


def update_battle_table(battle_table_bytes: bytearray, replacements: Dict) -> bytearray:
    for replacement_offset in replacements.keys():
        battle_table_bytes[replacement_offset - 1] = replacements[replacement_offset][0]
        battle_table_bytes[replacement_offset] = replacements[replacement_offset][1]
    return battle_table_bytes


def output_chest_lua_file(chest_lua_str: str) -> None:
    rando_chest_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoChests.lua")
    write_plaintext(file_path=rando_chest_lua_path, data=chest_lua_str, overwrite=True, create_parents=True)    


def output_battle_table(battle_table_bytes: bytearray) -> None:
    rando_battle_table_path = root_path().joinpath("Working", "btltbl.bin")
    write_bytes(file_path=rando_battle_table_path, data=bytes(battle_table_bytes), overwrite=True, create_parents=True)


def write_chests_and_rewards(seed_json_file = None, version: APVersion = APVersion.AP_DEV) -> None:
    kh1_data_path = root_path().joinpath("Working")
    chest_definitions = get_chest_definitions()
    reward_definitions = get_rewards_definitions()
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=False)
    chest_replacements, reward_definitions = get_all_chest_replacements(chest_definitions, reward_definitions, seed_json_data)
    reward_replacements = get_all_reward_replacements(reward_definitions, seed_json_data)
    chest_template_lua = get_chest_template_lua()
    chest_lua = update_chest_lua(chest_template_lua, chest_replacements)
    output_chest_lua_file(chest_lua)
    battle_table_bytes = get_battle_table(kh1_data_path)
    updated_battle_table = update_battle_table(battle_table_bytes, reward_replacements)
    output_battle_table(updated_battle_table)

if __name__=="__main__":
    write_chests_and_rewards()