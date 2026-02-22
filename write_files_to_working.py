import shutil
from typing import Dict, List
from pathlib import Path

from config import APVersion
from helpers import get_folder, root_path, read_csv


def write_static_files() -> None:
    source_path = root_path().joinpath("Static Files")
    destination_path = root_path().joinpath("Working")
    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)


def list_definition_files_in_current_directory() -> List[str]:
    files = []
    documentation_path = root_path().joinpath("Documentation")
    for file in documentation_path.iterdir():
        if "KH1FM Documentation" in file:
            files.append(file)
    return files


def copy_src_kh1_files_to_output(kh1_data_path: Path, csv_lines: List[dict]) -> None:
    copied_files = []
    for line in csv_lines:
        if "File" in line.keys():
            if line["File"] not in copied_files:
                source_path = kh1_data_path
                if "Use Corrected File?" in line.keys():
                    if line["Use Corrected File?"] == "Y":
                        source_path = root_path().joinpath("Corrected EVDLs")
                input_full_path = source_path.joinpath(line["File"])
                output_full_path = root_path().joinpath("Working", line["File"])
                print(f"Copying {input_full_path} to {output_full_path}")
                output_directory = output_full_path.parent
                if not output_directory.exists():
                    output_directory.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(input_full_path, output_full_path)
                copied_files.append(line["File"])


def write_files_to_working(kh1_data_path: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    kh1_data_path = get_folder(folder_path=kh1_data_path, label="KH1 Data Path", ask_prompt=True)
    csv_lines: List[Dict] = []
    for file in list_definition_files_in_current_directory():
        file_path = root_path().joinpath("Documentation", file)
        csv_lines.extend(read_csv(file_path=file_path))
    copy_src_kh1_files_to_output(kh1_data_path, csv_lines)
    write_static_files()


if __name__=="__main__":
    write_files_to_working()