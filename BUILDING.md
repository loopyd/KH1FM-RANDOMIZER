
# Building the project

You need:

- Working installation of pyenv
- Working C++ compiler accessible to shell session (msvc on Windows, gcc on linux)

## Environment Setup 

Setup the project:

```sh
pyenv install miniconda-latest
pyenv activate miniconda-latest
```

Run from the virtual conda environment to create the local environment itself:

```sh
conda env create -f environment.yml -p ./.venv
```

## Building

Now you can build the bundled installer in the environment.  Enter it first

```sh
conda activate ./.venv
```

Then run:

(For Linux building):
```sh
pyinstaller --noconsole --onefile --icon=./Images/config_icon.ico mod_generator.py --splash "./Images/splash.png" --add-data=./mod_generator_presets.json:. --add-data=Images:Images --add-data=AP\ World:AP\ World --add-data=Corrected\ EVDLs:Corrected\ EVDLs --add-data=Default\ Settings\ JSON:Default\ Settings\ JSON --add-data=Documentation:Documentation --add-data=Static\ Files:Static\ Files --add-data=Template\ Luas:Template\ Luas
pyinstaller --noconsole --onefile --icon=./Images/config_icon.ico seed_generator.py --splash "./Images/splash.png" --add-data=./seed_generator_presets.json:. --add-data=Images:Images --add-data=Images:Images --add-data=AP\ World:AP\ World --add-data=Default\ Settings\ JSON:Default\ Settings\ JSON
pyinstaller --noconsole --onefile --icon=./Images/config_icon.ico settings_generator.py --splash "./Images/splash.png" --add-data=./settings_generator_presets.json:. --add-data=Images:Images --add-data=Images:Images --add-data=AP\ World:AP\ World --add-data=Default\ Settings\ JSON:Default\ Settings\ JSON
```

Your results are in `/dist`.  if you want to run something as a developer, you'll need to do it in the activated virtual environment, ex.:

```sh
python settings_generator.py
```
