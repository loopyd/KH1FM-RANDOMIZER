from pathlib import Path
from typing import Dict, List

from definitions import keyblade_list
from write_item_descriptions import replace_specific_item_description
from helpers import root_path, read_json, read_csv, read_bytes, write_bytes


def get_seed_keyblade_stats_data(seed_json_file: Path | None = None) -> List[Dict]:
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=True)
    return seed_json_data


def get_battle_table(kh1_data_path: Path) -> bytearray:
    battle_table_path = kh1_data_path.joinpath("btltbl.bin")
    battle_data = read_bytes(battle_table_path)
    return battle_data


def get_weapon_stat_definitions() -> List[Dict]:
    weapon_stats_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Weapon Stats.csv")
    weapon_definitions = read_csv(file_path=weapon_stats_csv_path)
    return weapon_definitions


def get_weapon_byte_offset(weapon_definitions: List[Dict], stat: str, keyblade: str, user: str):
    for weapon in weapon_definitions:
        if stat == weapon["Notes"] and keyblade == weapon["Keyblade"] and weapon["User"] == user:
            return weapon["Offset"]


def write_weapon_stats(battle_table_data: bytearray, weapon_definitions: List[Dict], keyblade_stats_data: List[Dict]) -> bytearray:
    i = 0
    while i < len(keyblade_list):
        if "STR" in keyblade_stats_data[i].keys():
            offset = get_weapon_byte_offset(weapon_definitions, "Strength", keyblade_list[i], "Sora")
            offset = int(offset,16)
            value = keyblade_stats_data[i]["STR"].to_bytes(1)
            if offset is not None:
                battle_table_data[offset] = int.from_bytes(value)
                print("Replaced STR of keyblade " + keyblade_list[i] + " with value " + str(keyblade_stats_data[i]["STR"]))
        if "CRR" in keyblade_stats_data[i].keys():
            offset = get_weapon_byte_offset(weapon_definitions, "Crit Percentage", keyblade_list[i], "Sora")
            offset = int(offset,16)
            value = keyblade_stats_data[i]["CRR"].to_bytes(1)
            if offset is not None:
                battle_table_data[offset] = int.from_bytes(value)
                print("Replaced CRR of keyblade " + keyblade_list[i] + " with value " + str(keyblade_stats_data[i]["CRR"]))
        if "CRB" in keyblade_stats_data[i].keys():
            offset = get_weapon_byte_offset(weapon_definitions, "Crit Bonus", keyblade_list[i], "Sora")
            offset = int(offset,16)
            value = keyblade_stats_data[i]["CRB"].to_bytes(1)
            if offset is not None:
                battle_table_data[offset] = int.from_bytes(value)
                print("Replaced CRB of keyblade " + keyblade_list[i] + " with value " + str(keyblade_stats_data[i]["CRB"]))
        if "REC" in keyblade_stats_data[i].keys():
            offset = get_weapon_byte_offset(weapon_definitions, "Recoil", keyblade_list[i], "Sora")
            offset = int(offset,16)
            value = keyblade_stats_data[i]["REC"].to_bytes(1)
            if offset is not None:
                battle_table_data[offset] = int.from_bytes(value)
                print("Replaced REC of keyblade " + keyblade_list[i] + " with value " + str(keyblade_stats_data[i]["REC"]))
        if "MP" in keyblade_stats_data[i].keys():
            offset = get_weapon_byte_offset(weapon_definitions, "MP", keyblade_list[i], "Sora")
            offset = int(offset,16)
            value = keyblade_stats_data[i]["MP"].to_bytes(1, signed=True)
            if offset is not None:
                battle_table_data[offset] = int.from_bytes(value)
                print("Replaced MP of keyblade " + keyblade_list[i] + " with value " + str(keyblade_stats_data[i]["MP"]))
        keyblade_description = ""
        keyblade_description = keyblade_description + "STR " + str(keyblade_stats_data[i]["STR"]) + " "
        keyblade_description = keyblade_description + "CRR " + str(keyblade_stats_data[i]["CRR"]) + " "
        keyblade_description = keyblade_description + "CRB " + str(keyblade_stats_data[i]["CRB"]) + " "
        keyblade_description = keyblade_description + "REC " + str(keyblade_stats_data[i]["REC"]) + " "
        keyblade_description = keyblade_description + "MP " + str(keyblade_stats_data[i]["MP"]) + "."
        replace_specific_item_description(i + 81, keyblade_description)
        i = i + 1
    return battle_table_data


def output_battle_table(battle_table_bytes: bytearray) -> None:
    battle_table_path = root_path().joinpath("Working", "btltbl.bin")
    write_bytes(file_path=battle_table_path, data=battle_table_bytes, overwrite=True, create_parents=True)


def write_keyblade_stats(seed_json_file = None):
    kh1_data_path = root_path().joinpath("Working")
    keyblade_stats_data = get_seed_keyblade_stats_data(seed_json_file)
    battle_table_bytes = get_battle_table(kh1_data_path)
    weapon_definitions = get_weapon_stat_definitions()
    battle_table_bytes = write_weapon_stats(battle_table_bytes, weapon_definitions, keyblade_stats_data)
    output_battle_table(battle_table_bytes)


if __name__ == "__main__":
    write_keyblade_stats()