from pathlib import Path
from typing import List

from config import ResourceType, read_data, write_data
from helpers import boolify


def update_ap_costs_template_lua(ap_cost_data: List, ap_costs_lua_str: str) -> str:
    costs_string = ""
    for ap_cost in ap_cost_data:
        costs_string = costs_string + str(ap_cost["AP Cost"]) + ","
    costs_string = costs_string[:-1]
    ap_costs_lua_str = ap_costs_lua_str.replace("ability_costs = {}", "ability_costs = {" + costs_string + "}")
    return ap_costs_lua_str


def write_ap_cost_lua(settings_file: Path | None = None, ap_cost_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("randomize_ap_costs", False)):
        ap_cost_data = read_data(kind=ResourceType.JSON, path=ap_cost_file, ask_prompt=True)
        ap_costs_lua_str = read_data(kind=ResourceType.LUA, key="template_ap_cost")
        ap_costs_lua_str = update_ap_costs_template_lua(ap_cost_data, ap_costs_lua_str)
        write_data(kind=ResourceType.LUA, data=ap_costs_lua_str, key="output_ap_cost", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_ap_cost_lua()