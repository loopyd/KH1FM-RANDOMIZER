from typing import Dict, List
from pathlib import Path

from config import ResourceType, read_data, write_data


def apply_exp_multiplier(battle_table_bytes: bytearray, settings_data: Dict, exp_chart_definitions: List[Dict]) -> bytearray:
    multiplier = settings_data["exp_multiplier"]
    for line in exp_chart_definitions:
        new_exp_to_add = max(int(int(line["EXP to Add"])//multiplier), 1)
        new_exp_to_add_bytes = new_exp_to_add.to_bytes(2, byteorder='little')
        battle_table_bytes[int(line["Offset"], 16)] = new_exp_to_add_bytes[0]
        battle_table_bytes[int(line["Offset"], 16) + 1] = new_exp_to_add_bytes[1]
    return battle_table_bytes


def write_exp_chart(settings_file: Path | None = None) -> None:
    exp_chart_definitions = read_data(kind=ResourceType.CSV, key="exp_chart_definitions")
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=False)
    battle_table_bytes = read_data(kind=ResourceType.BIN, key="battle_table")
    battle_table_bytes = apply_exp_multiplier(battle_table_bytes, settings_data, exp_chart_definitions)
    write_data(kind=ResourceType.BIN, data=battle_table_bytes, key="battle_table", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_exp_chart()