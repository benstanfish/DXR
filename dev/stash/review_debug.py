from DXBuild.DXReviewComponents import Review
import DXutils
from DXutils import _NL as NL
import pandas as pd

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments


# for comment in review_comments.comments:
#     print(utils._BOLD + utils._RED + comment.id + utils._RESET, 
#           utils._BOLD + utils._GREEN + comment.author + utils._RESET, 
#           NL + comment.text + NL)

a_comment = review_comments.comments[0]

# attrs_keys = {
#     'ID': 'id',
#     'Status': 'status',
#     'Discipline': 'discipline',
#     'Author': 'author',
#     'Email': 'email',
#     'Date': 'date_created',
#     'Comment': 'text',
#     'Critical': 'is_critical',
#     'Class': 'classification',
#     'Att': 'has_attachment',
#     'Days Open': 'days_open'
# }

# attrs = ['id', 'author', 'date_created', 'text', 'is_critical', 'days_open']
# my_list = a_comment.to_list(attrs)
# my_list = a_comment.to_list(COMMENT_COLUMNS)

# print(my_list)

# my_data = []
# for comment in review_comments.comments:
#     my_data.append(comment.to_list(_COMMENT_COLUMNS))

review_comments_list = review_comments.comments_list
# column_names = [key for key in COMMENT_COLUMNS.keys()]
column_names = review_comments.column_names

df = pd.DataFrame(review_comments_list, columns=column_names)
print(df)
df.to_excel('output.xlsx', index=False)

# print(a_comment.days_open)