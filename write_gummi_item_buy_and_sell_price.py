from pathlib import Path

from config import ResourceType, read_data, write_data


def get_gumi_spec_file(kh1_data_path: Path) -> bytearray:
    return 

def write_gummi_item_buy_and_sell_price() -> None:
    gumi_spec_file = read_data(kind=ResourceType.BIN, key="gumi_spec_file")
    gummi_block_prices = read_data(kind=ResourceType.CSV, key="gummi_block_prices")
    for gummi_block_price in gummi_block_prices:
        offset = int(gummi_block_price["Offset"], 16)
        gumi_spec_file[offset] = 0
    write_data(kind=ResourceType.BIN, data=gumi_spec_file, key="gumi_spec_file", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_gummi_item_buy_and_sell_price()