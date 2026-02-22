from pathlib import Path
from typing import Dict, List

from config import ResourceType, read_data, write_data
from definitions import sora_ability_item_ids


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


def write_level_up_rewards(seed_json_file: Path | None = None) -> None:
    level_up_abilities_definitions = read_data(kind=ResourceType.CSV, key="level_up_abilities_definitions")
    level_up_stats_definitions = read_data(kind=ResourceType.CSV, key="level_up_stats_definitions")
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=False)
    replacements = get_battle_table_replacements(level_up_stats_definitions, level_up_abilities_definitions, seed_json_data)
    battle_table_bytes = read_data(kind=ResourceType.BIN, key="battle_table")
    battle_table_bytes = update_battle_table(battle_table_bytes, replacements)
    write_data(kind=ResourceType.BIN, data=battle_table_bytes, key="battle_table", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_level_up_rewards()