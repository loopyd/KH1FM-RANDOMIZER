from pathlib import Path

from config import ResourceType, read_data, write_data


def write_seed(settings_file: Path | None = None) -> None:
    settings_data = read_data(kind=ResourceType.JSON, path=settings_file, ask_prompt=True)
    seed = settings_data["seed"]
    write_data(kind=ResourceType.PLAINTEXT, data=seed, key="seed", overwrite=True, create_parents=True)


if __name__ == "__main__":
    write_seed()