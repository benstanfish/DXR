# Copyright (c) 2018-2025 Ben Fisher

from typing import Literal

"""The following constants are not intended for public access. They
relate to the parsing and internal workings of this script."""
_PROJECT_INFO_INDEX = 0
_COMMENTS_INDEX = 1
_PROJECT_INFO_VERTICAL_OFFSET = 2
_RESPONSE_EXPANSION_TYPES = Literal['chronological', 'type']
_TRUE_SYMBOLIC = '〇'

"""
COMMENT_COLUMNS and RESPONSE_COLUMNS are dictionaries where the key
is the name used in an Excel column, while the values are the property
names of the respective Classes. If the value = '' it is because the
it is not a property of the Comment or Response classes and is added
by alternative processes. These are the default dictionaries, but
alternatives can be provided in the arguments of the calling functions;
it's recommended to provide different dictionaries, rather than overwrite
these defaults.
"""

COMMENT_COLUMNS = {
    'ID': 'id',
    'Status': 'status',
    'Discipline': 'discipline',
    'Author': 'author',
    'Email': 'email',
    'Date': 'date_created',
    'Source': '',
    'Reference': '',
    'Sheet': '',
    'Spec': '',
    'Section': '',
    'Comment': 'text',
    'Critical': 'is_critical',
    'Class': 'classification',
    'Att': 'has_attachment',
    'Days Open': 'days_open',
    # 'Ball in Court': 'ball_in_court',
    'Highest Resp.': 'highest_response'
}

RESPONSE_COLUMNS = {
    'Status': 'status',
    'Author': 'author',
    'Email': 'email',
    'Date': 'date_created',
    'Text': 'text',
    'Att': 'has_attachment'
}

USER_NOTES_COLUMNS = ['No.', 
                      'Notes', 
                      'Action Items', 
                      'Action Assignee', 
                      'Proposed Response', 
                      'Proposed State', 
                      'State']

"""
RESPONSE_VALUES is a dictionary with the response strings from Dr Checks,
and the values are the ranking. The larger the number, the more weight it
is given in the highest_response() logical. This dictionary is the default,
but alternative can be provided in the function's arguments. It's recommended
to provide different dictionaries, rather than overwrite this default.
"""
RESPONSE_VALUES = {
    'concur': 1,
    'for information only': 2,
    'non-concur': 3,
    'check and resolve': 4
}

FALLBACKS = {
    'font_name': 'Aptos',
    'font_size': 10,
    'font_bold': False
}