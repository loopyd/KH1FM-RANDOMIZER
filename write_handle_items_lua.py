from typing import Dict
from pathlib import Path

from helpers import read_json, write_plaintext, read_plaintext, root_path


def get_settings_data(settings_file: Path | None = None) -> Dict:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    return settings_data

def get_handle_items_lua() -> str:
    handle_items_lua_path = root_path().joinpath("Template Luas", "1fmRandoHandleItems.lua")
    handle_items_lua_str = read_plaintext(file_path=handle_items_lua_path)
    return handle_items_lua_str


def update_puppies_handle_items_lua(handle_items_lua_str: str, settings_data: Dict) -> str:
    handle_items_lua_str = handle_items_lua_str.replace("puppy_value = 3", "puppy_value = " + str(settings_data["puppy_value"]))
    return handle_items_lua_str


def update_stacking_worlds(handle_items_lua_str: str, settings_data: Dict) -> str:
    handle_items_lua_str = handle_items_lua_str.replace("stacking_worlds = false", "stacking_worlds = " + str(settings_data["stacking_world_items"]).lower())
    return handle_items_lua_str


def update_stacking_forget_me_not(handle_items_lua_str: str, settings_data: Dict) -> str:
    handle_items_lua_str = handle_items_lua_str.replace("stacking_forget_me_not = false", "stacking_forget_me_not = " + str(settings_data["halloween_town_key_item_bundle"]).lower())
    return handle_items_lua_str


def output_handle_items_lua_file(handle_items_lua_str: str) -> None:
    handle_items_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoHandleItems.lua")
    write_plaintext(file_path=handle_items_lua_path, data=handle_items_lua_str, overwrite=True, create_parents=True)


def write_handle_items_lua(settings_file: Path | None = None):
    settings_data = get_settings_data(settings_file)
    handle_items_lua_str = get_handle_items_lua()
    handle_items_lua_str = update_puppies_handle_items_lua(handle_items_lua_str, settings_data)
    handle_items_lua_str = update_stacking_worlds(handle_items_lua_str, settings_data)
    handle_items_lua_str = update_stacking_forget_me_not(handle_items_lua_str, settings_data)
    output_handle_items_lua_file(handle_items_lua_str)


if __name__ == "__main__":
    write_handle_items_lua()