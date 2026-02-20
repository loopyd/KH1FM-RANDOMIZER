from pathlib import Path

from helpers import read_json, root_path, read_plaintext, write_plaintext


def get_lua_str(lua_file_name: Path) -> str:
    lua_path = root_path().joinpath("Template Luas", lua_file_name)
    lua_str = read_plaintext(file_path=lua_path)
    return lua_str


def output_lua_file(lua_str: str, lua_file_name: Path) -> None:
    lua_path = root_path().joinpath("Working", "scripts", lua_file_name)
    write_plaintext(file_path=lua_path, data=lua_str, overwrite=True, create_parents=True)


def write_synthesis_item_names_lua(settings_file: Path | None = None) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    synthesis_item_names_bytes_array = settings_data["synthesis_item_name_byte_arrays"]
    synth_item_bytes_str = str(synthesis_item_names_bytes_array).replace("[", "{").replace("]", "}")
    synthesis_item_names_lua_str = get_lua_str("1fmRandoWriteSynthesisItemNames.lua")
    synthesis_item_names_lua_str = synthesis_item_names_lua_str.replace("synth_item_bytes = {}", "synth_item_bytes = " + str(synth_item_bytes_str))
    output_lua_file(synthesis_item_names_lua_str, "1fmRandoWriteSynthesisItemNames.lua")

if __name__ == "__main__":
    write_synthesis_item_names_lua()