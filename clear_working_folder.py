from helpers import clear_folder, root_path


def clear_working_folder() -> None:
    output_folder = root_path().joinpath("Working")
    clear_folder(output_folder)


if __name__ == "__main__":
    clear_working_folder()