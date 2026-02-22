import shutil
from pathlib import Path

from config import APVersion
from helpers import root_path, get_file

def write_settings_file(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> Path:
    settings_file = get_file(file_path=settings_file, file_type=[("JSON", "*.json")], ask_prompt=True, label="KH1 Randomizer Settings JSON")
    
    target_dir = root_path().joinpath("Working")
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    target_path = target_dir.joinpath(settings_file.name)
    shutil.copy2(settings_file, target_path)
    print(f"Copied settings file to: {target_path}")
    return target_path

if __name__ == "__main__":
    write_settings_file()