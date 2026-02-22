from pathlib import Path
from typing import Dict, List

from config import APVersion
from definitions import filler_item_ids
from helpers import read_bytes, root_path, read_csv, write_bytes


def get_enemy_drop_definitions() -> List[Dict]:
    enemy_drop_definitions_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Enemy Stats and Drops.csv")
    enemy_drop_definitions = read_csv(file_path=enemy_drop_definitions_csv_path)
    return enemy_drop_definitions


def get_enemy_data(kh1_data_path: Path, file_name: str) -> bytearray:
    data_path = kh1_data_path.joinpath(file_name)
    enemy_data_bytes = read_bytes(data_path)
    return enemy_data_bytes


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



def write_enemy_mdls(enemy_bytes: bytearray, file_name: str) -> None:
    enemy_mdl_path = root_path().joinpath("Working", file_name)
    write_bytes(file_path=enemy_mdl_path, data=enemy_bytes, overwrite=True, create_parents=True)


def sort_enemy_drop_definitions(enemy_drop_definitions: List[Dict]) -> Dict:
    sorted_enemy_drop_definitions = {}
    for enemy_drop_definition in enemy_drop_definitions:
        if enemy_drop_definition["File"] not in sorted_enemy_drop_definitions.keys():
            sorted_enemy_drop_definitions[enemy_drop_definition["File"]] = []
        sorted_enemy_drop_definitions[enemy_drop_definition["File"]].append(enemy_drop_definition)
    return sorted_enemy_drop_definitions


def write_enemy_drop_rewards(version: APVersion = APVersion.AP_DEV) -> None:
    kh1_data_path = root_path().joinpath("Working")
    enemy_drop_definitions = get_enemy_drop_definitions()
    sorted_enemy_drop_definitions = sort_enemy_drop_definitions(enemy_drop_definitions)
    for file in sorted_enemy_drop_definitions.keys():
        enemy_bytes = get_enemy_data(kh1_data_path, file)
        enemy_bytes = remove_enemy_synth_drops(enemy_bytes, sorted_enemy_drop_definitions[file])
        write_enemy_mdls(enemy_bytes, file)


if __name__=="__main__":
    write_enemy_drop_rewards()