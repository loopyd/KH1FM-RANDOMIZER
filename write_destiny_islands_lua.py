from pathlib import Path

from config import APVersion
from helpers import read_plaintext, root_path, write_plaintext, read_json



def get_destiny_islands_lua_str() -> str:
    rando_destiny_islands_lua_path = root_path().joinpath("Template Luas", "1fmRandoAllowDestinyIslands.lua")
    destiny_islands_lua_str = read_plaintext(file_path=rando_destiny_islands_lua_path)
    return destiny_islands_lua_str


def output_destiny_islands_lua_file(destiny_islands_lua_str: str) -> None:
    rando_destiny_islands_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoAllowDestinyIslands.lua")
    write_plaintext(file_path=rando_destiny_islands_lua_path, data=destiny_islands_lua_str, overwrite=True, create_parents=True)


def update_destiny_islands_lua_str(destiny_islands_lua_str: str, day_2_materials: int, homecoming_materials: int) -> str:
    destiny_islands_lua_str = destiny_islands_lua_str.replace("day_2_materials = 0", "day_2_materials = " + str(day_2_materials))
    destiny_islands_lua_str = destiny_islands_lua_str.replace("homecoming_materials = 0", "homecoming_materials = " + str(homecoming_materials))
    return destiny_islands_lua_str


def write_destiny_islands_lua(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    if settings_data["destiny_islands"]:
        day_2_materials = settings_data["day_2_materials"]
        homecoming_materials = settings_data["homecoming_materials"]
        destiny_islands_lua_str = get_destiny_islands_lua_str()
        destiny_islands_lua_str = update_destiny_islands_lua_str(destiny_islands_lua_str, day_2_materials, homecoming_materials)
        output_destiny_islands_lua_file(destiny_islands_lua_str)


if __name__ == "__main__":
    write_destiny_islands_lua()