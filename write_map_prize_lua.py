from pathlib import Path
from typing import Dict

from definitions import filler_item_ids
from helpers import root_path, read_json, read_plaintext, write_plaintext


def get_map_prize_template_lua() -> str:
    rando_map_prizes_lua_path = root_path().joinpath("Template Luas", "1fmRandoMapPrizes.lua")
    map_prize_lua_str = read_plaintext(file_path=rando_map_prizes_lua_path)
    return map_prize_lua_str


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


def output_map_prize_lua_file(map_prize_lua_str: str) -> None:
    map_prize_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoMapPrizes.lua")
    write_plaintext(file_path=map_prize_lua_path, content=map_prize_lua_str)


def write_map_prize_lua(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=False)
    map_prize_lua_str = get_map_prize_template_lua()
    map_prize_lua_str = update_map_prize_template_lua(map_prize_lua_str, seed_json_data)
    output_map_prize_lua_file(map_prize_lua_str)


if __name__ == "__main__":
    write_map_prize_lua()