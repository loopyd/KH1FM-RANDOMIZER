from typing import Dict, Literal
from argparse import Namespace

from helpers import read_json, root_path, write_json

NodeType = Literal["mod", "settings", "seed"]


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