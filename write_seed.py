from pathlib import Path

from config import APVersion
from helpers import root_path, read_json, write_plaintext


def output_seed(seed: str) -> None:
    output_path = root_path().joinpath("Working", "scripts", "randofiles", "seed.txt")
    write_plaintext(file_path=output_path, content=seed, overwrite=True, create_parents=True)


def write_seed(settings_file: Path | None = None, version: APVersion = APVersion.AP_DEV) -> None:
    settings_data = read_json(file_path=settings_file, ask_prompt=True)
    seed = settings_data["seed"]
    output_seed(seed)


if __name__ == "__main__":
    write_seed()