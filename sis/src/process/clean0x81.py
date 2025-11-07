# Copyright (c) 2025 Ben Fisher
""" 
This module provides utilities for inspecting and cleaning files that contain 
non-printing 0x81 byte characters, which interfer with Python libraries used to
process XML, text and other files.

It includes functions for:
- Safely evaluate if a file contains 0x81 bytes
- Remove 0x81 bytes from files and overwrite existing or copy to new file
- Batch processing files in a given directory

Example usage:
    >>> import clean0x81
    >>> clean0x81.get_0x81_file_list('path/to/dir', '.xml')
    'Report written to: path/to/dir/files_with_0x81.txt'

    >>> clean0x81.clean_0x81_files('path/do/dir', 'path/do/new_dir', '.sec')
"""

__all__ = ['get_0x81_file_list', 'clean_files']

import os, shutil
from pathlib import Path
from ..escapes.escapes import Escapes





def test_file_for_0x81(file_path: str) -> bool:
    """Determine if the file contains occurances of the 0x81 character.

    Args:
        file_path (str): Path to .xml, .sec or other file.

    Returns:
        bool: True if file contains 0x81.
    """
    try: 
        with open(file_path, 'r') as file:
            content = file.read()
        return False
    except:
        return True



def clean_file(file_path: str, 
                    new_path: str='') -> None:
    """Replaces the 0x81 byte (all occurances) and saves to file.

    Args:
        file_path (str): Path to .xml, .sec or other file.
        new_path (str, optional): Write to new_path if provided, else overwrite existing. Defaults to overwrite.
    """
    find_text = b'\x81'
    replace_text = b''
    with open(file_path, 'rb') as file:
        content = file.read()
    content = content.replace(find_text, replace_text)
    try:
        if new_path:
            with open(new_path, 'wb') as file:
                file.write(content)
        else:
            with open(file_path, 'wb') as file:
                file.write(content)
    except Exception as e:
        # print(f'An error occured when trying to write the file to {'new file' if new_path else 'existing path'}: {e}')
        pass
    # print(f'Cleaned file written {'new file' if new_path else 'existing path'}: {new_path if new_path else file_path}')




def get_file_dict(parent_dir: str, 
                  extension: str='.sec') -> dict:
    """Creates dictionary of file stems and absolute paths that match the file extension condition.

    Args:
        parent_dir (str, optional): Path to directory (parent) of files to be included. Defaults to r'./specs/sec'.
        extension (str, optional): File extension to be matched; case-insensitive. Defaults to '.sec' (a type of .xml).

    Returns:
        dict: Dictionary with keys = file name stem and value = absolute path to file.
    """
    file_list = [os.path.abspath(os.path.join(parent_dir, file)) for \
                file in os.listdir(parent_dir) \
                    if Path(file).suffix.lower() == extension]
    return {Path(file_path).stem: file_path for file_path in file_list}




def test_files_for_0x81(file_dict: dict) -> bool:
    """Loops through files in dictionary to test if each file has 0x81 character and prints color-coded results to console.

    Args:
        file_dict (dict): Dictionary with key = file stem, value = absolute path.
    
    Returns:
        bool: Result of all parsed files in supplied file dictionary.
    """
    dir_has_0x81 = False
    print('='*75)
    for file_stem, path in file_dict.items():
        file_with_0x81 = test_file_for_0x81(path)
        if file_with_0x81:
            dir_has_0x81 = file_with_0x81
        print(f'{file_stem}: {Escapes.Red + Escapes.Bold if file_with_0x81 \
                         else Escapes.Green}{file_with_0x81}{Escapes.Reset}')
    print('-'*75)
    print(f'File dictionary {Escapes.Red + Escapes.Bold + 'has' if dir_has_0x81 \
                       else Escapes.Green + 'does not'}{Escapes.Reset} files with 0x81 character.\n')
    return dir_has_0x81





def get_0x81_file_list(parent_dir: str=r'../../specs/sec', 
                       extension: str='.sec') -> None:
    """Write list of files in directory that contain 0x81 character(s) to text file in same directory.

    Args:
        parent_dir (str, optional): Path of directory to be evaluated. Defaults to r'./specs/sec'.
        extension (str, optional): File extension to be matched; case-insensitive. Defaults to '.sec' (a type of .xml).
    """
    file_dict = get_file_dict(parent_dir=parent_dir, extension=extension)
    has_list = []
    for file_stem, path in file_dict.items():
        if test_file_for_0x81(path):
            has_list.append(Path(path).name)
    report_path = os.path.join(parent_dir, 'files_with_0x81.txt')
    try:
        with open(report_path, 'w') as file:
            if has_list:
                file.write(f'The following {len(has_list)} files include 0x81 byte characters and need to be cleaned before processing:\n\n')
                for item in has_list:
                    file.write(item + '\n')
        print(f'Report written to: {report_path}')
    except Exception as e:
        print(f'An exception occurred when trying to write the report: {e}')





def clean_files(orig_dir: str, temp_dir: str, file_type: str='.sec') -> dict:
    """Clean all files in a specified directory, copying to new temp directory.

    Args:
        orig_dir (str): _description_
        file_type (str, optional): _description_. Defaults to '.sec'.

    Returns:
        dict: _description_
    """
    
    target_files = get_file_dict(orig_dir, file_type)
    
    if not os.path.exists(temp_dir):
        os.mkdir(os.path.abspath(temp_dir))

    processed_files_dict = {}

    for section, path in target_files.items():
        new_path = os.path.join(os.path.abspath(temp_dir), section + file_type)
        if test_file_for_0x81(path):
            clean_file(path, new_path)
            processed_files_dict[section] = {
                'path': path,
                'temp': new_path,
                'has_0x81': True
            }
        else:
            shutil.copy(path, new_path)
            processed_files_dict[section] = {
                'path': path,
                'temp': new_path,
                'has_0x81': False
            }

    return processed_files_dict

