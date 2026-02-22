from typing import Dict, List
from pathlib import Path

from helpers import root_path, read_bytes, write_bytes, read_csv


def get_gumi_spec_file(kh1_data_path: Path) -> bytearray:
    gummi_spec_file_path = kh1_data_path.joinpath("gumi_spec_file.bin")
    gummi_spec_bytes=read_bytes(file_path=gummi_spec_file_path)
    return gummi_spec_bytes


def get_gummi_block_prices() -> List[Dict]:
    gummi_block_prizes_csv_path = root_path().joinpath("Documentation", "KH1FM Documentation - Gummi Block Prices.csv")
    gummi_block_prices_definitions = read_csv(file_path=gummi_block_prizes_csv_path)
    return gummi_block_prices_definitions
    

def output_gumi_spec_file(gummi_spec_file_bytes: bytearray) -> None:
    gummi_spec_path = root_path().joinpath("Working", "gumi_spec_file.bin")
    write_bytes(file_path=gummi_spec_path, data=gummi_spec_file_bytes, overwrite=True, create_parents=True)
    

def write_gummi_item_buy_and_sell_price() -> None:
    kh1_data_path = root_path().joinpath("Working")
    gumi_spec_file = get_gumi_spec_file(kh1_data_path)
    gummi_block_prices = get_gummi_block_prices()
    for gummi_block_price in gummi_block_prices:
        offset = int(gummi_block_price["Offset"], 16)
        gumi_spec_file[offset] = 0
    output_gumi_spec_file(gumi_spec_file)


if __name__ == "__main__":
    write_gummi_item_buy_and_sell_price()