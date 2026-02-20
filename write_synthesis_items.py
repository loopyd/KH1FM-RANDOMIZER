from pathlib import Path
from typing import List

from helpers import root_path, read_json, read_plaintext, write_plaintext


def get_synth_items(seed_json_data) -> List[int]:
    synth_items = []
    i = 1
    while i <= 33:
        synth_item_id = seed_json_data[str(2656400 + i)] % 2641000
        if synth_item_id > 255: # If not a regular item
            synth_item_id = 230 # Make it an AP Item
        synth_items.append(synth_item_id)
        i = i + 1
    return synth_items

def get_synth_template_lua() -> str:
    lua_path = root_path().joinpath("Template Luas", "1fmRandoSynthesis.lua")
    synth_lua_str = read_plaintext(file_path=lua_path)
    return synth_lua_str


def update_synth_lua(synth_lua_str: str, synth_items: List[int]) -> str:
    replace_string = "synth_items = {"
    for item in synth_items:
        replace_string = replace_string + str(item) + ", "
    replace_string = replace_string[:-2] + "}"
    return synth_lua_str.replace("synth_items = {}", replace_string)


def output_synth_lua_file(synth_lua_str: str) -> None:
    lua_path = root_path().joinpath("Working", "scripts", "1fmRandoSynthesis.lua")
    write_plaintext(file_path=lua_path, data=synth_lua_str, overwrite=True, create_parents=True)


def write_synthesis_items(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=True)
    synth_items = get_synth_items(seed_json_data)
    synth_lua_str = get_synth_template_lua()
    synth_lua_str = update_synth_lua(synth_lua_str, synth_items)
    output_synth_lua_file(synth_lua_str)


if __name__ == "__main__":
    write_synthesis_items()