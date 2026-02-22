from pathlib import Path
from typing import Dict, List

from config import ResourceType, read_data, write_data


def remove_map_prizes(map_prize_bytes: bytearray, map_prize_definitions) -> bytearray:
    for map_prize_definition in map_prize_definitions:
        offset = int(map_prize_definition["Offset"],16)
        for i in range(23):
            map_prize_bytes[offset + i] = 0
    return map_prize_bytes


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
    map_prize_definitions = read_data(kind=ResourceType.CSV, key="map_prize_definitions")
    map_prize_data = read_data(kind=ResourceType.BIN, key="map_prize")
    map_prize_bytes = remove_map_prizes(map_prize_data, map_prize_definitions)
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    map_prize_bytes = replace_map_prize_items(map_prize_bytes, map_prize_definitions, seed_json_data)
    write_data(kind=ResourceType.BIN, data=map_prize_bytes, key="map_prize", overwrite=True, create_parents=True)


if __name__=="__main__":
    write_map_prizes()