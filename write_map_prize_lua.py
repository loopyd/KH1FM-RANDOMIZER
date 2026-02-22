from pathlib import Path
from typing import Dict

from config import ResourceType, read_data, write_data
from definitions import filler_item_ids


def update_map_prize_template_lua(map_prize_lua_str: str, seed_json_data: Dict) -> str:
    map_prize_location_ids = [
        2656600,
        2656601,
        2656602,
        2656603,
        2656604,
        2656605,
        2656606,
        2656607,
        2656608,
        2656609,
        2656610,
        2656611,
        2656612,
        2656613,
        2656614,
        2656615,
        2656616,
        2656617,
        2656618,
        2656619,
        2656620,
        2656621,
        2656622,
        2656623
    ]
    for map_prize_location_id in map_prize_location_ids:
        replace = "0"
        if str(map_prize_location_id) in seed_json_data.keys():
            item = seed_json_data[str(map_prize_location_id)] % 2641000
            if item <= 255 and int(item) not in filler_item_ids and item != 230:
                replace = str(item)
        map_prize_lua_str = map_prize_lua_str.replace("replace_" + str(map_prize_location_id), str(replace))
    return map_prize_lua_str





def write_map_prize_lua(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    map_prize_lua_str = read_data(kind=ResourceType.LUA, key="template_map_prize")
    map_prize_lua_str = update_map_prize_template_lua(map_prize_lua_str, seed_json_data)
    write_data(kind=ResourceType.LUA, data=map_prize_lua_str, key="output_map_prize", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_map_prize_lua()