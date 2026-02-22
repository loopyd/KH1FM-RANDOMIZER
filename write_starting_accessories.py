from pathlib import Path
from typing import Dict, List

from config import APVersion
from helpers import root_path, read_json, read_csv, read_bytes, write_bytes


def get_starting_accessory_equipped_defintions() -> List[Dict]:
    party_member_starting_accessories_equipped_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Party Member Starting Accessories Equipped.csv")
    evdl_locations = read_csv(file_path=party_member_starting_accessories_equipped_csv_path)
    return evdl_locations


def get_starting_accessory_stock_defintions() -> List[Dict]:
    party_member_starting_accessories_stock_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Party Member Starting Accessories Stock.csv")
    evdl_locations = read_csv(file_path=party_member_starting_accessories_stock_csv_path)
    return evdl_locations


def get_evdl_bytes(file_path: Path) -> bytearray:
    evdl_bytes = read_bytes(file_path=file_path)
    return evdl_bytes


def write_evdl_bytes_to_file(file_path: Path, evdl_bytes: bytearray) -> None:
    output_path = root_path().joinpath("Working", file_path)
    write_bytes(file_path=output_path, data=evdl_bytes, overwrite=True, create_parents=True)


def write_starting_accessories_equipped(seed_json_file: Path | None = None, settings_file: Path | None = None):
    kh1_data_path = root_path().joinpath("Working")
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    if settings_data["randomize_party_member_starting_accessories"]:
        evdl_location = kh1_data_path.joinpath("remastered", "dh01.ard", "UK_dh01c.ev")
        evdl_bytes = get_evdl_bytes(evdl_location)
        starting_accessory_equipped_definitions = get_starting_accessory_equipped_defintions()
        seed_json_data = read_json(file_path=seed_json_file, ask_prompt=True)
        starting_accessory_location_id_character_map = {
            "2656800": 1,
            "2656801": 1,
            "2656802": 2,
            "2656803": 2,
            "2656804": 3,
            "2656805": 5,
            "2656806": 5,
            "2656807": 6,
            "2656808": 6,
            "2656809": 6,
            "2656810": 7,
            "2656811": 7,
            "2656812": 8,
            "2656813": 8,
            "2656814": 9}
        accessories_placed = 0
        for key in starting_accessory_location_id_character_map.keys():
            if accessories_placed < 10:
                if key in seed_json_data.keys():
                    accessory_to_place = seed_json_data[key] % 2641000
                    if accessory_to_place < 17 or accessory_to_place > 71:
                        print("Invalid accessory placed at key " + str(key) + ": " + str(accessory_to_place))
                        exit(1)
                    location_to_place = starting_accessory_equipped_definitions[accessories_placed]
                    offset = int(location_to_place["Offset"], 16)
                    evdl_bytes[offset] = starting_accessory_location_id_character_map[key]
                    evdl_bytes[offset + 4] = accessory_to_place
                    accessories_placed = accessories_placed + 1
        if accessories_placed < 10:
            print("Got less than 10 accessories to place!  Placed: " + str(accessories_placed))
            exit(1)
        write_evdl_bytes_to_file(Path("remastered") / "dh01.ard" / "UK_dh01c.ev", evdl_bytes)


def write_starting_accessories_stock(seed_json_file: Path | None = None, settings_file: Path | None = None):
    kh1_data_path = root_path().joinpath("Working")
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    if settings_data["randomize_party_member_starting_accessories"]:
        evdl_location = kh1_data_path.joinpath("remastered", "dh01.ard", "UK_dh01c.ev")
        evdl_bytes = get_evdl_bytes(evdl_location)
        starting_accessory_stock_definitions = get_starting_accessory_stock_defintions()
        seed_json_data = read_json(file_path=seed_json_file, ask_prompt=True)
        starting_accessory_location_ids = [
            "2656800",
            "2656801",
            "2656802",
            "2656803",
            "2656804",
            "2656805",
            "2656806",
            "2656807",
            "2656808",
            "2656809",
            "2656810",
            "2656811",
            "2656812",
            "2656813",
            "2656814"]
        accessories_placed = 0
        for key in starting_accessory_location_ids:
            if accessories_placed < 10:
                if key in seed_json_data.keys():
                    accessory_to_place = seed_json_data[key] % 2641000
                    if accessory_to_place < 17 or accessory_to_place > 71:
                        print("Invalid accessory placed at key " + str(key) + ": " + str(accessory_to_place))
                        exit(1)
                    location_to_place = starting_accessory_stock_definitions[accessories_placed]
                    offset = int(location_to_place["Offset"], 16)
                    evdl_bytes[offset] = accessory_to_place
                    accessories_placed = accessories_placed + 1
        if accessories_placed < 10:
            print("Got less than 10 accessories to place!  Placed: " + str(accessories_placed))
            exit(1)
        write_evdl_bytes_to_file(Path("remastered") / "dh01.ard" / "UK_dh01c.ev", evdl_bytes)


def write_starting_accessories(seed_json_file: Path | None = None, settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV):
    write_starting_accessories_equipped(seed_json_file, settings_file)
    write_starting_accessories_stock(seed_json_file, settings_file)


if __name__=="__main__":
    write_starting_accessories()