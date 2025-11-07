# Copyright (c) 2025 Ben Fisher
"""
XXX

It includes functions for:
- XXX

Example usage:
    >>> XXX
"""

import os, shutil
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
import minify_html


def get_timestamp(as_day:bool=False) -> str:
    if as_day:
        return datetime.now().strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def create_error_html(html_dir:str) -> None:
    error_report = os.path.join(html_dir, 'errors.txt')
    if os.path.exists(error_report):

        with open(error_report, 'r') as file:
            error_content = file.read()

        error_fragment = BeautifulSoup(error_content, 'html.parser')

        html_template = './sis/src/htmlrsx/error_template.html'
        error_html_path = os.path.join(html_dir, 'Error Report.html')
        error_html_file = shutil.copy(html_template, error_html_path)

        with open(error_html_file, 'r') as file:
            error_html = file.read()

        soup = BeautifulSoup(error_html, 'html.parser')
        soup.find('div', class_='error_report').append(error_fragment)

        with open('./sis/src/htmlrsx/reboot.css', 'r') as file:
            css_reboot = file.read()

        with open('./sis/src/htmlrsx/index_style.css', 'r') as file:
            css_styles = file.read()

        with open('./sis/src/htmlrsx/scripts.js', 'r') as file:
            js_scripts = file.read()

        soup.find(id='reboot').append(css_reboot)
        soup.find(id='index_styles').append(css_styles)
        soup.find(id='scripts').append(js_scripts)

        mini_html = minify_html.minify(str(soup), keep_comments=False, minify_css=True, minify_js=True)

        with open(error_html_file, 'w') as file:
            file.write(mini_html)





def create_index(html_dir:str) -> None:
    # html_dir = './specs/html'
    html_files = []
    for file_name in os.listdir(html_dir):
        if Path(file_name).suffix == '.html':
            html_files.append(file_name)

    html_template = './sis/src/htmlrsx/index_template.html'
    index_path = os.path.join(html_dir, 'index.html')
    index_file = shutil.copy(html_template, index_path)

    with open(index_file, 'r') as file:
        index_content = file.read()

    soup = BeautifulSoup(index_content, 'html.parser')
    soup.find('span', class_='create_date').append(get_timestamp())

    # sec_dir = soup.find('a', class_='sec_dir')
    # sec_dir.append('Folder with original .sec files')
    # sec_dir['href'] = ''
    # sec_dir['target'] = '_blank'

    # html_dir = soup.find('a', class_='html_dir')
    # html_dir.append('Folder with new .html reports')
    # html_dir['href'] = ''
    # html_dir['target'] = '_blank'

    page_list = soup.find('ol', class_='page_list')

    for file in html_files:
        if file != 'index.html':
            new_li = soup.new_tag('li')
            page_list.append(new_li)

            new_anchor = soup.new_tag('a')
            new_anchor.append(Path(file).stem)
            new_anchor['href'] = file
            new_anchor['target'] = '_blank'
            new_li.append(new_anchor)

    with open('./sis/src/htmlrsx/reboot.css', 'r') as file:
        css_reboot = file.read()

    with open('./sis/src/htmlrsx/index_style.css', 'r') as file:
        css_styles = file.read()

    with open('./sis/src/htmlrsx/scripts.js', 'r') as file:
        js_scripts = file.read()

    soup.find(id='reboot').append(css_reboot)
    soup.find(id='index_styles').append(css_styles)
    soup.find(id='scripts').append(js_scripts)

    mini_html = minify_html.minify(str(soup), keep_comments=False, minify_css=True, minify_js=True)

    with open(index_file, 'w') as file:
        file.write(mini_html)