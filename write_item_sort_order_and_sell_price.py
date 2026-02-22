from typing import Dict
from pathlib import Path

from config import ResourceType, read_data, write_data
from definitions import sort_order, filler_item_ids


#def write_item_csv():
#    kh1_data_path = "./Working/"
#    battle_table_bytes = get_battle_table(kh1_data_path)
#    per_item_bytes = 20
#    items = 255
#    start_index = 0x1A58
#    end_index = start_index + (per_item_bytes * items)
#    item_bytes = battle_table_bytes[start_index:end_index]
#    i = 0
#    j = 0
#    btl_tbl_item_values = []
#    while i < len(item_bytes):
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i:i+2]),
#            "Value": bytes_to_int(item_bytes[i:i+2]),
#            "Notes": "Item Name"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+2),
#            "Value (HEX)": convert_byte_array_to_string([item_bytes[i+2]]),
#            "Value": bytes_to_int([item_bytes[i+2]]),
#            "Notes": "Item Icon"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+3),
#            "Value (HEX)": convert_byte_array_to_string([item_bytes[i+3]]),
#            "Value": bytes_to_int([item_bytes[i+3]]),
#            "Notes": "???"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+4),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+4:i+6]),
#            "Value": bytes_to_int(item_bytes[i+4:i+6]),
#            "Notes": "???"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+6),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+6:i+8]),
#            "Value": bytes_to_int(item_bytes[i+6:i+8]),
#            "Notes": "???"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+8),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+8:i+10]),
#            "Value": bytes_to_int(item_bytes[i+8:i+10]),
#            "Notes": "Buy Price"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+10),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+10:i+12]),
#            "Value": bytes_to_int(item_bytes[i+10:i+12]),
#            "Notes": "Sell Price"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+12),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+12:i+14]),
#            "Value": bytes_to_int(item_bytes[i+12:i+14]),
#            "Notes": "???"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+14),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+14:i+16]),
#            "Value": bytes_to_int(item_bytes[i+14:i+16]),
#            "Notes": "???"
#            })
#        btl_tbl_item_values.append({
#            "Item Index": j + 1,
#            "Item Name": item_list[j],
#            "File": "btltbl.bin",
#            "Offset": to_hex_no_0x(start_index + i+16),
#            "Value (HEX)": convert_byte_array_to_string(item_bytes[i+16:i+20]),
#            "Value": bytes_to_int(item_bytes[i+16:i+20]),
#            "Notes": "Sort Order"
#            })
#        i = i + 20
#        j = j + 1
#
#       for item in btl_tbl_item_values:
#           print(item)
#
#       df = pd.DataFrame(btl_tbl_item_values)
#       df.to_csv("Battle Table Items.csv", index=False, quoting=csv.QUOTE_ALL)


def write_item_sort_order() -> None:
    battle_table_bytes = read_data(ResourceType.BIN, key="battle_table")
    battle_table_item_definitions = read_data(ResourceType.CSV, "battle_table_item_definitions")
    for battle_table_item_definition in battle_table_item_definitions:
        if battle_table_item_definition["Notes"] == "Sort Order":
            offset = int(battle_table_item_definition["Offset"], 16)
            replacement = sort_order[int(battle_table_item_definition["Item Index"]) - 1]
            replacement_byte_array = replacement.to_bytes(4, byteorder = "little")
            battle_table_bytes[offset] = replacement_byte_array[0]
            battle_table_bytes[offset + 1] = replacement_byte_array[1]
            battle_table_bytes[offset + 2] = replacement_byte_array[2]
            battle_table_bytes[offset + 3] = replacement_byte_array[3]
    write_data(ResourceType.BIN, battle_table_bytes, "battle_table", overwrite=True, create_parents=True)


def write_item_sell_price() -> None:
    battle_table_bytes = read_data(ResourceType.BIN, key="battle_table")
    battle_table_item_definitions = read_data(ResourceType.CSV, "battle_table_item_definitions")
    for battle_table_item_definition in battle_table_item_definitions:
        if battle_table_item_definition["Notes"] == "Sell Price":
            if int(battle_table_item_definition["Item Index"]) not in filler_item_ids:
                offset = int(battle_table_item_definition["Offset"], 16)
                replacement = 0
                replacement_byte_array = replacement.to_bytes(2, byteorder = "little")
                battle_table_bytes[offset] = replacement_byte_array[0]
                battle_table_bytes[offset + 1] = replacement_byte_array[1]
    write_data(ResourceType.BIN, battle_table_bytes, "battle_table", overwrite=True, create_parents=True)


def write_item_buy_price(new_prices: Dict[int, int]) -> None:
    battle_table_bytes = read_data(ResourceType.BIN, key="battle_table")
    battle_table_item_definitions = read_data(ResourceType.CSV, "battle_table_item_definitions")
    for battle_table_item_definition in battle_table_item_definitions:
        if battle_table_item_definition["Notes"] == "Buy Price":
            if int(battle_table_item_definition["Item Index"]) in new_prices.keys():
                offset = int(battle_table_item_definition["Offset"], 16)
                replacement = new_prices[int(battle_table_item_definition["Item Index"])]
                replacement_byte_array = replacement.to_bytes(2, byteorder = "little")
                battle_table_bytes[offset] = replacement_byte_array[0]
                battle_table_bytes[offset + 1] = replacement_byte_array[1]
    write_data(ResourceType.BIN, battle_table_bytes, "battle_table", overwrite=True, create_parents=True)


def write_item_sort_order_and_sell_price(settings_file: Path | None = None) -> None:
    settings_data = read_data(ResourceType.JSON, path=settings_file, ask_prompt=True)
    new_prices = {}
    new_prices[4] = 400 # Elixir added for WL flowers
    new_prices[254] = settings_data.get("mythril_price")         # TODO: Default Mythril Price
    new_prices[255] = settings_data.get("orichalcum_price")     # TODO: Default Orichalcum Price
    write_item_sort_order()
    write_item_sell_price()
    write_item_buy_price(new_prices)


if __name__ == "__main__":
    write_item_sort_order_and_sell_price()