from typing import Dict, Literal, Union, Tuple, Any
from pathlib import Path
from argparse import Namespace
from enum import IntEnum, Enum
import sys

import wx

from helpers import (
    read_json,
    root_path,
    write_json,
    WxControlType,
    read_csv,
    read_plaintext,
    read_bytes,
    write_bytes,
    write_plaintext,
    write_csv,
)

NodeType = Literal["mod", "settings", "seed"]

class ResourceType(Enum):
    CSV = "csv"
    JSON = "json"
    BIN = "bin"
    PLAINTEXT = "plaintext"
    LUA = "lua"
    

class APVersion(IntEnum):
    AP_MAIN = 1
    AP_DEV = 2
    
    
class PlatformType(IntEnum):
    WINDOWS = 1
    LINUX = 2
    MACOS = 3

FILE_PATHS: Dict[str, Dict[str, Tuple[str, ...] | str]] = {
    "csv": {
        "evdl_locations": ("Documentation", "KH1FM Documentation - Static Items.csv"),
        "enemy_drop_definitions": ("Documentation", "KH1FM Documentation - Enemy Stats and Drops.csv"),
        "bambi_definitions": ("Documentation", "KH1FM Documentation - Bambi Drops.csv"),
        "chest_definitions": ("Documentation", "KH1FM Documentation - Chest Items.csv"),
        "rewards_definitions": ("Documentation", "KH1FM Documentation - Battle Table Reward Items.csv"),
        "level_up_stats_definitions": ("Documentation", "KH1FM Documentation - Battle Table Sora Level Up Stats.csv"),
        "level_up_abilities_definitions": ("Documentation", "KH1FM Documentation - Battle Table Sora Level Up Abilities.csv"),
        "weapon_stat_definitions": ("Documentation", "KH1FM Documentation - Keyblade Stats.csv"),
        "battle_table_item_definitions": ("Documentation", "KH1FM Documentation - Battle Table Items.csv"),
        "map_prize_definitions": ("Documentation", "KH1FM Documentation - Map Prizes.csv"),
        "exp_chart_definitions": ("Documentation", "KH1FM Documentation - EXP Chart.csv"),
        "spell_mp_cost_definitions": ("Documentation", "KH1FM Documentation - Spell MP Cost.csv"),
        "spell_effectiveness_definitions": ("Documentation", "KH1FM Documentation - Spell Effectiveness.csv"),
        "gummi_block_prices": ("Documentation", "KH1FM Documentation - Gummi Block Prices.csv"),
        "starting_accessory_equipped_definitions": ("Documentation", "KH1FM Documentation - Party Member Starting Accessories Equipped.csv"),
        "starting_accessory_stock_definitions": ("Documentation", "KH1FM Documentation - Party Member Starting Accessories Stock.csv"),
        "map_enemies": ("Documentation", "KH1FM Documentation - Map Enemies.csv"),
        "enemy_categories": ("Documentation", "KH1FM Documentation - Enemy Categories.csv"),
    },
    "lua": {
        "template_lucky_emblems": ("Template Luas", "1fmRandoHandleLuckyEmblems.lua"),
        "template_interaction": ("Template Luas", "1fmRandoInteraction.lua"),
        "template_fix_combo_master": ("Template Luas", "1fmRandoFixComboMaster.lua"),
        "template_map_prize": ("Template Luas", "1fmRandoMapPrizes.lua"),
        "template_handle_items": ("Template Luas", "1fmRandoHandleItems.lua"),
        "template_death_link": ("Template Luas", "1fmRandoHandleDeathLink.lua"),
        "template_destiny_islands": ("Template Luas", "1fmRandoAllowDestinyIslands.lua"),
        "template_receive_ap_items": ("Template Luas", "1fmRandoReceiveAPItems.lua"),
        "template_ap_cost": ("Template Luas", "1fmRandoAPCosts.lua"),
        "template_gummi_items": ("Template Luas", "1fmRandoGummiItems.lua"),
        "template_augments": ("Template Luas", "1fmRandoHandleAugments.lua"),
        "template_synth": ("Template Luas", "1fmRandoSynthesis.lua"),
        "template_synth_names": ("Template Luas", "1fmRandoWriteSynthesisItemNames.lua"),
        "template_chest": ("Template Luas", "1fmRandoChests.lua"),
        "output_lucky_emblems": ("Working", "scripts", "1fmRandoHandleLuckyEmblems.lua"),
        "output_interaction": ("Working", "scripts", "1fmRandoInteraction.lua"),
        "output_fix_combo_master": ("Working", "scripts", "1fmRandoFixComboMaster.lua"),
        "output_map_prize": ("Working", "scripts", "1fmRandoMapPrizes.lua"),
        "output_handle_items": ("Working", "scripts", "1fmRandoHandleItems.lua"),
        "output_death_link": ("Working", "scripts", "1fmRandoHandleDeathLink.lua"),
        "output_destiny_islands": ("Working", "scripts", "1fmRandoAllowDestinyIslands.lua"),
        "output_receive_ap_items": ("Working", "scripts", "1fmRandoReceiveAPItems.lua"),
        "output_ap_cost": ("Working", "scripts", "1fmRandoAPCosts.lua"),
        "output_augments": ("Working", "scripts", "1fmRandoHandleAugments.lua"),
        "output_synth": ("Working", "scripts", "1fmRandoSynthesis.lua"),
        "output_synth_names": ("Working", "scripts", "1fmRandoWriteSynthesisItemNames.lua"),
        "output_gummi_items": ("Working", "scripts", "1fmRandoGummiItems.lua"),
        "output_chest": ("Working", "scripts", "1fmRandoChests.lua"),
        "output_scripts_dir": ("Working", "scripts"),
    },
    "bin": {
        "battle_table": ("Working", "btltbl.bin"),
        "bambi_mdls": ("Working", "xa_ex_4030.mdls"),
        "sysmsg": ("Working", "remastered", "menu", "uk", "sysmsg.bin", "UK_sysmsg.binl"),
        "item_help": ("Working", "remastered", "btltbl.bin", "UK_BattleHelp.bin"),
        "gummi_item_descriptions": ("Working", "exchange", "UK_gumi_mes_data.bin"),
        "gummi_item_descriptions_offsets": ("Working", "exchange", "UK_gumi_mes_ofs.bin"),
        "gumi_spec_file": ("Working", "gumi_spec_file.bin"),
        "item_descriptions": ("Working", "menu", "itemdict.bin", "UK_itemdict.binl"),
        "starting_accessory_equipped_evdl": ("Working", "remastered", "dh01.ard", "UK_dh01c.ev"),
        "starting_accessory_stock_evdl": ("Working", "remastered", "dh01.ard", "UK_dh01c.ev"),
        "map_prize": ("Working", "map_prize.bin"),
        "working_dir": ("Working",),
    },
    "plaintext": {
        "seed": ("Working", "scripts", "randofiles", "seed.txt"),
    },
    "json": {
        "presets": ("{node}_generator_presets.json",),
    },
}   

gui_theme: Dict[Union[str, WxControlType], Dict[str, Dict[PlatformType, str]]] = {
    "gooey": {
        "header_bg_color" : {
            PlatformType.WINDOWS: "#efcf78", PlatformType.LINUX: "#554e3b", PlatformType.MACOS: "#554e3b"
            },
        "body_bg_color" : {
            PlatformType.WINDOWS: "#bdbdbd", PlatformType.LINUX: "#bdbdbd", PlatformType.MACOS: "#bdbdbd"
            },
        "footer_bg_color" : {
            PlatformType.WINDOWS: "#A9A9A9", PlatformType.LINUX: "#A9A9A9", PlatformType.MACOS: "#A9A9A9"
            },
        "terminal_bg_color" : {
            PlatformType.WINDOWS: "#303030", PlatformType.LINUX: "#3d3d3d", PlatformType.MACOS: "#3d3d3d"
            },
        "terminal_font_color" : {
            PlatformType.WINDOWS: "#E1E1E1", PlatformType.LINUX: "#31F006", PlatformType.MACOS: "#FFFFFF"
            },
    },
    wx.Button: {
        "bg_color" : {
            PlatformType.WINDOWS: "#A9A9A9", PlatformType.LINUX: "#A9A9A9", PlatformType.MACOS: "#A9A9A9"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.CheckBox: {
        "bg_color" : {
            PlatformType.WINDOWS: "#bdbdbd", PlatformType.LINUX: "#bdbdbd", PlatformType.MACOS: "#bdbdbd"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.RadioButton: {
        "bg_color" : {
            PlatformType.WINDOWS: "#bdbdbd", PlatformType.LINUX: "#bdbdbd", PlatformType.MACOS: "#bdbdbd"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    # this screws up the header labels
    # wx.StaticText: {
    #     "bg_color" : {
    #         PlatformType.WINDOWS: "#bdbdbd", PlatformType.LINUX: "#bdbdbd", PlatformType.MACOS: "#bdbdbd"
    #         },
    #     "font_color" : {
    #         PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
    #         },
    # },
    wx.TextCtrl: {
        "bg_color" : {
            PlatformType.WINDOWS: "#FFFFFF", PlatformType.LINUX: "#FFFFFF", PlatformType.MACOS: "#FFFFFF"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.Choice: {
        "bg_color" : {
            PlatformType.WINDOWS: "#FFFFFF", PlatformType.LINUX: "#FFFFFF", PlatformType.MACOS: "#FFFFFF"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.ListBox: {
        "bg_color" : {
            PlatformType.WINDOWS: "#FFFFFF", PlatformType.LINUX: "#FFFFFF", PlatformType.MACOS: "#FFFFFF"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.ComboBox: {
        "bg_color" : {
            PlatformType.WINDOWS: "#FFFFFF", PlatformType.LINUX: "#FFFFFF", PlatformType.MACOS: "#FFFFFF"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.SpinCtrl: {
        "bg_color" : {
            PlatformType.WINDOWS: "#FFFFFF", PlatformType.LINUX: "#FFFFFF", PlatformType.MACOS: "#FFFFFF"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000"
            },
    },
    wx.Slider: {
        "bg_color" : {
            PlatformType.WINDOWS: "#bdbdbd", PlatformType.LINUX: "#bdbdbd", PlatformType.MACOS: "#bdbdbd"
            },
        "font_color" : {
            PlatformType.WINDOWS: "#000000", PlatformType.LINUX: "#000000", PlatformType.MACOS: "#000000" 
            },
    }
}

def _build_path(category: ResourceType | str, key: str, **format_args) -> Path:
    category_key = category.value if isinstance(category, ResourceType) else category
    parts = FILE_PATHS[category_key][key]
    if isinstance(parts, str):
        parts = (parts,)
    return root_path().joinpath(*(part.format(**format_args) for part in parts))


def read_data(
    kind: ResourceType,
    key: str | None = None,
    *,
    path: Path | None = None,
    path_parts: Tuple[str, ...] | None = None,
    ask_prompt: bool = False,
    **format_args,
) -> Any:
    """
    Reads data from a file of the specified kind.
    
    Args:
        kind (ResourceType): The kind of file to read.
        key (str | None): The key identifying the file path in the config.py FILE_PATHS structure. If path is not provided, this is required.
        path (Path | None): An optional Path object specifying the file path directly.
        path_parts (Tuple[str, ...] | None): An optional tuple of strings specifying parts of the path relative to the root path.
        ask_prompt (bool): Whether to prompt the user for the file path if it cannot be found.
        format_args: Additional arguments to format the path if using a key.
    """
    if isinstance(kind, str):
        kind = ResourceType(kind)
    if path is None:
        if path_parts is not None:
            path = root_path().joinpath(*path_parts)
        else:
            if key is None:
                raise ValueError("key is required when path is not provided")
            path = _build_path(kind, key, **format_args)
    if kind == ResourceType.CSV:
        return read_csv(file_path=path, ask_prompt=ask_prompt)
    if kind == ResourceType.JSON:
        return read_json(file_path=path, ask_prompt=ask_prompt)
    if kind == ResourceType.BIN:
        return read_bytes(file_path=path, ask_prompt=ask_prompt)
    return read_plaintext(file_path=path, ask_prompt=ask_prompt)


def write_data(
    kind: ResourceType,
    data: Any,
    key: str | None = None,
    *,
    path: Path | None = None,
    path_parts: Tuple[str, ...] | None = None,
    overwrite: bool = False,
    create_parents: bool = True,
    **format_args,
) -> None:
    """
    Writes data to a file of the specified kind.
    
    Args:
        kind (ResourceType): The kind of file to write.
        data (Any): The data to write to the file.
        key (str | None): The key identifying the file path in the config.py FILE_PATHS structure. If path is not provided, this is required.
        path (Path | None): An optional Path object specifying the file path directly.
        path_parts (Tuple[str, ...] | None): An optional tuple of strings specifying parts of the path relative to the root path.
        overwrite (bool): Whether to overwrite the file if it already exists.
        create_parents (bool): Whether to create parent directories if they do not exist.
        format_args: Additional arguments to format the path if using a key.
    """
    if isinstance(kind, str):
        kind = ResourceType(kind)
    if path is None:
        if path_parts is not None:
            path = root_path().joinpath(*path_parts)
        else:
            if key is None:
                raise ValueError("key is required when path is not provided")
            path = _build_path(kind, key, **format_args)
    if kind == ResourceType.JSON:
        write_json(file_path=path, data=data, overwrite=overwrite, create_parents=create_parents)
        return
    if kind == ResourceType.BIN:
        write_bytes(file_path=path, data=data, overwrite=overwrite, create_parents=create_parents)
        return
    if kind == ResourceType.CSV:
        write_csv(file_path=path, data=data, overwrite=overwrite, create_parents=create_parents)
        return
    write_plaintext(file_path=path, data=data, overwrite=overwrite, create_parents=create_parents)


def get_theme_color(node_name: Literal["gooey"] | WxControlType,color_name: str) -> str | None:
    platform = sys.platform
    if platform.startswith("win"):
        platform_key = PlatformType.WINDOWS
    elif platform.startswith("linux"):
        platform_key = PlatformType.LINUX
    elif platform.startswith("darwin"):
        platform_key = PlatformType.MACOS
    else:
        platform_key = PlatformType.WINDOWS
    node = gui_theme.get(node_name, None)
    if node is None:
        return None
    return node.get(color_name, {}).get(platform_key, None) 

def read_presets(node_name: NodeType) -> Dict:
    return read_data(ResourceType.JSON, "presets", node=node_name)

def write_presets(node_name: NodeType, args: Namespace) -> None:
    pythonic_vars = vars(args)
    if node_name == "mod":
        pythonic_vars = {
            key: value for key, value in pythonic_vars.items() if key in ["ap_zip_file", "kh1_data_path"]
        }
    write_data(ResourceType.JSON, pythonic_vars, "presets", node=node_name, overwrite=True, create_parents=True)


def get_ap_version(settings_data: Dict) -> APVersion:
    if getattr(settings_data, "version", None) is not None:
        if settings_data["version"] not in set(version.value for version in APVersion):
            version = APVersion.AP_MAIN
        else:
            version = APVersion(settings_data["version"])
    else:
        version = APVersion.AP_MAIN
    return version