import csv
import json
import os
import shutil
import struct
import sys
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple, Union, Type

import zipfile
import tkinter.filedialog as filedialog
import wx 

WxControlType = Union[
    Type[wx.Button],
    Type[wx.TextCtrl],
    Type[wx.RadioButton],
    Type[wx.CheckBox],
    Type[wx.StaticText],
    Type[wx.Choice],
    Type[wx.ListBox],
    Type[wx.ComboBox],
    Type[wx.SpinCtrl],
    Type[wx.Slider],
    Type[wx.Window]
]

WxControl = Union[
    wx.Button,
    wx.TextCtrl,
    wx.RadioButton,
    wx.CheckBox,
    wx.StaticText,
    wx.Choice,
    wx.ListBox,
    wx.ComboBox,
    wx.SpinCtrl,
    wx.Slider,
    wx.Window
]


def get_folder(folder_path: Path | None = None, ask_prompt: bool = True, label: str = "folder path") -> Path:
    """
    Validates that a folder path is a valid directory. Optionally prompts the user to select a folder if the provided path is invalid.
    
    Args:
        folder_path (Path | None): The path to the folder.
        ask_prompt (bool): Whether to ask the user to select a folder if the provided folder path is invalid. Defaults to True.
        label (str): A label to use in the prompt if the user needs to select a folder.
    """
    if folder_path is not None:
        if folder_path.is_dir() and folder_path.exists():
            return folder_path
    if not ask_prompt:
        raise FileNotFoundError(f"Error: {folder_path} is not a valid directory.")
    folder_selected = None
    while not folder_selected:
        folder_selected = filedialog.askdirectory(title=f"Select {label}", mustexist=True)
        if not folder_selected:
             print(f"Error, please select a valid {label}")
             continue
        folder_path = Path(folder_selected)
        if not folder_path.is_dir() or not folder_path.exists():    
            print(f"Error, please select a valid {label}")
            folder_selected = None
    return folder_path


def get_file(file_path: Path | None = None, file_type: Iterable[Tuple[str, str]] | None = None, ask_prompt: bool = True, label: str = "file path") -> Path:
    """
    Validates that a file path is a valid file. Optionally prompts the user to select a file if the provided path is invalid.

    Args:
        file_path (Path | None): The path to the file.
        file_type (Iterable[Tuple[str, str]] | None): The file types to filter by in the prompt.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to True.
        label (str): A label to use in the prompt if the user needs to select a file.

    Returns:
        Path: The validated file path.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.exists():
            return file_path
    if not ask_prompt:
        raise FileNotFoundError(f"Error: {file_path} is not a valid file.")
    file_selected = None
    while not file_selected:
        file_selected = filedialog.askopenfilename(title=f"Select {label}", filetypes=file_type, mustexist=True)
        if not file_selected:
             print(f"Error, please select a valid {label}")
             continue
        file_path = Path(file_selected)
        if not file_path.is_file() or not file_path.exists():    
            print(f"Error, please select a valid {label}")
            file_selected = None
    return file_path
    

def list_files_recursive(path: Path = Path('.'), filenames: List[str] | None = None) -> List[str]:
    """
    Recursively lists all files in a directory and its subdirectories.
    
    Args:
    
        path (Path): The directory path to list files from. Defaults to the current directory.
        filenames (List[str] | None): A list to store the file paths. If None, a new list will be created. Defaults to None.
    
    Returns:
        List[str]: A list of file paths.
    """
    if filenames is None:
        filenames = []
    for entry in path.resolve().iterdir():
        full_path = entry
        if full_path.is_dir():
            list_files_recursive(full_path, filenames)
        else:
            filenames.append(str(full_path.resolve()).replace("\\", "/"))
    return filenames


def remove_path(files: List[str], path: str) -> None:
    """
    Removes a specified path from a list of file paths.
    
    Args:
        files (List[str]): A list of file paths.
        path (str): The path to remove from the file paths.
    """
    for i in range(len(files)):
        files[i] = files[i].replace(path, "")
        

def replace_value_at_index(data: bytes, index: int, new_value: int, sentinal: bytes) -> bytes:
    """
    Replaces a 2-byte value at a specific index in a byte array, where the index is determined by the position of a sentinel byte sequence.
    
    Args:
        data (bytes): The original byte array.
        index (int): The index of the value to replace, relative to the position of the sentinel.
        new_value (int): The new value to insert at the specified index.
        sentinal (bytes): The byte sequence that indicates the end of the values and the start of the tail.
    """
    sentinel_index = data.index(sentinal)
    raw_values = data[:sentinel_index]
    tail = data[sentinel_index:]
    values = [v[0] for v in struct.iter_unpack("<H", raw_values)]
    if not (0 <= index < len(values)):
        raise IndexError(f"Index {index} out of range (0–{len(values)-1})")
    values[index] = new_value
    new_raw = b"".join(struct.pack("<H", v) for v in values)
    return new_raw + tail


def to_hex_no_0x(val: int) -> str:
    """
    Converts an integer to a hexadecimal string without the '0x' prefix, ensuring an even number of characters by padding with a leading zero if necessary.
    
    Args:
        val (int): The integer value to convert to hexadecimal.
    
    Returns:
        str: The hexadecimal representation of the integer, without the '0x' prefix and with an even number of characters.
    """
    val = hex(val).upper().replace("0X","")
    if len(val) % 2 == 1:
        val = "0" + val
    return val
    
    
def bytes_to_int(byte_array: bytes, byteorder='little') -> int:
    """
    Converts a byte array to an integer using the specified byte order.
    
    Args:
        byte_array (bytes): The byte array to convert.
        byteorder (str): The byte order to use for the conversion ('little' or 'big'). Defaults to 'little'.
        
    Returns:
        int: The integer representation of the byte array.
    """
    return int.from_bytes(byte_array, byteorder)


def convert_byte_array_to_string(byte_array: bytes) -> str:
    """
    Converts a byte array to a string of hexadecimal values, with each byte represented as two uppercase hexadecimal characters and separated by spaces.
    
    Args:
        byte_array (bytes): The byte array to convert.
        
    Returns:
        str: A string representation of the byte array in hexadecimal format, with bytes separated by spaces.
    """
    output_string = ""
    for byte in byte_array:
        output_string = output_string + to_hex_no_0x(byte) + " "
    return output_string[:-1]


def boolify(v: str) -> bool | str:
    """
    Converts "Yes"/"No" strings to boolean True/False, leaves other values unchanged.
    
    Args:
        v (str): The value to convert.
        
    Returns:
        bool or str: The converted boolean value if input is "Yes" or "No", otherwise returns the original value.
    """
    if isinstance(v, str) and v.lower() in ("yes", "no", "true", "false"):
        return v.lower() == "yes"
    return v


def space_to_snake(v: str) -> str:
    return str(v).replace(" ", "_").lower()
    
    
def clear_folder(folder_path: Path, remove_folder: bool = False):
    """
    Clears a folder of all files and subfolders.

    Args:
        folder_path (Path): The path to the folder to clear.
        remove_folder (bool): Whether to remove the folder itself after clearing. Defaults to False.
    
    Raises:
        FileNotFoundError: If the folder path does not exist or is not a directory.
    """
    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Error: {folder_path} is not a valid directory.")
    for filename in folder_path.iterdir():
        file_path = folder_path.joinpath(filename)
        try:
            if file_path.is_file() or file_path.is_symlink():
                file_path.unlink()
            elif file_path.is_dir() and file_path != folder_path:
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            raise e
    if remove_folder:
        try:
            folder_path.rmdir()
        except Exception as e:
            print(f"Failed to delete {folder_path}. Reason: {e}")
            raise e
            

def copy_and_replace(source_path: Path, destination_path: Path):
    """
    Copies a file or folder from source_path to destination_path, replacing the destination if it already exists.
    
    Args:
        source_path (Path): The path to the source file or folder.
        destination_path (Path): The path to the destination file or folder.
        
    Raises:
        FileNotFoundError: If the source path does not exist.
    """
    if not source_path.exists():
         raise FileNotFoundError(f"Error, {source_path} does not exist")
    if destination_path.exists():
        if destination_path.is_file():
            os.remove(destination_path)
        elif destination_path.is_dir():
            clear_folder(destination_path, remove_folder=True)
    if source_path.is_file():
        shutil.copy2(source_path, destination_path)
    else:
        shutil.copytree(source_path, destination_path)
        

def validate_json(file_path: Path | None) -> Path:
    """
    Validates that a file path points to a valid JSON file. Optionally prompts the user to select a file if the provided path is invalid.

    Args:
        file_path (Path): The path to the json file.

    Returns:
        Path: The validated file path if it is a valid JSON file, None otherwise.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.suffix.lower() == '.json' and file_path.exists():
            if file_path.stat().st_size > 0:
                return file_path
    return None
    
def read_json(file_path: Path | None, ask_prompt: bool = False) -> Dict:
    """
    Read JSON file with santiy checks

    Args:
        file_path (Path): The path to the json file.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to False.

    Returns:
        Dict: A serialized Dictionary of the contents of the json file.
    """
    if validate_json(file_path) is None:
        if ask_prompt:
            select_path = None
            while select_path is None:
                select_path = filedialog.askopenfilename(filetypes =[('JSON', '*.json')], title = "Select JSON File")
                if not select_path:
                    print("Error, please select a valid JSON file.")
                else:
                    file_path = Path(select_path)
        else:
            raise FileNotFoundError(f"Error: {file_path} is not a valid json file, or does not exist.")
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
def write_json(file_path: Path, data: Dict, overwrite: bool = False, create_parents: bool = True) -> None:
    """
    Write object to json file on disk.

    Args:
        file_path (Path): The path to the target json file
        data (Dict): The serialized data object to deserialize to json and write.
        overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        create_parents (bool, optional): Whether to create parent directories if they do not exist. Defaults to True.

    Raises:
        ValueError: If the file path is not a json file.
        FileExistsError: If the file already exists and overwrite is False.
    """
    if file_path.suffix.lower() != '.json':
        raise ValueError(f"Error: {file_path} is not a valid JSON file.")
    if not overwrite and file_path.exists():
        raise FileExistsError(f"Error: {file_path} already exists.")
    if not file_path.parent.exists() and create_parents:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.parent.exists() and not create_parents:
        raise FileNotFoundError(f"Error: Parent directory {file_path.parent} does not exist.")
    data = json.dumps(data, indent=4)
    with open(file_path, 'w') as file:
        file.write(data)


def validate_bytes(file_path: Path | None) -> Path | None:
    """
    Validates that a file path points to a valid file that can be read as bytes.

    Args:
        file_path (Path): The path to the file.

    Returns:
        bool: True if the file path is valid, False otherwise.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.exists():
            if file_path.stat().st_size > 0:
                return file_path
    return None

def read_bytes(file_path: Path, ask_prompt: bool = False) -> bytearray:
    """
    Reads a file as raw bytes.
    
    Args:
        file_path (Path): The path to the file to read.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to False.
        
    Returns:
        bytearray: The raw bytes of the file.
    """
    if validate_bytes(file_path) is None:
        if ask_prompt:
            select_path = None
            while select_path is None:
                select_path = filedialog.askopenfilename(title = "Select File")
                if not select_path:
                    print("Error, please select a valid file.")
                else:
                    file_path = Path(select_path)
        else:
            raise FileNotFoundError(f"Error: {file_path} is not a valid file or does not exist.")
    with open(file_path, mode = 'rb') as file:
        return bytearray(file.read())
    
def write_bytes(file_path: Path, data: bytearray, overwrite: bool = False, create_parents: bool = True) -> None:
    """
    Writes raw bytes to a file.

    Args:
        file_path (Path): The path to the target file.
        data (bytearray): The raw bytes to write to the file.
        overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        create_parents (bool, optional): Whether to create parent directories if they do not exist. Defaults to True.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
    """
    if not overwrite and file_path.exists():
        raise FileExistsError(f"Error: {file_path} already exists.")
    if not file_path.parent.exists() and create_parents:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.parent.exists() and not create_parents:
        raise FileNotFoundError(f"Error: Parent directory {file_path.parent} does not exist.")
    with open(file_path, mode = 'wb') as file:
        file.write(data)
        
def validate_plaintext(file_path: Path | None) -> Path | None:
    """
    Validates that a file path points to a valid plaintext file. Optionally prompts the user to select a file if the provided path is invalid.

    Args:
        file_path (Path | None): The path to the plaintext file.

    Returns:
        Path | None: The validated file path if it is a valid plaintext file, None otherwise.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.exists():
            if file_path.stat().st_size > 0:
                return file_path
    return None

def read_plaintext(file_path: Path, ask_prompt: bool = False) -> str:
    """
    Reads a plaintext file and returns its contents as a string.

    Args:
        file_path (Path): The path to the plaintext file.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to False.

    Returns:
        str: The contents of the plaintext file as a string.
    """
    if validate_plaintext(file_path) is None:
        if ask_prompt:
            select_path = None
            while select_path is None:
                select_path = filedialog.askopenfilename(filetypes =[('Text', '*.txt')], title = "Select Plaintext File")
                if not select_path:
                    print("Error, please select a valid plaintext file.")
                else:
                    file_path = Path(select_path)
        else:
            raise FileNotFoundError(f"Error: {file_path} is not a valid plaintext file, or does not exist.")
    with open(file_path, mode = 'r') as file:
        return file.read()
    
def write_plaintext(file_path: Path, data: str, overwrite: bool = False, create_parents: bool = True) -> None:
    """
    Writes a string to a plaintext file.

    Args:
        file_path (Path): The path to the target plaintext file.
        data (str): The string data to write to the file.
        overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        create_parents (bool, optional): Whether to create parent directories if they do not exist. Defaults to True.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
    """
    if not overwrite and file_path.exists():
        raise FileExistsError(f"Error: {file_path} already exists.")
    if not file_path.parent.exists() and create_parents:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.parent.exists() and not create_parents:
        raise FileNotFoundError(f"Error: Parent directory {file_path.parent} does not exist.")
    with open(file_path, mode = 'w') as file:
        file.write(data)

def validate_csv(file_path: Path | None) -> Path | None:
    """
    Validates that a file path points to a valid CSV file. Optionally prompts the user to select a file if the provided path is invalid.

    Args:
        file_path (Path): The path to the csv file.
    
    Returns:
        Path | None: The validated file path if it is a valid CSV file, None otherwise.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.suffix.lower() == ".csv" and file_path.exists():
            if file_path.stat().st_size > 0:
                return file_path
    return None

def read_csv(file_path: Path, ask_prompt: bool = False) -> List[Dict]:
    """
    Reads a csv file and returns a list of dictionaries representing the rows.

    Args:
        file_path (Path): The path to the csv file.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to False.

    Returns:
        List[Dict]: A list of dictionaries representing the rows of the csv file.
    """
    if validate_csv(file_path) is None:
        if ask_prompt:
            select_path = None
            while select_path is None:
                select_path = filedialog.askopenfilename(filetypes =[('CSV', '*.csv')], title = "Select CSV File")
                if not select_path:
                    print("Error, please select a valid CSV file.")
                else:
                    file_path = Path(select_path)
        else:
            raise FileNotFoundError(f"Error: {file_path} is not a valid file or does not exist.")
    with open(file_path, mode = 'r') as file:
        data = []
        csv_data = csv.DictReader(file)
        for line in csv_data:
            data.append(line)
    return data

def write_csv(file_path: Path, data: List[Dict], overwrite: bool = False, create_parents: bool = True) -> None:
    """
    Writes a list of dictionaries to a csv file.

    Args:
        file_path (Path): The path to the target csv file.
        data (List[Dict]): The list of dictionaries to write to the csv file.
        overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
        create_parents (bool, optional): Whether to create parent directories if they do not exist. Defaults to True.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
    """
    if not overwrite and file_path.exists():
        raise FileExistsError(f"Error: {file_path} already exists.")
    if not file_path.parent.exists() and create_parents:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.parent.exists() and not create_parents:
        raise FileNotFoundError(f"Error: Parent directory {file_path.parent} does not exist.")
    with open(file_path, mode = 'w', newline='') as file:
        if len(data) == 0:
            return
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def root_path() -> Path:
    """
    Substitutes the path to the root of the project, whether it's running as a script or as a bundled executable.

    Returns:
        Path: The path to the root of the project.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        mei_pass = getattr(sys, '_MEIPASS')
        if mei_pass is not None:
            return Path(mei_pass)
        else:
            return Path(os.path.dirname(__file__))
    return Path(os.path.dirname(__file__))

def get_nested_zip(zip_file_path: Path, allow_multiple: bool = False) -> Path | List[Path] | None:
    """
    Checks if a zip file contains another zip file.

    Args:
        zip_file_path (Path): The path to the zip file.
        allow_multiple (bool): If True, allows multiple nested zip files and returns a list of their paths. Default is False, an error will be raised if multiple zip files are found.

    Returns:
        Path or None: The path of the nested zip file if found, else None.
    """
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_files = [item for item in zip_file.namelist() if Path(item).suffix.lower() == '.zip']
            if len(zip_files) == 1:
                return zip_file_path.with_suffix("").joinpath(zip_files[0])
            elif len(zip_files) > 1:
                if allow_multiple:
                    return [zip_file_path.with_suffix("").joinpath(item) for item in zip_files]
                AssertionError(f"Multiple zip files found in the provided zip: {', '.join(zip_files)}.")
                return None
            else:
                return None
    except zipfile.BadZipFile:
        return None
    
    
def validate_zip(file_path: Path | None) -> Path | None:
    """
    Validates that a file path points to a valid zip file. Optionally prompts the user to select a file if the provided path is invalid.

    Args:
        file_path (Path): The path to the zip file.
    Returns:
        bool: True if the file path is valid, False otherwise.
    """
    if file_path is not None:
        if file_path.is_file() and file_path.suffix.lower() == '.zip' and file_path.exists():
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    return file_path
            except zipfile.BadZipFile:
                return None
    return None


def extract_zip(zip_file_path: Path | None, ask_prompt: bool = False) -> None:
    """
    Extracts a file to a folder with the same name as the zip file.
    
    Args:
    
        zip_file_path (Path): The path to the zip file.
        ask_prompt (bool): Whether to ask the user to select a file if the provided file path is invalid. Defaults to False.
    
    Raises:
        FileNotFoundError: If the zip file is not valid and ask_prompt is False.
    """
    if validate_zip(zip_file_path) is None:
        if ask_prompt:
            select_path = None
            while select_path is None:
                select_path = filedialog.askopenfilename(filetypes =[('ZIP', '*.zip')], title = "Select ZIP File")
                if not select_path:
                    print("Error, please select a valid ZIP file.")
                else:
                    zip_file_path = Path(select_path)
        else:
            raise FileNotFoundError(f"Error: {zip_file_path} is not a valid zip file, or does not exist.")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        folder_name = zip_file_path.with_suffix("")
        folder_name.mkdir(parents=True, exist_ok=True)
        zip_ref.extractall(folder_name)


def create_zip(zip_file_path: Path, directory_path: Path, overwrite: bool = False) -> None:
    """
    Creates a zip file from a directory.

    Args:
        zip_file_path (Path): The path to the target zip file.
        directory_path (Path): The path to the directory to zip.
        overwrite (bool, optional): Whether to overwrite the zip file if it already exists. Defaults to False.
    """
    if validate_zip(zip_file_path) is not None:
        if not overwrite:
            raise FileExistsError(f"Error: {zip_file_path} already exists.")
        else:
            zip_file_path.unlink()
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = Path(root).joinpath(file)
                zipf.write(file_path, file_path.relative_to(directory_path))


def set_wx_control_props(control, foreground_color: wx.Colour | None = None, background_color: wx.Colour | None = None) -> None:
    """
    Customizes the select wxPython control's properties.
    
    Args:
        control: A wxPython control object (e.g., wx.Button, wx.TextCtrl, wx.RadioButton, wx.CheckBox)
        foreground_color (wx.Colour | None): The foreground (text) color.
                                        If None, the foreground color is not changed.
        background_color (wx.Colour | None): The background color.
                                        If None, the background color is not changed.
    """
    try:
        if not isinstance(control, wx.Window):
            raise TypeError(f"Control must be a wx.Window instance, got {type(control)}")
        if foreground_color is not None:
            control.SetForegroundColour(foreground_color)
        if background_color is not None:
            control.SetBackgroundColour(background_color)
        control.Refresh() 
    except ImportError:
        raise ImportError("wxPython (wx) is not installed. Install it with: pip install wxPython")
    except Exception as e:
        raise RuntimeError(f"Error setting control colors: {str(e)}")


def get_wx_controls_by_type(parent, control_type: WxControlType) -> List[WxControl]:
    """
    Recursively finds all wxPython controls of a specified type within a parent container.
    
    Args:
        parent: A wxPython parent container (e.g., wx.Panel, wx.Frame)
        control_type: The type of control to find.
    
    Returns:
        List[WxControlType]: A list of all matching control objects found within the parent container.
    """
    try:
        controls = []
        has_children = hasattr(parent, 'GetChildren') and callable(getattr(parent, 'GetChildren')) and len(parent.GetChildren()) > 0
        if not has_children:
            return controls
        for child in parent.GetChildren():
            if isinstance(child, control_type):
                controls.append(child)
            has_children = hasattr(child, 'GetChildren') and callable(getattr(child, 'GetChildren')) and len(child.GetChildren()) > 0
            if has_children:
                controls.extend(get_wx_controls_by_type(child, control_type))
        return controls
    except ImportError:
        raise ImportError("wxPython (wx) is not installed. Install it with: pip install wxPython")
    except Exception as e:
        raise RuntimeError(f"Error finding controls: {str(e)}")


def get_gooey_window() -> wx.Window | None:
    """
    Retrieves the current wx.Window (frame) from a running Gooey application.
    
    Returns:
        wx.Window | None: The current Gooey window, or None if no Gooey application is running.
    """
    try:
        app = wx.GetApp()
        if app is None:
            return None
        window = wx.App.GetTopWindow(app)
        if window is None:
            return None
        return window
    except ImportError:
        raise ImportError("wxPython (wx) is not installed. Install it with: pip install wxPython")
    except Exception as e:
        raise RuntimeError(f"Error getting Gooey window: {str(e)}")


def customize_gooey_window_async(timeout: float = 3.0, customization_callback: Callable | None = None, get_theme_func: Callable | None = None) -> None:
    """
    Waits for the Gooey window to appear and customizes it in a background thread.
    
    Args:
        timeout (float): Maximum time to wait for the window to appear (in seconds). Defaults to 30.
        customization_callback (callable): A function that takes the Gooey window as an argument
                                          and customizes it. If None, no customization is performed.
        get_theme_func (callable): A function that returns theme customizations based on a node-key pairing.
    """
    try:
        start_time = time.time()
        gooey_window = None
        while gooey_window is None and (time.time() - start_time) < timeout:
            gooey_window = get_gooey_window()
            if gooey_window is None:
                time.sleep(0.01)

        if gooey_window is None:
            print(f"Timeout: Gooey window did not appear within {timeout} seconds.")
            return
        
        time.sleep(0.60)  # Allow time for the window to fully initialize, if is too short will cause a segfault
    
        if customization_callback is not None and callable(customization_callback):
            customization_callback(gooey_window, get_theme_func)
        
    except Exception as e:
        print(f"Error customizing Gooey window: {str(e)}")
        

def customize_gooey_window(gooey_window: wx.Window, theme_color_func: Callable | None = None) -> None:
    try:
        if theme_color_func is None:
            raise ValueError("theme_color_func must be provided")
        if getattr(theme_color_func, '__call__', None) is None:
            raise ValueError("theme_color_func must be a callable function")
        
        for control_type in [ wx.Button, wx.TextCtrl, wx.RadioButton, wx.CheckBox, wx.StaticText,
                     wx.Choice, wx.ListBox, wx.ComboBox, wx.SpinCtrl, wx.Slider ]:
            wx_controls = get_wx_controls_by_type(gooey_window, control_type)
            for control in wx_controls:
                font_color = theme_color_func(control_type, "font_color")
                bg_color = theme_color_func(control_type, "bg_color")
                set_wx_control_props(control, foreground_color=font_color, background_color=bg_color)

    except Exception as e:
        import traceback
        print(f"Error during window customization: {str(e)}")
        traceback.print_exc()
