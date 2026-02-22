from typing import Dict
from pathlib import Path

from config import ResourceType, read_data, write_data


def update_lucky_emblems_eotw_lua(lucky_emblems_lua_str: str, settings_data: Dict) -> str:
    lucky_emblems_lua_str = lucky_emblems_lua_str.replace("eotw_lucky_emblems = 100", "eotw_lucky_emblems = " + str(settings_data["required_lucky_emblems_eotw"]))
    return lucky_emblems_lua_str


def update_lucky_emblems_door_lua(lucky_emblems_lua_str: str, settings_data: Dict) -> str:
    lucky_emblems_lua_str = lucky_emblems_lua_str.replace("door_lucky_emblems = 100", "door_lucky_emblems = " + str(settings_data["required_lucky_emblems_door"]))
    return lucky_emblems_lua_str

def write_lucky_emblems_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if settings_data.get("end_of_the_world_unlock", None) == "lucky_emblems" or settings_data.get("final_rest_door_key", None) == "lucky_emblems":
        lucky_emblems_lua_str = read_data(kind=ResourceType.LUA, key="template_lucky_emblems")
        if settings_data.get("end_of_the_world_unlock", None) == "lucky_emblems":
            lucky_emblems_lua_str = update_lucky_emblems_eotw_lua(lucky_emblems_lua_str, settings_data)
        if settings_data.get("final_rest_door_key", None) == "lucky_emblems":
            lucky_emblems_lua_str = update_lucky_emblems_door_lua(lucky_emblems_lua_str, settings_data)
        write_data(kind=ResourceType.LUA, data=lucky_emblems_lua_str, key="output_lucky_emblems", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_lucky_emblems_lua()