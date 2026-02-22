from pathlib import Path

from config import APVersion, get_ap_version
from helpers import root_path, read_json, read_plaintext, write_plaintext

lua_map = {
    APVersion.AP_MAIN: {
        "shorten_go_mode": "1fmRandoShortenGoMode.lua",
        "one_hp": "1fm1HP.lua",
        "four_by_three": "1fm4By3.lua",
        "beep_hack": "1fmBeepHack.lua",
        "consistent_finishers": "1fmConsistentFinishers.lua",
        "early_skip": "1fmEarlySkip.lua",
        "fast_camera": "1fmFastCamera.lua",
        "faster_animations": "1fmFasterAnims.lua",
        "unlock_0_volume": "1fmUnlock0Volume.lua",
        "unskippable": "1fmUnskippable.lua",
        "auto_save": "1fmRandoAutoSave.lua",
        "warp_anywhere": "1fmRandoWarpAnywhere.lua"
    },
    APVersion.AP_DEV: {
        "shorten_go_mode": "1fmRandoShortenGoMode.lua",
        "one_hp": "1fm1HP.lua",
        "four_by_three": "1fm4By3.lua",
        "beep_hack": "1fmBeepHack.lua",
        "consistent_finishers": "1fmConsistentFinishers.lua",
        "early_skip": "1fmEarlySkip.lua",
        "fast_camera": "1fmFastCamera.lua",
        "faster_animations": "1fmFasterAnims.lua",
        "unlock_0_volume": "1fmUnlock0Volume.lua",
        "unskippable": "1fmUnskippable.lua",
        "auto_save": "1fmRandoAutoSave.lua",
        "warp_anywhere": "1fmRandoWarpAnywhere.lua"
    },
}


def get_lua_str(lua_file_name: Path) -> str:
    lua_path = root_path().joinpath("Template Luas", lua_file_name)
    lua_str = read_plaintext(file_path=lua_path)
    return lua_str


def output_lua_file(lua_str: str, lua_file_name: Path) -> None:
    lua_path = root_path().joinpath("Working", "scripts", lua_file_name)
    write_plaintext(file_path=lua_path, data=lua_str, overwrite=True, create_parents=True)


def write_toggleable_luas(settings_file: Path | None = None) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    version = get_ap_version(settings_data)
    for key in lua_map[version].keys():
        if settings_data[key]:
            lua_str = get_lua_str(lua_map[version][key])
            output_lua_file(lua_str, lua_map[version][key])


if __name__ == "__main__":
    write_toggleable_luas()