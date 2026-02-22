from pathlib import Path
from typing import List

from config import ResourceType, read_data, write_data


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


def update_synth_lua(synth_lua_str: str, synth_items: List[int]) -> str:
    replace_string = "synth_items = {"
    for item in synth_items:
        replace_string = replace_string + str(item) + ", "
    replace_string = replace_string[:-2] + "}"
    return synth_lua_str.replace("synth_items = {}", replace_string)


def write_synthesis_items(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    synth_items = get_synth_items(seed_json_data)
    synth_lua_str = read_data(kind=ResourceType.LUA, key="template_synth")
    synth_lua_str = update_synth_lua(synth_lua_str, synth_items)
    write_data(kind=ResourceType.LUA, data=synth_lua_str, key="output_synth", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_synthesis_items()