from pathlib import Path
from typing import Dict, List

from helpers import root_path, read_json, read_csv, read_bytes, write_bytes

def get_evdl_locations() -> List[Dict]:
    static_items_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Static Items.csv")
    evdl_locations = read_csv(file_path=static_items_csv_path)
    return evdl_locations


def get_seed_json_data(seed_json_file: Path | None = None) -> Dict:
    seed_json_data = read_json(file_path=seed_json_file, ask_prompt=True)
    return seed_json_data


def get_evdl_bytes(file_path: Path) -> bytearray:
    evdl_bytes = read_bytes(file_path=file_path)
    return evdl_bytes


def sort_evdl_location_data(evdl_locations: List[Dict]) -> Dict[str, List[Dict]]:
    sorted_evdl_location_data = {}
    for evdl_location in evdl_locations:
        if evdl_location["File"] not in sorted_evdl_location_data.keys():
            sorted_evdl_location_data[evdl_location["File"]] = []
        sorted_evdl_location_data[evdl_location["File"]].append(evdl_location)
    return sorted_evdl_location_data


def write_evdl_bytes_to_file(evdl_file: Path, evdl_bytes: bytearray):
    file_path = root_path().joinpath("Working", evdl_file)
    write_bytes(file_path=file_path, data=evdl_bytes, overwrite=True, create_parents=True)
    

def write_updated_evdl_files(sorted_evdl_location_data: Dict[str, List[Dict]], seed_json_data: Dict, kh1_data_path: Path) -> None:
    for file in sorted_evdl_location_data.keys():
        print("Preparing " + file)
        corrected_file = sorted_evdl_location_data[file][0]["Use Corrected File?"]
        if corrected_file == "Y":
            file_path = root_path().joinpath("Corrected EVDLs", file)
        else:
            file_path = kh1_data_path.joinpath(file)
        evdl_bytes = get_evdl_bytes(file_path)
        for replacement in sorted_evdl_location_data[file]:
            print(replacement)
            print("Updating " + replacement["AP Location ID"] + " at offset " + replacement["Offset"])
            if replacement["AP Location ID"] in seed_json_data.keys():
                item_id = seed_json_data[replacement["AP Location ID"]] % 2640000
                if item_id > 1000 and item_id < 2000:
                    evdl_bytes[int(replacement["Offset"], 16)] = item_id % 1000
                    print("Writing item with value " + str(item_id % 1000))
                else:
                    evdl_bytes[int(replacement["Offset"], 16)] = 230
                    print("Writing generic AP Item")
            else:
                evdl_bytes[int(replacement["Offset"], 16)] = 1
                print("AP Location ID not found in replacement JSON, writing potion")
        write_evdl_bytes_to_file(file_path=file, evdl_bytes=evdl_bytes)


def write_static_items(seed_json_file: Path | None = None) -> None:
    kh1_data_path = root_path().joinpath("Working")
    seed_json_data = get_seed_json_data(seed_json_file)
    evdl_locations = get_evdl_locations()
    sorted_evdl_location_data = sort_evdl_location_data(evdl_locations)
    write_updated_evdl_files(sorted_evdl_location_data, seed_json_data, kh1_data_path)


if __name__=="__main__":
    write_static_items()