from pathlib import Path
from typing import Dict, List

from definitions import sora_ability_item_ids
from helpers import root_path, read_csv, read_json, read_bytes, write_bytes


def get_level_up_stats_definitions() -> List[Dict]:
    battle_table_sora_level_up_stats_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Battle Table Sora Level Up Stats.csv")
    level_up_stats_definitions = read_csv(file_path=battle_table_sora_level_up_stats_csv_path)
    return level_up_stats_definitions


def get_level_up_abilities_definitions() -> List[Dict]:
    level_up_abilities_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Battle Table Sora Level Up Abilities.csv")
    level_up_abilities_definitions = read_csv(file_path=level_up_abilities_csv_path)
    return level_up_abilities_definitions


def get_battle_table(kh1_data_path: Path) -> bytearray:
    battle_table_path = kh1_data_path.joinpath("btltbl.bin")
    battle_data = read_bytes(battle_table_path)
    return battle_data


def update_battle_table(battle_table_bytes: bytearray, replacements: Dict[int, int]) -> bytearray:
    for replacement_offset in replacements.keys():
        battle_table_bytes[replacement_offset] = replacements[replacement_offset]
    return battle_table_bytes


def get_battle_table_replacements(level_up_stats_definitions: List[Dict], level_up_abilities_definitions: List[Dict], seed_json_data: Dict) -> Dict[int, int]:
    replacements = {}
    for level_up_stats_definition in level_up_stats_definitions:
        location_id = level_up_stats_definition["AP Location ID"]
        offset = int(level_up_stats_definition["Offset"],16)
        print("Getting replacement byte for level up location: " + level_up_stats_definition["AP Location Name"] + " with offset " + level_up_stats_definition["Offset"])
        replacements[offset] = 0
        if location_id in seed_json_data.keys():
            item_id = seed_json_data[location_id]
            if item_id >= 2641239 and item_id <= 2641245:
                replacements[offset] = (item_id % 2641239) + 1
        print("New value for level up location: " + level_up_stats_definition["AP Location Name"] + " with offset " + level_up_stats_definition["Offset"] + " is " + str(replacements[offset]))
    for level_up_abilities_definition in level_up_abilities_definitions:
        location_id = level_up_abilities_definition["AP Location ID"]
        offset = int(level_up_abilities_definition["Offset"],16)
        print("Getting replacement byte for level up location: " + level_up_abilities_definition["AP Location Name"] + " with offset " + level_up_abilities_definition["Offset"])
        replacements[offset] = 0
        if location_id in seed_json_data.keys():
            item_id = seed_json_data[location_id]
            if item_id >= 2641239 and item_id <= 2641245:
                replacements[offset] = (item_id % 2641239) + 1
            elif item_id in sora_ability_item_ids:
                replacements[offset] = item_id % 2643000 + 0x80
        print("New value for level up location: " + level_up_abilities_definition["AP Location Name"] + " with offset " + level_up_abilities_definition["Offset"] + " is " + str(replacements[offset]))
    return replacements


def output_battle_table(battle_table_bytes: bytearray) -> None:
    battle_table_path = root_path().joinpath("Working", "btltbl.bin")
    write_bytes(file_path=battle_table_path, data=battle_table_bytes, overwrite=True, create_parents=True)
    

def write_level_up_rewards(seed_json_file: Path | None = None) -> None:
    kh1_data_path = root_path().joinpath("Working")
    level_up_abilities_definitions = get_level_up_abilities_definitions()
    level_up_stats_definitions = get_level_up_stats_definitions()
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=False)
    replacements = get_battle_table_replacements(level_up_stats_definitions, level_up_abilities_definitions, seed_json_data)
    battle_table_bytes = get_battle_table(kh1_data_path)
    battle_table_bytes = update_battle_table(battle_table_bytes, replacements)
    output_battle_table(battle_table_bytes)


if __name__ == "__main__":
    write_level_up_rewards()