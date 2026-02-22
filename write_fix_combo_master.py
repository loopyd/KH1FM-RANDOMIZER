from pathlib import Path

from config import ResourceType, read_data, write_data


def update_fix_combo_master_template_lua(fix_combo_master_lua_str: str, seed_json_data: dict) -> str:
    if "2658150" in seed_json_data.keys():
        if seed_json_data["2658150"] > 2643000 and seed_json_data["2658150"] < 2644000:
            fix_combo_master_lua_str = fix_combo_master_lua_str.replace("level_50_overwrite_value = 0x0", "level_50_overwrite_value = " + str(hex(seed_json_data["2658150"] % 2643000 + 0x80)))
    if "2658155" in seed_json_data.keys():
        if seed_json_data["2658155"] > 2643000 and seed_json_data["2658155"] < 2644000:
            fix_combo_master_lua_str = fix_combo_master_lua_str.replace("level_55_overwrite_value = 0x0", "level_55_overwrite_value = " + str(hex(seed_json_data["2658155"] % 2643000 + 0x80)))
    return fix_combo_master_lua_str


def write_fix_combo_master(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    fix_combo_master_lua_str = read_data(kind=ResourceType.LUA, key="template_fix_combo_master")
    fix_combo_master_lua_str = update_fix_combo_master_template_lua(fix_combo_master_lua_str, seed_json_data)
    write_data(kind=ResourceType.LUA, data=fix_combo_master_lua_str, key="output_fix_combo_master", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_fix_combo_master()