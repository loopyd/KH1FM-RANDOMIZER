import sys
from typing import Dict

from gooey import Gooey,GooeyParser
import shutil
import subprocess
import re
from pathlib import Path

from helpers import root_path, read_json, write_json, copy_and_replace, clear_folder

# Handle Splash Screen
if getattr(sys, 'frozen', False):
    import pyi_splash
    pyi_splash.close()


def read_presets() -> Dict:
    presets_path = root_path().joinpath("seed_generator_presets.json")
    data = read_json(presets_path)
    return data


def write_presets(args):
    presets_path = root_path().joinpath("seed_generator_presets.json")
    write_json(presets_path, vars(args), overwrite=True)


def handle_replacing_ap_world(archipelago_directory: Path, replace_ap_world: bool) -> None:
    if replace_ap_world:
        print("Moving AP World to Archipelago directory...")
        ap_world_file = root_path().joinpath("AP World", "kh1.apworld")
        if not ap_world_file.is_file() or not ap_world_file.exists():
            raise FileNotFoundError(f"Couldn't find {ap_world_file}!  Make sure the file exists and try again.")
        destination_path = archipelago_directory.joinpath("lib", "worlds", "kh1.apworld")
        copy_and_replace(ap_world_file, destination_path)
        print(f"{ap_world_file} moved to {destination_path}")


def move_settings_file_to_players_folder(archipelago_directory: Path, settings_file: Path, clean_players_folder: bool):
    print("Moving settings file to Archipelago Players folder...")
    players_directory = archipelago_directory.joinpath("Players")
    if not players_directory.exists():
        players_directory.mkdir(parents=True, exist_ok=True)
    if clean_players_folder:
        clear_folder(players_directory)
    shutil.copy(settings_file, players_directory)
    print(f"{settings_file} copied to {players_directory}")


def generate_ap_game(archipelago_directory: Path) -> Path:
    print("Generating AP game...")
    archipelago_executable = archipelago_directory.joinpath("ArchipelagoGenerate.exe")
    if archipelago_executable.is_file() and archipelago_executable.exists():
        p = subprocess.run(archipelago_executable, input = "\n", capture_output=True, text=True)
    else:
        raise FileNotFoundError(f"Couldn't find ArchipelagoGenerate.exe in {archipelago_directory}!  Make sure Archipelago is properly installed and try again.")
    print(p.stdout)
    try:
        generated_seed_zip = re.search("AP.*.zip", str(p.stdout)).group()
    except AttributeError:
        raise RuntimeError("Couldn't find generated seed zip in ArchipelagoGenerate.exe output!  Make sure Archipelago is properly installed and try again.")
    print(f"Found generated seed zip: {generated_seed_zip}")
    return Path(generated_seed_zip)


def move_generated_seed_zip_to_files(archipelago_directory: Path, generated_seed_zip: Path):
    print("Moving generated game back to files...")
    files_path = root_path().joinpath("Files")
    if not files_path.exists():
        files_path.mkdir(parents=True, exist_ok=True)
    generated_seed_zip_path = archipelago_directory.joinpath("Output", generated_seed_zip)
    if not generated_seed_zip_path.is_file() or not generated_seed_zip_path.exists():
        raise FileNotFoundError(f"Couldn't find generated seed zip at {generated_seed_zip_path}!  Make sure Archipelago is properly installed and try again.")
    destination_seed_zip_path = files_path.joinpath(generated_seed_zip.name)
    shutil.move(generated_seed_zip_path, destination_seed_zip_path)
    print(f"Moved generated seed zip from {generated_seed_zip_path} to {destination_seed_zip_path}")


@Gooey(program_name='KH1 Randomizer Seed Generator',
        image_dir=str(root_path().joinpath("Images")),
        program_description = "Program to generate KH1 Randomizer seed.",
        header_bg_color="#5E5540")

def main():
    presets = read_presets()
    parser = GooeyParser()
    parser.add_argument("archipelago_directory",
        widget = "DirChooser",
        default = presets["archipelago_directory"],
        metavar = "Archipelago Directory",
        help = "The directory where Archipelago is installed, which will be used for generation.")
    parser.add_argument("settings_file",
        widget = "FileChooser",
        default = presets["settings_file"],
        metavar = "Settings File",
        help = "The settings file (yaml) to be used in generation.")
    parser.add_argument("--replace_ap_world",
        choices = ["Yes",
            "No"],
        default = presets["replace_ap_world"],
        metavar = "Replace AP World",
        help = "Determines whether to replace the AP World in the specified Archipelago installation.  If unsure, set this to \"Yes\".")
    parser.add_argument("--clean_players_folder",
        choices = ["Yes",
            "No"],
        default = presets["clean_players_folder"],
        metavar = "Clean Players Folder",
        help = "Determines whether clear all previous data in Archipelago's \"Players\" folder before generation.\nSet to \"No\" if there are YAMLs or subfolders in this folder you'd like to keep.")
    
    args = parser.parse_args()
    
    archipelago_directory = getattr(args, "archipelago_directory")
    if archipelago_directory is None or not Path(archipelago_directory).is_dir() or not Path(archipelago_directory).exists():
        FileNotFoundError(f"Error: {archipelago_directory} is not a valid directory, or does not exist.")
    
    settings_file = getattr(args, "settings_file")
    if settings_file is None or not Path(settings_file).is_file() or not Path(settings_file).exists():
        FileNotFoundError(f"Error: {settings_file} is not a valid file, or does not exist.")
    
    replace_ap_world = getattr(args, "replace_ap_world")
    if replace_ap_world not in ["Yes", "No"]:
        ValueError("Error: replace_ap_world must be either \"Yes\" or \"No\".")
        
    clean_players_folder = getattr(args, "clean_players_folder")
    if clean_players_folder not in ["Yes", "No"]:
        ValueError("Error: clean_players_folder must be either \"Yes\" or \"No\".")
        
    write_presets(args)
    
    handle_replacing_ap_world(archipelago_directory, replace_ap_world == "Yes")
    move_settings_file_to_players_folder(archipelago_directory, settings_file, clean_players_folder == "Yes")
    generated_seed_zip = generate_ap_game(archipelago_directory)
    move_generated_seed_zip_to_files(archipelago_directory, generated_seed_zip)
    
    
if __name__ == "__main__":
    main()
    
    