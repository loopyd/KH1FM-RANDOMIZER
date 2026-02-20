from pathlib import Path
from typing import List

from helpers import root_path, read_json, read_plaintext, write_plaintext


def get_ap_cost_template_lua():
    file_path = root_path().joinpath("Template Luas", "1fmRandoAPCosts.lua")
    ap_costs_lua_str = read_plaintext(file_path=file_path)
    return ap_costs_lua_str


def output_ap_cost_template_lua(ap_costs_lua_str: str):
    file_path = root_path().joinpath("Working", "scripts", "1fmRandoAPCosts.lua")
    write_plaintext(file_path=file_path, data=ap_costs_lua_str, overwrite=True, create_parents=True)


def update_ap_costs_template_lua(ap_cost_data: List, ap_costs_lua_str: str) -> str:
    costs_string = ""
    for ap_cost in ap_cost_data:
        costs_string = costs_string + str(ap_cost["AP Cost"]) + ","
    costs_string = costs_string[:-1]
    ap_costs_lua_str = ap_costs_lua_str.replace("ability_costs = {}", "ability_costs = {" + costs_string + "}")
    return ap_costs_lua_str


def write_ap_cost_lua(settings_file: Path | None = None, ap_cost_file: Path | None = None):
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
    if settings_data["randomize_ap_costs"] != "off":
        ap_cost_data = read_json(file_path=ap_cost_file, ask_prompt=False)
        ap_costs_lua_str = get_ap_cost_template_lua()
        ap_costs_lua_str = update_ap_costs_template_lua(ap_cost_data, ap_costs_lua_str)
        output_ap_cost_template_lua(ap_costs_lua_str)


if __name__ == "__main__":
    write_ap_cost_lua()