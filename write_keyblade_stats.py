from pathlib import Path
from typing import Dict, List

from config import ResourceType, read_data, write_data
from definitions import keyblade_list
from write_item_descriptions import replace_specific_item_description


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


def write_keyblade_stats(seed_json_file: Path | None = None) -> None:
    seed_json_file = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    battle_table_bytes = read_data(kind=ResourceType.BIN, key="battle_table")
    weapon_definitions = read_data(kind=ResourceType.CSV, key="weapon_stat_definitions")
    battle_table_bytes = write_weapon_stats(battle_table_bytes, weapon_definitions, seed_json_file)
    write_data(kind=ResourceType.BIN, data=battle_table_bytes, key="battle_table", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_keyblade_stats()