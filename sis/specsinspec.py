# Copyright (c) 2025 Ben Fisher
""" 
XXX

It includes functions for:
- XXX

Example usage:
    >>> XXX
"""
import os
from pathlib import Path

from .src.process.clean0x81 import clean_files
from .src.process.sectohtml import make_html_from_sec
from .src.process.createhtmltoc import create_error_html, create_index

# sec_folder = './specs/sec'

def create_html_reports(folder_path:str) -> None:
    source_basename = os.path.basename(folder_path)
    parent_folder = Path(folder_path).parent.resolve()
    html_folder = os.path.join(parent_folder, 'html')

    if not os.path.exists(html_folder):
        os.mkdir(html_folder)

    temp_sec_path = os.path.join(parent_folder, f'temp_{source_basename}')
    if not os.path.exists(temp_sec_path):
        os.mkdir(temp_sec_path)

    processed_sec_files = clean_files(orig_dir=os.path.abspath(folder_path), temp_dir=temp_sec_path, file_type='.sec')
    cleaned_sec_files = [file for file in os.listdir(temp_sec_path) if Path(file).suffix == '.sec']
    
    all_file_data = []
    files_with_0x81 = [key for (key, values) in processed_sec_files.items() if values['has_0x81'] == True]
    error_files = {}

    for sec_file in cleaned_sec_files:
        try:
            html_file = make_html_from_sec(os.path.join(temp_sec_path, sec_file), output_path=html_folder)
            all_file_data.append(html_file)
        except Exception as e:
            error_files[sec_file] = f'{e}'

    with open(os.path.join(html_folder, 'errors.txt'), 'w') as file:
        if len(error_files) > 0:
            file.write(f'<h2>Files not processed due to errors in the files</h2>')
            file.write(f'<div class="error-row"><div class="error-section">Section</div><div class="error-section">Error</div></div>')
            file.write(f'<br />')
            for key, value in error_files.items():
                file.write(f'<div class="error-row"><div class="error-section">{key}</div><div class="error-value">{value}</div></div>')
            file.write(f'<br />')
        if files_with_0x81:
            file.write(f'<h2>Files with 0x81 Character</h2>')
            file.write(f'<p>The following original .sec files contain a 0x81 character (non-printing character) that needs to be cleaned. Temporary versions were processed into a temp folder.</p>')
            file.write(f'')
            file.write(f'<ul style="columns: 3">')
            for file_name in files_with_0x81:
                file.write(f'<li style="font-weight: bold;">{file_name}</li>')
            file.write(f'</ul>')

    create_error_html(html_folder)
    create_index(html_folder)

# create_html_reports(sec_folder)