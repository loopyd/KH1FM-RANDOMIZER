from typing import Dict
from pathlib import Path

from helpers import root_path, read_json, read_plaintext, write_plaintext


def get_lucky_emblems_template_lua() -> str:
    rando_lucky_emblems_lua_path = root_path().joinpath("Template Luas", "1fmRandoHandleLuckyEmblems.lua")
    lucky_emblems_lua_str = read_plaintext(file_path=rando_lucky_emblems_lua_path)
    return lucky_emblems_lua_str


def update_lucky_emblems_eotw_lua(lucky_emblems_lua_str: str, settings_data: Dict) -> str:
    lucky_emblems_lua_str = lucky_emblems_lua_str.replace("eotw_lucky_emblems = 100", "eotw_lucky_emblems = " + str(settings_data["required_lucky_emblems_eotw"]))
    return lucky_emblems_lua_str


def update_lucky_emblems_door_lua(lucky_emblems_lua_str: str, settings_data: Dict) -> str:
    lucky_emblems_lua_str = lucky_emblems_lua_str.replace("door_lucky_emblems = 100", "door_lucky_emblems = " + str(settings_data["required_lucky_emblems_door"]))
    return lucky_emblems_lua_str

def output_lucky_emblems_lua_file(lucky_emblems_lua_str: str) -> None:
    lucky_emblems_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoHandleLuckyEmblems.lua")
    write_plaintext(file_path=lucky_emblems_lua_path, content=lucky_emblems_lua_str)


def write_lucky_emblems_lua(settings_file: Path | None = None) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    if settings_data["end_of_the_world_unlock"] == "lucky_emblems" or settings_data["final_rest_door_key"] == "lucky_emblems":
        lucky_emblems_lua_str = get_lucky_emblems_template_lua()
        if settings_data["end_of_the_world_unlock"] == "lucky_emblems":
            lucky_emblems_lua_str = update_lucky_emblems_eotw_lua(lucky_emblems_lua_str, settings_data)
        if settings_data["final_rest_door_key"] == "lucky_emblems":
            lucky_emblems_lua_str = update_lucky_emblems_door_lua(lucky_emblems_lua_str, settings_data)
        output_lucky_emblems_lua_file(lucky_emblems_lua_str)


if __name__ == "__main__":
    write_lucky_emblems_lua()