from pathlib import Path

from config import ResourceType, read_data, write_data


def write_synthesis_item_names_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    synthesis_item_names_bytes_array = settings_data.get("synthesis_item_name_byte_arrays", [])
    synth_item_bytes_str = str(synthesis_item_names_bytes_array).replace("[", "{").replace("]", "}")
    synthesis_item_names_lua_str = read_data(kind=ResourceType.LUA, key="template_synth_names")
    synthesis_item_names_lua_str = synthesis_item_names_lua_str.replace("synth_item_bytes = {}", "synth_item_bytes = " + str(synth_item_bytes_str))
    write_data(
        kind=ResourceType.LUA,
        data=synthesis_item_names_lua_str,
        key="output_synth_names",
        overwrite=True,
        create_parents=True,
    )

if __name__ == "__main__":
    write_synthesis_item_names_lua()