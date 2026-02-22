from typing import Dict
from pathlib import Path

from config import ResourceType, read_data, write_data
from helpers import boolify


def update_puppies_handle_items_lua(handle_items_lua_str: str, settings_data: Dict) -> str:
    puppy_value = settings_data.get("puppy_value", 3)
    handle_items_lua_str = handle_items_lua_str.replace("puppy_value = 3", "puppy_value = " + str(puppy_value))
    return handle_items_lua_str


def update_stacking_worlds(handle_items_lua_str: str, settings_data: Dict) -> str:
    stacking_world_items = str(boolify(settings_data.get("stacking_world_items", False))).lower()
    handle_items_lua_str = handle_items_lua_str.replace("stacking_worlds = false", f"stacking_worlds = {stacking_world_items}")
    return handle_items_lua_str


def update_stacking_forget_me_not(handle_items_lua_str: str, settings_data: Dict) -> str:
    haloween_town_key_item_bundle = str(boolify(settings_data.get("halloween_town_key_item_bundle", False))).lower()
    handle_items_lua_str = handle_items_lua_str.replace("stacking_forget_me_not = false", f"stacking_forget_me_not = {haloween_town_key_item_bundle}")
    return handle_items_lua_str

def write_handle_items_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    handle_items_lua_str = read_data(kind=ResourceType.LUA, key="template_handle_items")
    handle_items_lua_str = update_puppies_handle_items_lua(handle_items_lua_str, settings_data)
    handle_items_lua_str = update_stacking_worlds(handle_items_lua_str, settings_data)
    handle_items_lua_str = update_stacking_forget_me_not(handle_items_lua_str, settings_data)
    write_data(kind=ResourceType.LUA, data=handle_items_lua_str, key="output_handle_items", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_handle_items_lua()