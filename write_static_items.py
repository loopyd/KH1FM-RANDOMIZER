from pathlib import Path
from typing import Dict, List

from config import ResourceType, read_data, write_data


def sort_evdl_location_data(evdl_locations: List[Dict]) -> Dict[str, List[Dict]]:
    sorted_evdl_location_data = {}
    for evdl_location in evdl_locations:
        if evdl_location["File"] not in sorted_evdl_location_data.keys():
            sorted_evdl_location_data[evdl_location["File"]] = []
        sorted_evdl_location_data[evdl_location["File"]].append(evdl_location)
    return sorted_evdl_location_data


def write_updated_evdl_files(sorted_evdl_location_data: Dict[str, List[Dict]], seed_json_data: Dict) -> None:
    for file in sorted_evdl_location_data.keys():
        print("Preparing " + file)
        corrected_file = sorted_evdl_location_data[file][0]["Use Corrected File?"]
        if corrected_file == "Y":
            evdl_bytes = read_data(kind=ResourceType.BIN, path_parts=("Corrected EVDLs", file), ask_prompt=False)
        else:
            evdl_bytes = read_data(kind=ResourceType.BIN, path_parts=("Working", file), ask_prompt=False)
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
        write_data(kind=ResourceType.BIN, data=evdl_bytes, path_parts=("Working", file), overwrite=True, create_parents=True)


def write_static_items(seed_json_file: Path | None = None) -> None:
    seed_json_data = read_data(kind=ResourceType.JSON, path=seed_json_file, ask_prompt=True)
    evdl_locations = read_data(kind=ResourceType.CSV, key="evdl_locations")
    sorted_evdl_location_data = sort_evdl_location_data(evdl_locations)
    write_updated_evdl_files(sorted_evdl_location_data, seed_json_data)


if __name__=="__main__":
    write_static_items()