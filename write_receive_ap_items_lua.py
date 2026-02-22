from pathlib import Path
from typing import Dict

from config import ResourceType, read_data, write_data


def update_receive_ap_items_lua(receive_ap_items_lua_str: str, settings_data: Dict) -> str:
    starting_items = str(settings_data["starting_items"]).replace("[", "{").replace("]","}")
    receive_ap_items_lua_str = receive_ap_items_lua_str.replace("starting_items = {}", f"starting_items = {starting_items}")
    return receive_ap_items_lua_str


def write_receive_ap_items_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    receive_ap_items_lua_str = read_data(kind=ResourceType.LUA, key="template_receive_ap_items")
    receive_ap_items_lua_str = update_receive_ap_items_lua(receive_ap_items_lua_str, settings_data)
    write_data(kind=ResourceType.LUA, data=receive_ap_items_lua_str, key="output_receive_ap_items", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_receive_ap_items_lua()