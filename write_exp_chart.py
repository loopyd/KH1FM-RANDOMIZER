from typing import Dict, List
from pathlib import Path

from config import APVersion
from helpers import read_json, root_path, read_csv, read_bytes, write_bytes


def get_exp_chart_definitions() -> List[Dict]:
    exp_chart_definitions_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - EXP Chart.csv")
    exp_chart_definitions = read_csv(file_path=exp_chart_definitions_csv_path)
    return exp_chart_definitions


def get_battle_table(kh1_data_path: Path) -> bytearray:
    battle_table_path = kh1_data_path.joinpath("btltbl.bin")
    battle_data = read_bytes(battle_table_path)
    return battle_data


def output_battle_table(battle_table_bytes: bytearray) -> None: 
    battle_table_path = root_path().joinpath("Working", "btltbl.bin")
    write_bytes(file_path=battle_table_path, data=battle_table_bytes, overwrite=True, create_parents=True)


def apply_exp_multiplier(battle_table_bytes: bytearray, settings_data: Dict, exp_chart_definitions: List[Dict]) -> bytearray:
    multiplier = settings_data["exp_multiplier"]
    for line in exp_chart_definitions:
        new_exp_to_add = max(int(int(line["EXP to Add"])//multiplier), 1)
        new_exp_to_add_bytes = new_exp_to_add.to_bytes(2, byteorder='little')
        battle_table_bytes[int(line["Offset"], 16)] = new_exp_to_add_bytes[0]
        battle_table_bytes[int(line["Offset"], 16) + 1] = new_exp_to_add_bytes[1]
    return battle_table_bytes

# FIX: Duplicate definition of output_battle_table removed.

def write_exp_chart(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    kh1_data_path = root_path().joinpath("Working")
    exp_chart_definitions = get_exp_chart_definitions()
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    battle_table_bytes = get_battle_table(kh1_data_path)
    battle_table_bytes = apply_exp_multiplier(battle_table_bytes, settings_data, exp_chart_definitions)
    output_battle_table(battle_table_bytes)


if __name__ == "__main__":
    write_exp_chart()