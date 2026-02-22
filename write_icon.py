from shutil import copyfile

from config import APVersion
from helpers import root_path


def write_icon(version: APVersion = APVersion.AP_DEV):
    program_icon_source = root_path().joinpath("Images", "program_icon.png")
    program_icon_destination = root_path().joinpath("Working", "icon.png")
    copyfile(program_icon_source, program_icon_destination)

if __name__ == "__main__":
    write_icon()