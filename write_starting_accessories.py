from pathlib import Path

from helpers import boolify
from config import ResourceType, read_data, write_data


def write_starting_accessories_equipped(seed_json_file: Path | None = None, settings_file: Path | None = None):
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("randomize_party_member_starting_accessories", False)):
        evdl_bytes = read_data(kind=ResourceType.BIN, key="starting_accessory_equipped_evdl")
        starting_accessory_equipped_definitions = read_data(kind=ResourceType.CSV, key="starting_accessory_equipped_definitions")
        seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
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
            print(f"Got less than 10 accessories to place!  Placed: {accessories_placed}")
            exit(1)
        write_data(kind=ResourceType.BIN, data=evdl_bytes, key="starting_accessory_equipped_evdl", overwrite=True, create_parents=True)


def write_starting_accessories_stock(seed_json_file: Path | None = None, settings_file: Path | None = None):
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    if boolify(settings_data.get("randomize_party_member_starting_accessories", False)) and settings_data.get("starting_accessory_stock_count", 0) > 0:
        evdl_bytes = read_data(kind=ResourceType.BIN, key="starting_accessory_stock_evdl")
        starting_accessory_stock_definitions = read_data(kind=ResourceType.CSV, key="starting_accessory_stock_definitions")
        seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
        starting_accessory_stock_count = settings_data.get("starting_accessory_stock_count", 0)
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
            if accessories_placed < starting_accessory_stock_count:
                if key in seed_json_data.keys():
                    accessory_to_place = seed_json_data[key] % 2641000
                    if accessory_to_place < 17 or accessory_to_place > 71:
                        print("Invalid accessory placed at key " + str(key) + ": " + str(accessory_to_place))
                        exit(1)
                    location_to_place = starting_accessory_stock_definitions[accessories_placed]
                    offset = int(location_to_place["Offset"], 16)
                    evdl_bytes[offset] = accessory_to_place
                    accessories_placed = accessories_placed + 1
        if accessories_placed < starting_accessory_stock_count:
            print(f"Got less than {starting_accessory_stock_count} accessories to place!  Placed: {accessories_placed}")
            exit(1)
        write_data(kind=ResourceType.BIN, data=evdl_bytes, key="starting_accessory_stock_evdl", overwrite=True, create_parents=True)


def write_starting_accessories(seed_json_file: Path | None = None, settings_file: Path | None = None):
    write_starting_accessories_equipped(seed_json_file, settings_file)
    write_starting_accessories_stock(seed_json_file, settings_file)


if __name__=="__main__":
    write_starting_accessories()