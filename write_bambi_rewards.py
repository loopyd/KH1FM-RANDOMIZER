from typing import Dict, List

from config import ResourceType, read_data, write_data
from definitions import filler_item_ids


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


def write_bambi_rewards() -> None:
    bambi_definitions = read_data(kind=ResourceType.CSV, key="bambi_definitions")
    bambi_bytes =  read_data(kind=ResourceType.BIN, key="bambi_mdls")
    bambi_bytes = remove_bambi_synth_drops(bambi_bytes, bambi_definitions)
    write_data(kind=ResourceType.BIN, data=bambi_bytes, key="bambi_mdls", overwrite=True, create_parents=True)


if __name__=="__main__":
    write_bambi_rewards()