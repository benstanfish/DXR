# Copyright 2025, Ben Fisher
"""This module parses a python script to extract signatures."""

import re, os

dev_folder = './dev'
file_path = './dxbuild/dxreview.py'

output_name = os.path.splitext(os.path.basename(file_path))[0] + '_defs.txt'
output_path = os.path.join(os.path.abspath(dev_folder), output_name)

signature_pattern = r'^(\s*)\b(def\s\w*|class\s\w*|super\(\)\.__init__).*\n'
defintions_list = []

with open(file_path, 'r', encoding='utf-8') as file:
    for line_no, line in enumerate(file, 1):
        signature_match = re.search(signature_pattern, line)
        if signature_match:
            defintions_list.append(signature_match[1] + signature_match[2])
            
with open(output_path, 'w') as file:
    header_line = f'This file contains signatures extracted from {os.path.basename(file_path)}\n'
    file.write(header_line)
    file.write('='*(len(header_line)-1))
    file.write('\n')
    file.write('\n')
    for definition in defintions_list:
        file.write(definition + '\n')