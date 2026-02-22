
from pathlib import Path
from typing import Dict

from config import APVersion
from helpers import root_path, read_json, read_plaintext, write_plaintext


def get_receive_ap_items_lua() -> str:
    receive_ap_items_lua_path = root_path().joinpath("Template Luas", "1fmRandoReceiveAPItems.lua")
    receive_ap_items_lua_str = read_plaintext(file_path=receive_ap_items_lua_path)
    return receive_ap_items_lua_str


def update_receive_ap_items_lua(receive_ap_items_lua_str: str, settings_data: Dict) -> str:
    receive_ap_items_lua_str = receive_ap_items_lua_str.replace("starting_items = {}", "starting_items = " + str(settings_data["starting_items"]).replace("[", "{").replace("]","}"))
    return receive_ap_items_lua_str


def output_receive_ap_items_lua_file(receive_ap_items_lua_str: str) -> None:
    output_path = root_path().joinpath("Working", "scripts", "1fmRandoReceiveAPItems.lua")
    write_plaintext(file_path=output_path, content=receive_ap_items_lua_str, overwrite=True, create_parents=True)


def write_receive_ap_items_lua(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    receive_ap_items_lua_str = get_receive_ap_items_lua()
    receive_ap_items_lua_str = update_receive_ap_items_lua(receive_ap_items_lua_str, settings_data)
    output_receive_ap_items_lua_file(receive_ap_items_lua_str)


if __name__ == "__main__":
    write_receive_ap_items_lua()