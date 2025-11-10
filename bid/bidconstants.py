# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime

def list_to_string(a_list:list, in_quotes:bool=True, delimiter:str=', ') -> str:
    if in_quotes:
        return f'"{delimiter.join(a_list)}"'
    else:
        return delimiter.join(a_list)

def timestamp(
        format_string: str=r'%Y%m%d_%H%M%S'
    ) -> str:
    """Returns a formatted timestamp of the current time.

    :param format_string: format string provided in accordance with https://docs.python.org/3/library/datetime.html#format-codes, defaults to r'%Y%m%d_%H%M%S'
    :type format_string: str, optional
    :return: current time as a timestamp string.
    :rtype: str
    """
    # """Returns a timestamp, default format: YYYYMMDD_HHMMSS"""
    return datetime.now().strftime(format_string)



FALLBACKS = {
    'font_name': 'Aptos Narrow',
    'font_size': 11,
    'font_bold': False
}



BALL_IN_COURT_FIELDS = [
    'TL',
    'TS',
    'PM',
    'CT',
    'OT',
    'AE'
    ]


BID_TABLE_HEADERS = [
    'Item No',
    'Comment ID',
    'Discipline',
    'Sheet',
    'Detail',
    'Spec',
    'Comment Text',
    # 'Comment Classification',
    'Assigned Discipline',
    'Assigned Party',
    'Ball in Court',
    'Response Discussions',
    'Preliminary Response',
    'Amend Required',
    'Amend No',
    'Engineering Final Response',
    'TL QA Reviewed',
    'Tech Services Final Response',
    'Contracting Response',
    'Engineering Response to Contracting',
    'OC Response',
    'Engineering Response to OC',
    'JED LL Capture'
    ]

DISCIPLINE_LIST = ['Installation', 
                   'Civil', 
                   'Geotech', 
                   'Environmental', 
                   'Architecture', 
                   'Structural', 
                   'Mechanical', 
                   'Plumbing', 
                   'Fire Protection/Life Safety', 
                   'Electrical', 
                   'Comm', 
                   'Cyber', 
                   'Contracting', 
                   'Specs', 
                   'Other']

ASSIGNED_PARTY_LIST = ['AE(DBB)', 
                       'Contracting', 
                       'TL', 
                       'PM', 
                       'SME', 
                       'MCX',
                       'TCX/COS',
                       'PDT(DB)']

