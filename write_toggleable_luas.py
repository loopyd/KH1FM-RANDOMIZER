from pathlib import Path

from helpers import boolify
from config import APVersion, ResourceType, get_ap_version, read_data, write_data

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


def write_toggleable_luas(settings_file: Path | None = None) -> None:
    settings_data = read_data(ResourceType.JSON, path=settings_file, ask_prompt=True)
    version = get_ap_version(settings_data)
    for key in lua_map[version].keys():
        if boolify(settings_data[key]):
            lua_str = read_data(kind=ResourceType.LUA, path_parts=("Template Luas", str(lua_map[version][key])))
            write_data(kind=ResourceType.LUA, data=lua_str, path_parts=("Working", "scripts", str(lua_map[version][key])), overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_toggleable_luas()