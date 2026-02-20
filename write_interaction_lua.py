from typing import Dict
from pathlib import Path

from helpers import read_json, root_path, read_plaintext, write_plaintext

def get_settings_data(settings_file: Path | None = None) -> Dict:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    return settings_data


def get_interaction_template_lua() -> str:
    interaction_lua_path = root_path().joinpath("Template Luas", "1fmRandoInteraction.lua")
    interaction_lua_str = read_plaintext(file_path=interaction_lua_path)
    return interaction_lua_str


def update_interaction_keyblade_lock_lua(interaction_lua_str: str, settings_data: Dict) -> str:
    if settings_data["interact_in_battle"]:
        interaction_lua_str = interaction_lua_str.replace("interactinbattle = false", "interactinbattle = true")
    return interaction_lua_str


def update_interaction_interact_in_battle_lua(interaction_lua_str: str, settings_data: Dict) -> str:
    if settings_data["keyblades_unlock_chests"]:
        interaction_lua_str = interaction_lua_str.replace("chestslocked = false", "chestslocked = true")
    return interaction_lua_str


def output_interaction_lua_file(interaction_lua_str: str) -> None:
    rando_interaction_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoInteraction.lua")
    write_plaintext(file_path=rando_interaction_lua_path, data=interaction_lua_str, overwrite=True, create_parents=True)


def write_interaction_lua(settings_file: Path | None = None):
    settings_data = get_settings_data(settings_file)
    if settings_data["interact_in_battle"] or settings_data["keyblades_unlock_chests"]:
        interaction_lua_str = get_interaction_template_lua()
        interaction_lua_str = update_interaction_interact_in_battle_lua(interaction_lua_str, settings_data)
        interaction_lua_str = update_interaction_keyblade_lock_lua(interaction_lua_str, settings_data)
        output_interaction_lua_file(interaction_lua_str)


if __name__ == "__main__":
    write_interaction_lua()