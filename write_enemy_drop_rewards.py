from typing import Dict, List

from config import ResourceType, read_data, write_data
from definitions import filler_item_ids

def remove_enemy_synth_drops(enemy_bytes: bytearray, enemy_drop_definitions: List[Dict]) -> bytearray:
    for enemy_drop_definition in enemy_drop_definitions:
        if enemy_drop_definition["Notes"].startswith("Drop"):
            if int(enemy_drop_definition["Value"]) not in filler_item_ids:
                offset = int(enemy_drop_definition["Offset"], 16)
                enemy_bytes[offset-4] = 0
                enemy_bytes[offset-3] = 0
                enemy_bytes[offset-2] = 0
                enemy_bytes[offset-1] = 0
                enemy_bytes[offset] = 0
                enemy_bytes[offset+1] = 0
                enemy_bytes[offset+2] = 0
                enemy_bytes[offset+3] = 0
    return enemy_bytes


def sort_enemy_drop_definitions(enemy_drop_definitions: List[Dict]) -> Dict:
    sorted_enemy_drop_definitions = {}
    for enemy_drop_definition in enemy_drop_definitions:
        if enemy_drop_definition["File"] not in sorted_enemy_drop_definitions.keys():
            sorted_enemy_drop_definitions[enemy_drop_definition["File"]] = []
        sorted_enemy_drop_definitions[enemy_drop_definition["File"]].append(enemy_drop_definition)
    return sorted_enemy_drop_definitions


def write_enemy_drop_rewards() -> None:
    enemy_drop_definitions = read_data(kind=ResourceType.CSV, key="enemy_drop_definitions")
    sorted_enemy_drop_definitions = sort_enemy_drop_definitions(enemy_drop_definitions)
    for file in sorted_enemy_drop_definitions.keys():
        enemy_bytes = read_data(kind=ResourceType.BIN, path_parts=("Working", file))
        enemy_bytes = remove_enemy_synth_drops(enemy_bytes, sorted_enemy_drop_definitions[file])
        write_data(kind=ResourceType.BIN, data=enemy_bytes, path_parts=("Working", file), overwrite=True, create_parents=True)



if __name__=="__main__":
    write_enemy_drop_rewards()