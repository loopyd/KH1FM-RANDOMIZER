from pathlib import Path

import yaml
from datetime import datetime

from config import ResourceType, read_data, write_data
from helpers import root_path, list_files_recursive, remove_path, create_zip


def create_mod_yaml(seed: int, slot_name: str) -> None:
    seed_string = hex(int(str(seed).replace("W", ""))).upper().replace("0X", "")
    data = {
        "title": f"KH1R {slot_name} {seed_string}",
        "originalAuthor": "Gicu",
        "description": "Necessary files for KH1FM Archipelago Randomizer.  For more info - kh1fmrando.com",
        "dependencies": [],
        "assets": []
    }
    
    directory_path = root_path().joinpath("Working")
    files = list_files_recursive(directory_path)
    remove_path(files, directory_path)
    for file in files:
        if file != "mod.yml":
            data["assets"].append({
                "name": str(file),
                "method": "copy",
                "source": [{"name": str(file)}]
            })
    
    mod_yaml_path = root_path().joinpath("Working", "mod.yml")
    mod_yaml_str = yaml.safe_dump(data, sort_keys=False)
    write_data(ResourceType.PLAINTEXT, mod_yaml_str, path=mod_yaml_path, overwrite=True, create_parents=True)


def write_mod_zip(settings_file: Path | None = None) -> None:
    settings_data = read_data(ResourceType.JSON, path=settings_file, ask_prompt=True)
    now = datetime.now()
    seed = settings_data["seed"]
    slot_name = settings_data.get("slot_name", "")
    create_mod_yaml(seed, slot_name)
    directory_to_zip = root_path().joinpath("Working")
    output_zip_file = root_path().joinpath('Output', 'mod_' + now.strftime("%Y%m%d%H%M%S") + ".zip")
    create_zip(zip_file_path=output_zip_file, directory_path=directory_to_zip, overwrite=True)

if __name__=="__main__":
    write_mod_zip()