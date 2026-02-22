from pathlib import Path

from config import ResourceType, read_data, write_data
from helpers import boolify


def update_destiny_islands_lua_str(destiny_islands_lua_str: str, day_2_materials: int, homecoming_materials: int) -> str:
    destiny_islands_lua_str = destiny_islands_lua_str.replace("day_2_materials = 0", "day_2_materials = " + str(day_2_materials))
    destiny_islands_lua_str = destiny_islands_lua_str.replace("homecoming_materials = 0", "homecoming_materials = " + str(homecoming_materials))
    return destiny_islands_lua_str


def write_destiny_islands_lua(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=False)
    if boolify(settings_data.get("destiny_islands", False)):
        day_2_materials = settings_data.get("day_2_materials", 0)
        homecoming_materials = settings_data.get("homecoming_materials", 0)
        destiny_islands_lua_str = read_data(kind=ResourceType.LUA, key="template_destiny_islands")
        destiny_islands_lua_str = update_destiny_islands_lua_str(destiny_islands_lua_str, day_2_materials, homecoming_materials)
        write_data(kind=ResourceType.LUA, data=destiny_islands_lua_str, key="output_destiny_islands", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_destiny_islands_lua()