from pathlib import Path
from typing import Dict, List

from definitions import filler_item_ids
from helpers import root_path, read_csv, read_bytes, write_bytes


def get_bambi_definitions() -> List[Dict]:
    bambi_drops_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Bambi Drops.csv")
    bambi_definitions = read_csv(file_path=bambi_drops_csv_path)
    return bambi_definitions


def get_bambi_data(kh1_data_path: Path) -> bytearray:
    bambi_data_path = kh1_data_path.joinpath("xa_ex_4030.mdls")
    bambi_data_bytes = read_bytes(bambi_data_path)
    return bambi_data_bytes


def remove_bambi_synth_drops(bambi_bytes: bytearray, bambi_definitions: List[Dict]) -> bytearray:
    for bambi_definition in bambi_definitions:
        if bambi_definition["Notes"].startswith("Drop"):
            if int(bambi_definition["Value"]) not in filler_item_ids:
                offset = int(bambi_definition["Offset"], 16)
                bambi_bytes[offset-4] = 0
                bambi_bytes[offset-3] = 0
                bambi_bytes[offset-2] = 0
                bambi_bytes[offset-1] = 0
                bambi_bytes[offset] = 0
                bambi_bytes[offset+1] = 0
                bambi_bytes[offset+2] = 0
                bambi_bytes[offset+3] = 0
    return bambi_bytes


def write_bambi_mdls(bambi_bytes: bytearray) -> None:
    bambi_data_path = root_path().joinpath("Working", "xa_ex_4030.mdls")
    write_bytes(file_path=bambi_data_path, data=bambi_bytes, overwrite=True, create_parents=True)


def write_bambi_rewards() -> None:
    kh1_data_path = root_path().joinpath("Working")
    bambi_definitions = get_bambi_definitions()
    bambi_bytes = get_bambi_data(kh1_data_path)
    bambi_bytes = remove_bambi_synth_drops(bambi_bytes, bambi_definitions)
    write_bambi_mdls(bambi_bytes)

if __name__=="__main__":
    write_bambi_rewards()