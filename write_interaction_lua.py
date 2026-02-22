from typing import Dict
from pathlib import Path

from config import ResourceType, read_data, write_data
from helpers import boolify


def update_interaction_keyblade_lock_lua(interaction_lua_str: str, settings_data: Dict) -> str:
    if boolify(settings_data.get("interact_in_battle", False)):
        interaction_lua_str = interaction_lua_str.replace("interactinbattle = false", "interactinbattle = true")
    return interaction_lua_str


def update_interaction_interact_in_battle_lua(interaction_lua_str: str, settings_data: Dict) -> str:
    if boolify(settings_data.get("keyblades_unlock_chests", False)):
        interaction_lua_str = interaction_lua_str.replace("chestslocked = false", "chestslocked = true")
    return interaction_lua_str


def write_interaction_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("interact_in_battle", False)) or boolify(settings_data.get("keyblades_unlock_chests", False)):
        interaction_lua_str = read_data(kind=ResourceType.LUA, key="template_interaction")
        interaction_lua_str = update_interaction_interact_in_battle_lua(interaction_lua_str, settings_data)
        interaction_lua_str = update_interaction_keyblade_lock_lua(interaction_lua_str, settings_data)
        write_data(kind=ResourceType.LUA, data=interaction_lua_str, key="output_interaction", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_interaction_lua()