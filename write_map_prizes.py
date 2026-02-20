from pathlib import Path
from typing import Dict, List

from helpers import root_path, read_bytes, read_csv, write_bytes, read_json

def get_map_prize_definitions() -> List[Dict]:
    map_prize_definitions_path = root_path().joinpath("Documentation", "KH1FM Documentation - Map Prizes.csv")
    map_prize_definitions = read_csv(file_path=map_prize_definitions_path)
    return map_prize_definitions


def get_map_prize_data(kh1_data_path: Path) -> bytearray:
    map_prize_data_path = kh1_data_path.joinpath("map_prize.bin")
    map_prize_data = read_bytes(file_path=map_prize_data_path)
    return map_prize_data


def remove_map_prizes(map_prize_bytes: bytearray, map_prize_definitions) -> bytearray:
    for map_prize_definition in map_prize_definitions:
        offset = int(map_prize_definition["Offset"],16)
        for i in range(23):
            map_prize_bytes[offset + i] = 0
    return map_prize_bytes


def write_map_prize_bin(map_prize_bytes: bytearray) -> None:
    map_prize_path = root_path().joinpath("Working", "map_prize.bin")
    write_bytes(file_path=map_prize_path, data=map_prize_bytes, overwrite=True, create_parents=True)


def replace_map_prize_items(map_prize_bytes: bytearray, map_prize_definitions: List[Dict], seed_json_data: Dict):
    for map_prize_definition in map_prize_definitions:
        if map_prize_definition["AP Location ID"] != "-":
            offset = int(map_prize_definition["Offset"],16)
            item = seed_json_data[map_prize_definition["AP Location ID"]] % 264100
            if item > 255: # If its an ability, must have been placed there as remote_items was set to allow
                item = 230 # Make it AP item, the item must be remote.
            map_prize_bytes[offset + 7] = 100
            map_prize_bytes[offset + 8] = item
    return map_prize_bytes


def write_map_prizes(seed_json_file: Path | None = None) -> None:
    kh1_data_path = root_path().joinpath("Working")
    map_prize_definitions = get_map_prize_definitions()
    map_prize_data = get_map_prize_data(kh1_data_path)
    map_prize_bytes = remove_map_prizes(map_prize_data, map_prize_definitions)
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=False)
    map_prize_bytes = replace_map_prize_items(map_prize_bytes, map_prize_definitions, seed_json_data)
    write_map_prize_bin(map_prize_bytes)


if __name__=="__main__":
    write_map_prizes()