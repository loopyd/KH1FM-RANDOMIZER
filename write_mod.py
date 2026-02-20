from pathlib import Path
from tkinter import filedialog

from clear_working_folder import clear_working_folder
from write_files_to_working import write_files_to_working
from write_enemy_drop_rewards import write_enemy_drop_rewards
from write_bambi_rewards import write_bambi_rewards
from write_chests_and_rewards import write_chests_and_rewards
from write_level_up_rewards import write_level_up_rewards
from write_mod_zip import write_mod_zip
from write_static_items import write_static_items
from write_keyblade_stats import write_keyblade_stats
from write_item_sort_order_and_sell_price import write_item_sort_order_and_sell_price
from write_synthesis_items import write_synthesis_items
from write_lucky_emblems_lua import write_lucky_emblems_lua
from write_interaction_lua import write_interaction_lua
from write_map_prizes import write_map_prizes
from write_exp_chart import write_exp_chart
from write_fix_combo_master import write_fix_combo_master
from write_map_prize_lua import write_map_prize_lua
from write_toggleable_luas import write_toggleable_luas
from write_handle_items_lua import write_handle_items_lua
from write_death_link_lua import write_death_link_lua
from write_destiny_islands_lua import write_destiny_islands_lua
from write_receive_ap_items_lua import write_receive_ap_items_lua
from write_seed import write_seed
from write_icon import write_icon
from write_synthesis_item_names_lua import write_synthesis_item_names_lua
from write_starting_accessories import write_starting_accessories
from write_ap_cost_lua import write_ap_cost_lua
from write_spell_info import write_spell_info
from write_gummi_items import write_gummi_items
from write_gummi_item_buy_and_sell_price import write_gummi_item_buy_and_sell_price
from write_augments import write_augments
from write_settings_file import write_settings_file
from validate_evdl_data import validate_evdl_data
from helpers import extract_zip, validate_json

def get_kh1_data_path():
    kh1_data_path = None
    while not kh1_data_path:
        kh1_data_path = filedialog.askdirectory()
        if not kh1_data_path:
            print("Error, please select a valid KH1 data path")
    return kh1_data_path

def write_mod(ap_zip_file_name: Path | None = None, kh1_data_path: Path | None = None):
    extract_zip(zip_file_path=ap_zip_file_name, ask_prompt=True)
    json_path = Path(ap_zip_file_name.with_suffix(''))
    
    item_location_map_file = validate_json(json_path.joinpath("item_location_map.json"))
    if item_location_map_file is None:
        raise FileNotFoundError("Error: item_location_map.json not found in the ap zip file.")
    
    keyblade_stats_file = validate_json(json_path.joinpath("keyblade_stats.json"))
    if keyblade_stats_file is None:
        raise FileNotFoundError("Error: keyblade_stats.json not found in the ap zip file.")
    
    settings_file = validate_json(json_path.joinpath("settings.json"))
    if settings_file is None:
        raise FileNotFoundError("Error: settings.json not found in the ap zip file.")
    
    ap_cost_file = validate_json(json_path.joinpath("ap_costs.json"))
    if ap_cost_file is None:
        raise FileNotFoundError("Error: ap_costs.json not found in the ap zip file.")
    
    mp_cost_file = validate_json(json_path.joinpath("mp_costs.json"))
    if mp_cost_file is None:
        raise FileNotFoundError("Error: mp_costs.json not found in the ap zip file.")
    
    print(f"Item Location Map File: {item_location_map_file}")
    print(f"Keyblade Stats File: {keyblade_stats_file}")
    print(f"Settings File: {settings_file}")
    print(f"AP Costs File: {ap_cost_file}")
    print(f"MP Costs File: {mp_cost_file}")
    
    if kh1_data_path is None:
        kh1_data_path = get_kh1_data_path()
    
    validate_evdl_data(kh1_data_path = kh1_data_path)
    clear_working_folder()
    
    print("Writing necessary files to working directory...")
    write_files_to_working(kh1_data_path = kh1_data_path)
    
    print("Writing static items...")
    write_static_items(seed_json_file = item_location_map_file)
    
    print("Writing enemy drops...")
    write_enemy_drop_rewards()
    
    print("Writing bambi drops...")
    write_bambi_rewards()
    
    print("Writing chests and rewards...")
    write_chests_and_rewards(seed_json_file = item_location_map_file)
    
    print("Writing level up rewards...")
    write_level_up_rewards(seed_json_file = item_location_map_file)
    
    print("Writing weapon stats...")
    write_keyblade_stats(seed_json_file = keyblade_stats_file)
    
    print("Writing item sort order and sell price...")
    write_item_sort_order_and_sell_price(settings_file = settings_file)
    
    print("Writing synthesis items...")
    write_synthesis_items(seed_json_file = item_location_map_file)
    
    print("Writing lucky emblem lua...")
    write_lucky_emblems_lua(settings_file = settings_file)
    
    print("Writing interaction lua...")
    write_interaction_lua(settings_file = settings_file)
    
    print("Writing map prizes...")
    write_map_prizes(seed_json_file = item_location_map_file)
    
    print("Writing EXP chart...")
    write_exp_chart(settings_file = settings_file)
    
    print("Writing combo master lua...")
    write_fix_combo_master(seed_json_file = item_location_map_file)
    
    print("Writing map prize lua...")
    write_map_prize_lua(seed_json_file = item_location_map_file)
    
    print("Writing toggleable luas...")
    write_toggleable_luas(settings_file = settings_file)
    
    print("Writing handle items lua...")
    write_handle_items_lua(settings_file = settings_file)
    
    print("Writing death link lua...")
    write_death_link_lua(settings_file = settings_file)
    
    print("Writing Destiny Islands lua...")
    write_destiny_islands_lua(settings_file = settings_file)
    
    print("Writing Receive AP Items lua...")
    write_receive_ap_items_lua(settings_file = settings_file)
    
    print("Writing synthesis item names lua...")
    write_synthesis_item_names_lua(settings_file = settings_file)
    
    print("Writing starting accessories...")
    write_starting_accessories(seed_json_file = item_location_map_file, settings_file = settings_file)
    
    print("Writing AP Costs lua...")
    write_ap_cost_lua(settings_file = settings_file, ap_cost_file = ap_cost_file)
    
    print("Writing spell info...")
    write_spell_info(settings_file = settings_file, mp_cost_file = mp_cost_file)
    
    print("Writing gummi items...")
    write_gummi_items(setings_file = settings_file)
    
    print("Writing gummi item buy and sell price...")
    write_gummi_item_buy_and_sell_price()
    
    print("Writing augment data...")
    write_augments(seed_json_file = item_location_map_file, settings_file = settings_file,  mp_cost_file = mp_cost_file)
    
    print("Writing settings file...")
    write_settings_file(settings_file = settings_file)
    
    print("Writing seed...")
    write_seed(settings_file = settings_file)
    
    print("Writing icon...")
    write_icon()
    
    print("Writing mod zip...")
    write_mod_zip(settings_file = settings_file)
    
    print("All jobs complete!  Enjoy!")

if __name__ == "__main__":
    write_mod()