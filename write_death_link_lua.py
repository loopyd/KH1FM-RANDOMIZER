from typing import Dict

from config import APVersion
from helpers import read_plaintext, root_path, read_json, write_plaintext


def get_death_link_template_lua() -> str:
    rando_death_link_lua_path = root_path().joinpath("Template Luas", "1fmRandoHandleDeathLink.lua")
    death_link_lua_str = read_plaintext(file_path=rando_death_link_lua_path)
    return death_link_lua_str


def update_death_link_lua(death_link_lua_str: str, settings_data: Dict) -> str:
    if settings_data["donald_death_link"]:
        death_link_lua_str = death_link_lua_str.replace("local donald_death_link = false", "local donald_death_link = true")
    # FIX: Replace with "goofy death link" instead of "donald death link", this seemed like a bug...
    if settings_data["goofy_death_link"]:
        death_link_lua_str = death_link_lua_str.replace("local goofy_death_link = false", "local goofy_death_link = true")
    if settings_data["death_link"] != "off":
        death_link_lua_str = death_link_lua_str.replace("local death_link = false", "local death_link = true")
    return death_link_lua_str


def output_death_link_lua_file(death_link_lua_str: str) -> None:
    rando_death_link_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoHandleDeathLink.lua")
    write_plaintext(file_path=rando_death_link_lua_path, data=death_link_lua_str, overwrite=True, create_parents=True)


def write_death_link_lua(settings_file = None, version: APVersion = APVersion.AP_DEV):
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    if settings_data["death_link"] != "off" or settings_data["donald_death_link"] or settings_data["goofy_death_link"]:
        death_link_lua_str = get_death_link_template_lua()
        death_link_lua_str = update_death_link_lua(death_link_lua_str, settings_data)
        output_death_link_lua_file(death_link_lua_str)


if __name__ == "__main__":
    write_death_link_lua()