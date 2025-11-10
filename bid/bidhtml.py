# Copyright (c) 2018-2025 Ben Fisher

import re, html
from bs4 import BeautifulSoup, element

file_path = './dev/html/ProjNet_ Logged In User.html'




def get_inner_html(element: element.Tag) -> str:
    """Get the inner-html of a html element from BeautifulSoup soup object."""
    return element.decode_contents()

def cleanse_string(base_string:str) -> str:
    """Returns processed 'inner html' string that does the following:
        1. removes extra spaces
        2. removes initial and final spaces
        3. remove NBSP characters
        3. removes line-feed characters
        4. converts <br/> to new line characters - this is intentional
        5. converts html entities back to human-readable characters
    """
    return html.unescape(re.sub(r' +', ' ', base_string).strip().replace('\xa0', ' ').replace('\n', ' ').replace('<br/>', '\n'))

# def comment_dict_to_list(comment_dict: dict) -> list:
#     temp = []
#     for key, item in comment_dict:


def read_bid_html_to_list(html_path:str) -> list:

    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    except FileNotFoundError:
        print(f"Error: The file '{html_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    project_header = soup.find(class_='reportSubHeader').get_text(strip=True)
    project_title = project_header.split('Review:')[0].replace('Project: ', '').strip()

    raw_tds = soup.find_all('td')

    id_pattern = r'^\d{6,8}$'

    comment_ids = [td.text for td in raw_tds if re.match(id_pattern, td.text)]
    comment_text = [cleanse_string(get_inner_html(comment)) for comment in soup.find_all(class_='report_comment')]
    comment_discipline = [td.next_sibling.next_sibling for td in raw_tds if re.match(id_pattern, td.text)]
    comment_sheet = [td.next_sibling.next_sibling.next_sibling.next_sibling for td in raw_tds if re.match(id_pattern, td.text)]
    comment_detail = [td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling for td in raw_tds if re.match(id_pattern, td.text)]
    comment_spec = [td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling for td in raw_tds if re.match(id_pattern, td.text)]
    comment_class = [comment.text.replace('Comment Classification: ', '') for comment in soup.find_all(class_='commentClassification')]

    comments_dict = {}
    for comment_id, comment, discipline, sheet, detail, spec, classification in zip(comment_ids, 
                                                                                    comment_text, 
                                                                                    comment_discipline, 
                                                                                    comment_sheet, 
                                                                                    comment_detail, 
                                                                                    comment_spec, 
                                                                                    comment_class):
        comments_dict[comment_id] = {
            'comment': comment,
            'discipline': cleanse_string(get_inner_html(discipline)),
            'sheet': cleanse_string(get_inner_html(sheet)),
            'detail': cleanse_string(get_inner_html(detail)),
            'spec': cleanse_string(get_inner_html(spec)),
            'classification': classification
        }

    comment_list = []
    for key, item in comments_dict.items():
        comment_list.append([key, item['comment'], item['discipline'], item['sheet'], item['detail'], item['spec'], item['classification']])

    return comment_list


