COMMENT_PARAMS = [
        {
            'column_name': 'ID',
            'class_property': 'id',
            'xml_tag': 'id',
            'is_used': True,
            'sort_order': 2
        },
        {
            'column_name': 'Spec',
            'class_property': 'spec',
            'xml_tag': 'spec',
            'is_used': True,
            'sort_order': 4
        },
        {
            'column_name': 'Sheet',
            'class_property': 'sheet',
            'xml_tag': 'sheet',
            'is_used': True,
            'sort_order': 3
        },
        {
            'column_name': 'Detail',
            'class_property': 'detail',
            'xml_tag': 'detail',
            'is_used': True,
            'sort_order': 1
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        },
        {
            'column_name': '',
            'class_property': '',
            'xml_tag': '',
            'is_used': True,
            'sort_order': 999
        }
    ]

temp = [item for item in COMMENT_PARAMS if item['is_used']]
temp2 = sorted(temp, key=lambda item: item['sort_order'])

# for item in temp2:
#     print(item['column_name'])




