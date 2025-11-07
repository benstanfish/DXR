# Copyright (c) 2025 Ben Fisher
""" 
This module provides utilities parsing an .sec file (a type of .xml file) into an
.html file for review outside SpecsIntact.

It includes functions for:
- XXX

Example usage:
    >>> XXX
"""

import os, shutil, re
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element

import minify_html

def get_timestamp(as_day:bool=False) -> str:
    if as_day:
        return datetime.now().strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def remove_declaration(xml_string: str) -> str:
    declaration_pattern = r'<\?xml[^>]*\?>'
    return re.sub(declaration_pattern, '', xml_string, count=1).strip()

def clean_sec_string(xml_string:str, 
                     spaces_reduced:bool=True, 
                     brk_replaced:bool=True, 
                     ast_removed:bool=False, 
                     ast_character:str='*', 
                     ast_count:int=100) -> str:
    temp = remove_declaration(xml_string)
    if spaces_reduced:
        temp = re.sub(' +', ' ', temp)
    temp = re.sub(r'<BRK />\s+?<BRK />', '<BRK />', temp)
    if brk_replaced:
        temp = re.sub('<BRK />', '<br/>', temp)
    if not ast_removed:
        # temp = temp.replace('<AST />', f"<AST>{ast_character * ast_count}</AST>")
        temp = temp.replace('<AST />', f'<AST><hr></AST>')
    else:
        temp = temp.replaced('<AST />', '')
    return temp

def get_all_tags(file_path:str) -> list:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        raw_tags = []
        raw_tags.append(root.tag)
        for elem in root.iter():
            if elem.tag not in raw_tags:
                raw_tags.append(elem.tag)
        sorted_tags = sorted(raw_tags)
        return sorted_tags
    except Exception as e:
        print(f'An exception occurred: {e}')
    return []

def add_display_tags(tag_name: str, all_text: str) -> str:
    start_tag = f'<{tag_name}>'
    end_tag = f'</{tag_name}>'
    new_start_tag = f'<{tag_name}><pre class="display_{tag_name}">&lt;{tag_name}&gt;</pre>'
    new_end_tag = f'<pre class="display_{tag_name}">&lt;/{tag_name.upper()}&gt;</pre></{tag_name}>'
    temp = all_text.replace(end_tag, new_end_tag)
    temp = temp.replace(start_tag, new_start_tag)
    return temp

def add_display_tags_to_soup(parent_tag, prefix, suffix, soup_element:BeautifulSoup):
    parent_tags = soup_element.find_all(parent_tag)
    for parent_tag in parent_tags:
        parent_tags.append()
    pass

def wrap_brackets_in_span(html_string:str) -> str:
    temp = html_string.replace(r'[', r'<div class="brackets">[')
    return temp.replace(r']', r']</div>')

def number_sections_recursively(element:Element, prefix:str='', attrib_name:str='outline'):
    """Recursively add outline number to PRT and SPT tags in XML file.

    Args:
        element (Element): _description_
        prefix (str, optional): _description_. Defaults to ''.
        attrib_name (str, optional): _description_. Defaults to 'outline'.
    """
    part_counter = 0
    current_counter = 0
    for child in element:
        if child.tag == 'PRT':
            part_counter += 1
            child.set(attrib_name, f'{part_counter}')
            number_sections_recursively(child, prefix=f'{part_counter}.')
        elif child.tag == 'SPT':
            current_counter += 1
            child.set(attrib_name, f'{prefix}{current_counter}')
            number_sections_recursively(child, prefix=f'{prefix}{current_counter}.')

def update_html_outline(soup: BeautifulSoup) -> BeautifulSoup:
    for element in soup.find_all():
        if 'outline' in element.attrs and element.name == 'spt':
            title_element = element.find('ttl')
            sub_element = title_element.find('sub')
            if sub_element:
                sub_element.insert_before(f'{element.attrs['outline']} ')
            else:
                title_element.string = element.attrs['outline'] + ' ' + title_element.text
    return soup

def make_subfolder(a_path:str, subfolder_name:str) -> str:
    parent_dir = os.path.abspath(os.path.dirname(a_path))
    new_path = os.path.join(parent_dir, subfolder_name)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    return new_path


def make_html_from_sec(sec_path:str, output_path:str='') -> dict:

        tree = ET.parse(sec_path)
        root = tree.getroot()

        number_sections_recursively(root)

        with open(sec_path, 'wb') as file:
            file.write(ET.tostring(root))

        try:
            _section = root.find('SCN').text.replace('SECTION ', '').strip()
        except:
            _section = Path(sec_path).stem + "---STL TAG ERROR"
        try:
            _title = root.find('STL').text.title().strip()
        except:
            _title = 'Section title not found'
        try:
            _date = root.find('DTE').text.strip()
        except:
            _date = ''

        
        section_info = {
            'section': _section,
            'title': _title,
            'date': _date,
            'run_date': get_timestamp()
        }

        with open(sec_path, 'r') as file:
            content = file.read()

        display_tags = ['ADD',
            # 'ALN',
            'AST',
            # 'BRK',
            # 'BRL',
            # 'CEL',
            # 'COL',
            'DEL',
            # 'DTA',
            'DTE',
            # 'END',
            'ENG',
            'HDR',
            'HL1',
            'HL4',
            'ITM',
            'LST',
            'MET',
            # 'MTA',
            # 'NED',
            'NPR',
            'NTE',
            'ORG',
            'PRA',
            'PRT',
            'REF',
            'RID',
            # 'ROW',
            'RTL',
            'SCN',
            'SCP',
            # 'SEC',
            'SPT',
            'SRF',
            'STL',
            # 'STS',
            # 'STY',
            'SUB',
            'TAB',
            'TAI',
            # 'TDA',
            'TST',
            # 'TTL',
            'TXT',
            'URL',
            # 'WBK'
            ]

        # display_tags = ['NTE', 'NPR', 'ENG', 'MET', 'RID', 'RTL', 'ADD', 'DEL', 'SRF', 'STL', 'SUB']
        for display_tag in display_tags:
            content = add_display_tags(tag_name=display_tag, all_text=content)
        content = wrap_brackets_in_span(content)
        content = clean_sec_string(content, brk_replaced=False)

        html_fragment = BeautifulSoup(content, 'html.parser')

        html_template = './sis/src/htmlrsx/template.html'

        if output_path:
            html_folder = output_path
        else:
            html_folder = make_subfolder(sec_path, 'html')

        html_path = os.path.join(os.path.abspath(html_folder), f"{section_info['section']}.html")
        html_file = shutil.copy(html_template, html_path)

        with open(html_file, 'r') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        soup.find('title').string = section_info['section'] + '.sec Viewer'
        soup.find('main').append(html_fragment)

        soup.find('span', class_='this_section_number').append(section_info['section'])
        soup.find('span', class_='create_date').append(get_timestamp())

        with open('./sis/src/htmlrsx/reboot.css', 'r') as file:
            css_reboot = file.read()

        with open('./sis/src/htmlrsx/style.css', 'r') as file:
            css_styles = file.read()

        with open('./sis/src/htmlrsx/scripts.js', 'r') as file:
            js_scripts = file.read()

        soup.find(id='reboot').append(css_reboot)
        soup.find(id='styles').append(css_styles)
        soup.find(id='scripts').append(js_scripts)

        soup = update_html_outline(soup)
        soup.prettify()

        mini_html = minify_html.minify(str(soup), keep_comments=False, minify_css=True, minify_js=True)

        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(mini_html)

        return section_info