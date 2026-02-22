from pathlib import Path

from config import ResourceType, read_data, write_data
from definitions import augment_strings
from write_item_descriptions import replace_specific_item_description
from helpers import boolify


def update_augment_lua(augments_lua_string: str, seed_json_data: dict) -> str:
    accessory_location_map = {k: v for k, v in seed_json_data.items() if 2659100 <= int(k) <= 2659154}
    for accessory_location_id in accessory_location_map.keys():
        acc_val = int(accessory_location_id) - 2659100 + 17
        aug_val = accessory_location_map[accessory_location_id]
        aug_str = augment_strings[aug_val][0]
        augments_lua_string = augments_lua_string.replace(aug_str + " = 256", aug_str + " = " + str(acc_val))
    return augments_lua_string


def update_accessory_descriptions(seed_json_data: dict) -> None:
    accessory_location_map = {k: v for k, v in seed_json_data.items() if 2659100 <= int(k) <= 2659154}
    for accessory_location_id in accessory_location_map.keys():
        acc_val = int(accessory_location_id) - 2659100 + 17
        aug_val = accessory_location_map[accessory_location_id]
        aug_description = augment_strings[aug_val][1]
        replace_specific_item_description(acc_val, aug_description)


def update_augment_mp_costs(augments_lua_string: str, mp_costs: list) -> str:
    cost_to_num_dict = {
        15:  1,
        30:  2,
        100: 3,
        200: 4,
        300: 5
    }
    search_string = "magic_costs = {2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4}"
    replacement_string = "magic_costs = {" + ",".join(str(cost_to_num_dict[x]) for x in mp_costs) + "}"
    augments_lua_string = augments_lua_string.replace(search_string, replacement_string)
    return augments_lua_string


def update_augment_spell_effectiveness(augments_lua_string: str, mp_costs: list) -> str:
    search_string = "effectiveness_values = {20,28,36,22,27,34,16,20,26,15,27,36,40,55,70,2,2,2,18,18,18}"
    spell_effectiveness = get_new_spell_effectiveness(mp_costs)
    replacement_string = "effectiveness_values = {" + ",".join(str(x) for x in spell_effectiveness) + "}"
    augments_lua_string = augments_lua_string.replace(search_string, replacement_string)
    return augments_lua_string


def get_new_spell_effectiveness(spell_mp_costs_data):
    original_spell_costs = [
        30, 30, 30,
        30, 30, 30,
        100, 100, 100,
        100, 100, 100,
        100, 100, 100,
        200, 200, 200,
        200, 200, 200]
    spell_effectiveness = [
        20,28,36,
        22,27,34,
        16,20,26,
        15,27,36,
        40,55,70,
        2,2,2,
        18,18,18]
    for i in range(len(spell_effectiveness)):
        current_effectiveness = spell_effectiveness[i]
        spell_effectiveness[i] = max([round(current_effectiveness * (spell_mp_costs_data[i] / original_spell_costs[i])), 1])
    return spell_effectiveness


def write_augments(seed_json_file: Path | None = None, settings_file: Path | None = None, mp_cost_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("accessory_augments")):
        augments_lua_string = read_data(kind=ResourceType.LUA, key="template_augments")
        if boolify(settings_data.get("randomize_spell_mp_costs", False)):
            mp_costs = read_data(kind=ResourceType.JSON, path=mp_cost_file, ask_prompt=True)
            augments_lua_string = update_augment_mp_costs(augments_lua_string, mp_costs)
            if boolify(settings_data.get("scaling_spell_potency", False)):
                augments_lua_string = update_augment_spell_effectiveness(augments_lua_string, mp_costs)
        seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
        augments_lua_string = update_augment_lua(augments_lua_string, seed_json_data)
        write_data(kind=ResourceType.LUA, data=augments_lua_string, key="output_augments", overwrite=True, create_parents=True)
        update_accessory_descriptions(seed_json_data)

if __name__=="__main__":
    write_augments()