from pathlib import Path
from typing import Dict

from config import ResourceType, read_data, write_data
from helpers import boolify


def update_death_link_lua(death_link_lua_str: str, settings_data: Dict) -> str:
    if boolify(settings_data.get("donald_death_link", False)):
        death_link_lua_str = death_link_lua_str.replace("local donald_death_link = false", "local donald_death_link = true")
    if boolify(settings_data.get("goofy_death_link", False)):
        death_link_lua_str = death_link_lua_str.replace("local goofy_death_link = false", "local goofy_death_link = true")
    if boolify(settings_data.get("death_link", False)):
        death_link_lua_str = death_link_lua_str.replace("local death_link = false", "local death_link = true")
    return death_link_lua_str


def write_death_link_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("death_link", False)) or boolify(settings_data.get("donald_death_link", False)) or boolify(settings_data.get("goofy_death_link", False)):
        death_link_lua_str = read_data(kind=ResourceType.LUA, key="template_death_link")
        death_link_lua_str = update_death_link_lua(death_link_lua_str, settings_data)
        write_data(kind=ResourceType.LUA, data=death_link_lua_str, key="output_death_link", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_death_link_lua()