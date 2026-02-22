from pathlib import Path

from config import APVersion
from write_item_descriptions import build_item_description_string, build_item_description_string_array, concat_item_descriptions, build_item_description_bytes
from helpers import root_path, read_json, read_bytes, write_bytes, replace_value_at_index, read_plaintext, write_plaintext

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


def get_gummi_item_description_bytes(kh1_data_path: Path) -> bytearray:
    gummi_mes_data_path = kh1_data_path.joinpath("exchange", "UK_gumi_mes_data.bin")
    gummi_mes_bytes = read_bytes(file_path=gummi_mes_data_path)
    return gummi_mes_bytes


def get_gummi_item_description_offset_bytes(kh1_data_path: Path) -> bytearray:
    gummi_mes_ofs_path = kh1_data_path.joinpath("exchange", "UK_gumi_mes_ofs.bin")
    gummi_mes_ofs_bytes = read_bytes(file_path=gummi_mes_ofs_path)
    return gummi_mes_ofs_bytes


def output_gummi_item_descriptions(new_gummi_item_description_bytes: bytearray) -> None:
    gummi_mes_data_path = root_path().joinpath("Working", "exchange", "UK_gumi_mes_data.bin")
    write_bytes(file_path=gummi_mes_data_path, data=new_gummi_item_description_bytes, overwrite=True, create_parents=True)


def output_gummi_item_descriptions_offset_bytes(new_gummi_item_description_offset_bytes: bytearray) -> None:
    gummi_mes_ofs_path = root_path().joinpath("Working", "exchange", "UK_gumi_mes_ofs.bin")
    write_bytes(file_path=gummi_mes_ofs_path, data=new_gummi_item_description_offset_bytes, overwrite=True, create_parents=True)


def replace_specific_gummi_item_string(index: int, description: str) -> None:
    kh1_data_path = root_path().joinpath("Working")
    if description in TOO_LONG_DESCRIPTIONS.keys():
        description = TOO_LONG_DESCRIPTIONS[description]
    gummi_item_description_bytes = get_gummi_item_description_bytes(
        kh1_data_path)
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
    output_gummi_item_descriptions(bytes(new_gummi_item_description_bytes))


def get_gummi_items_lua() -> str:
    rando_gummi_items_lua_path = root_path().joinpath("Template Luas", "1fmRandoGummiItems.lua")
    gummi_items_lua_str = read_plaintext(file_path=rando_gummi_items_lua_path)
    return gummi_items_lua_str


def output_gummi_items_lua_file(gummi_items_lua_str: str) -> None:
    gummi_items_lua_path = root_path().joinpath("Working", "scripts", "1fmRandoGummiItems.lua")
    write_plaintext(file_path=gummi_items_lua_path, data=gummi_items_lua_str, overwrite=True, create_parents=True)


def write_gummi_items(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    kh1_data_path = root_path().joinpath("Working")
    settings_data = read_json(file_path=settings_file, ask_prompt=False)
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
    gummi_item_description_bytes = get_gummi_item_description_bytes(
        kh1_data_path)
    for i in range(len(gummi_item_description_bytes)):
        if gummi_item_description_bytes[i] == 0x00:
            offsets.append(i + 1)
    offsets = offsets[:-2]
    gummi_item_description_offset_bytes = get_gummi_item_description_offset_bytes(
        kh1_data_path)
    for i in range(len(offsets)):
        gummi_item_description_offset_bytes = replace_value_at_index(
            gummi_item_description_offset_bytes, i, offsets[i])
    output_gummi_item_descriptions_offset_bytes(
        gummi_item_description_offset_bytes)

    gummi_items_lua_str = get_gummi_items_lua()
    gummi_items_lua_str = gummi_items_lua_str.replace(
        "gummi_item_count = 0", f"gummi_item_count = {settings_num}")
    output_gummi_items_lua_file(gummi_items_lua_str)
    

# FIX: Forgot to call the function in main in the original code, so added that here.
if __name__ == "__main__":
    write_gummi_items()
