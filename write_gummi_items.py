from pathlib import Path

from config import ResourceType, read_data, write_data
from write_item_descriptions import build_item_description_string, build_item_description_string_array, concat_item_descriptions, build_item_description_bytes
from helpers import replace_value_at_index

SETTINGS_EXCLUSIONS = [
    "starting_items", "synthesis_item_name_byte_arrays", "remote_location_ids", "slot_name"]
SENTINEL = b"\xCD" * 10
AP_ITEM_GUMMI_INDEXES = [0x77, 0x78, 0x79, 0x7A]
START_INVENTORY_WRITTEN_INDEX = 0x7B
GUMMI_ITEMS_WRITTEN_INDEX = 0x7C
TOO_LONG_DESCRIPTIONS = {
    "Accessory Augments": "Acc Augments",
    "Bad Starting Weapons": "Bad Starting Wpns",
    "Consistent Finishers": "Consistent Fnshrs",
    "End Of The World Unlock": "EOTW Unlock",
    "Extra Shared Abilities": "Extra Shared Ablts",
    "Final Rest Door Key": "FR Door Key",
    "Force Stats On Levels": "Force Stats on LVs",
    "Halloween Town Key Item Bundle": "HT Key Item Bundle",
    "Homecoming Materials": "Homecomings Mats",
    "Individual Spell Level Costs": "Ind Spell LV Costs",
    "Keyblades Unlock Chests": "Keyblade Locking",
    "Randomize Ap Costs": "Random AP Costs",
    "Randomize Emblem Pieces": "Random E. Pieces",
    "Randomize Heartless": "Random Heartless",
    "Randomize Party Member Starting Accessories": "Random Start Accs",
    "Randomize Postcards": "Random Postcards",
    "Randomize Spell Mp Costs": "Random Spell MP",
    "Required Lucky Emblems Door": "Rqrd Embs Door",
    "Required Lucky Emblems Eotw": "Rqrd Embs EOTW",
    "Required Postcards": "Rqrd Postcards",
    "Scaling Spell Potency": "Scaling Spells",
    "Stacking World Items": "Stacking Worlds"}


def replace_specific_gummi_item_string(index: int, description: str) -> None:
    if description in TOO_LONG_DESCRIPTIONS.keys():
        description = TOO_LONG_DESCRIPTIONS[description]
    gummi_item_description_bytes = read_data(kind=ResourceType.BIN, key="gummi_item_descriptions")

    gummi_item_description_string = build_item_description_string(
        gummi_item_description_bytes)
    gummi_item_descriptions = build_item_description_string_array(
        gummi_item_description_string)
    gummi_item_descriptions[index] = description
    new_gummi_item_description_string = concat_item_descriptions(
        gummi_item_descriptions)
    new_gummi_item_description_bytes = build_item_description_bytes(
        new_gummi_item_description_string)
    for byte in new_gummi_item_description_bytes:
        if byte is None:
            print("Something went wrong!!!")
    write_data(kind=ResourceType.BIN, data=bytes(new_gummi_item_description_bytes), key="gummi_item_descriptions", overwrite=True, create_parents=True)


def write_gummi_items(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=False)
    settings_num = 0

    # Handle Text
    for setting in settings_data.keys():
        print(f"Working on setting {setting}...")
        if setting not in SETTINGS_EXCLUSIONS:
            setting_name = setting.upper().replace("_", " ").title()
            setting_description = str(
                settings_data[setting]).replace("_", " ").title()
            print(
                f"Setting {setting} not in exclusions!  New name is {setting_name} and description is {setting_description}...")
            replace_specific_gummi_item_string(settings_num, setting_name)
            replace_specific_gummi_item_string(
                settings_num + 160, setting_description)
            settings_num = settings_num + 1
    for index in AP_ITEM_GUMMI_INDEXES:
        replace_specific_gummi_item_string(index,       "AP Items Received")
        replace_specific_gummi_item_string(index + 160, "")
    replace_specific_gummi_item_string(
        START_INVENTORY_WRITTEN_INDEX, "Start Written")
    replace_specific_gummi_item_string(START_INVENTORY_WRITTEN_INDEX + 160, "")
    replace_specific_gummi_item_string(
        GUMMI_ITEMS_WRITTEN_INDEX, "Gummi Written")
    replace_specific_gummi_item_string(GUMMI_ITEMS_WRITTEN_INDEX + 160, "")

    # Handle Offsets
    offsets = [0]
    gummi_item_description_bytes = read_data(kind=ResourceType.BIN, key="gummi_item_descriptions")
    for i in range(len(gummi_item_description_bytes)):
        if gummi_item_description_bytes[i] == 0x00:
            offsets.append(i + 1)
    offsets = offsets[:-2]
    gummi_item_description_offset_bytes = read_data(kind=ResourceType.BIN, key="gummi_item_descriptions_offsets")
    for i in range(len(offsets)):
        gummi_item_description_offset_bytes = replace_value_at_index(
            gummi_item_description_offset_bytes, i, offsets[i])
    write_data(kind=ResourceType.BIN,
        data=gummi_item_description_offset_bytes,
        key="gummi_item_descriptions_offsets",
        overwrite=True,
        create_parents=True,
    )

    gummi_items_lua_str = read_data(kind=ResourceType.LUA, key="template_gummi_items")
    gummi_items_lua_str = gummi_items_lua_str.replace(
        "gummi_item_count = 0", f"gummi_item_count = {settings_num}")
    write_data(kind=ResourceType.LUA, data=gummi_items_lua_str, key="output_gummi_items", overwrite=True, create_parents=True)
    

# FIX: Forgot to call the function in main in the original code, so added that here.
if __name__ == "__main__":
    write_gummi_items()
