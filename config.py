from typing import Dict, Literal, Union
from argparse import Namespace
from enum import IntEnum
import sys

import wx

from helpers import read_json, root_path, write_json, WxControlType

NodeType = Literal["mod", "settings", "seed"]

class APVersion(IntEnum):
    AP_MAIN = 1
    AP_DEV = 2
    
class PlatformType(IntEnum):
    WINDOWS = 1
    LINUX = 2
    MACOS = 3
    

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
    presets_path = root_path().joinpath(f"{node_name}_generator_presets.json")
    data = read_json(file_path=presets_path, ask_prompt=False)
    return data

def write_presets(node_name: NodeType, args: Namespace) -> None:
    presets_path = root_path().joinpath(f"{node_name}_generator_presets.json")
    pythonic_vars = vars(args)
    if node_name == "mod":
        pythonic_vars = {
            key: value for key, value in pythonic_vars.items() if key in ["ap_zip_file", "kh1_data_path"]
        }
    write_json(presets_path, pythonic_vars, overwrite=True, create_parents=True)


def get_ap_version(settings_data: Dict) -> APVersion:
    if getattr(settings_data, "version", None) is not None:
        if settings_data["version"] not in set(version.value for version in APVersion):
            version = APVersion.AP_MAIN
        else:
            version = APVersion(settings_data["version"])
    else:
        version = APVersion.AP_MAIN
    return version