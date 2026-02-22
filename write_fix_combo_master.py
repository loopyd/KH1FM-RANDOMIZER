
from pathlib import Path

from config import APVersion
from helpers import read_json, root_path, read_plaintext, write_plaintext


def get_fix_combo_master_template_lua() -> str:
    rando_combo_master_lua_path = root_path().joinpath("Template Luas", "1fmRandoFixComboMaster.lua")
    fix_combo_master_lua_str = read_plaintext(file_path=rando_combo_master_lua_path)
    return fix_combo_master_lua_str


def update_fix_combo_master_template_lua(fix_combo_master_lua_str: str, seed_json_data: dict) -> str:
    if "2658150" in seed_json_data.keys():
        if seed_json_data["2658150"] > 2643000 and seed_json_data["2658150"] < 2644000:
            fix_combo_master_lua_str = fix_combo_master_lua_str.replace("level_50_overwrite_value = 0x0", "level_50_overwrite_value = " + str(hex(seed_json_data["2658150"] % 2643000 + 0x80)))
    if "2658155" in seed_json_data.keys():
        if seed_json_data["2658155"] > 2643000 and seed_json_data["2658155"] < 2644000:
            fix_combo_master_lua_str = fix_combo_master_lua_str.replace("level_55_overwrite_value = 0x0", "level_55_overwrite_value = " + str(hex(seed_json_data["2658155"] % 2643000 + 0x80)))
    return fix_combo_master_lua_str


def output_fix_combo_master_lua_file(fix_combo_master_lua_str: str) -> None:
    output_file_path = root_path().joinpath("Working", "scripts", "1fmRandoFixComboMaster.lua")
    write_plaintext(file_path=output_file_path, data=fix_combo_master_lua_str, overwrite=True, create_parents=True)


def write_fix_combo_master(seed_json_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=False)
    fix_combo_master_lua_str = get_fix_combo_master_template_lua()
    fix_combo_master_lua_str = update_fix_combo_master_template_lua(fix_combo_master_lua_str, seed_json_data)
    output_fix_combo_master_lua_file(fix_combo_master_lua_str)


if __name__ == "__main__":
    write_fix_combo_master()