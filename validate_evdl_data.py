from pathlib import Path

from config import read_data, ResourceType
from helpers import get_folder


def validate_evdl_data(kh1_data_path: Path | None = None) -> None:
    kh1_data_path = get_folder(folder_path=kh1_data_path, label="KH1 Data Path", ask_prompt=True)
    error = False
    corrected_evdl_data = read_data(kind=ResourceType.CSV, key="evdl_locations")
    static_item_dict = {}
    use_corrected_evdl_dict = {}
    for file_location in corrected_evdl_data:
        key = file_location["World"] + " " + file_location["Location"] + " " + file_location["Action"] + " " + file_location["Item"] + " " + file_location["Number"]
        if key not in static_item_dict.keys():
            static_item_dict[key] = []
        static_item_dict[key].append({"File": file_location["File"], "Offset": file_location["Offset"], "Use Corrected File?": file_location["Use Corrected File?"]})
    for item in static_item_dict.keys():
        bytes = []
        for file_location in static_item_dict[item]:
            if file_location["Use Corrected File?"] == "N":
                file_path = kh1_data_path.joinpath(file_location["File"])
                try:
                    data = read_data(kind=ResourceType.BIN, path=file_path, ask_prompt=False)
                except FileNotFoundError:
                    print("Error, " + file_location["File"] + " not found in KH1 data path. Check the file name and try again.")
                    error = True
                    continue
                offset = int(file_location["Offset"],16)
                bytes.append(hex(data[offset]))
            else:
                try:
                    data = read_data(kind=ResourceType.BIN, path_parts=("Corrected EVDLs", file_location["File"]), ask_prompt=False)
                except FileNotFoundError:
                    print("Error, " + file_location["File"] + " not found in Corrected EVDLs folder. Check the file name and try again.")
                    error = True
                    continue
                offset = int(file_location["Offset"],16)
                bytes.append(hex(data[offset]))
        if bytes.count(bytes[0]) != len(bytes):
            print("ERROR! Check " + item + " again!")
            print(bytes)
            error = True
    for file_location in corrected_evdl_data:
        if file_location["File"] not in use_corrected_evdl_dict.keys():
            use_corrected_evdl_dict[file_location["File"]] = file_location["Use Corrected File?"]
        elif use_corrected_evdl_dict[file_location["File"]] != file_location["Use Corrected File?"]:
            print("ERROR! Check " + file_location["File"] + " again!  Multiple Use Corrected File? values found")
            error = True
    if not error:
        print("All checks completed successfully!")

if __name__=="__main__":
    validate_evdl_data()