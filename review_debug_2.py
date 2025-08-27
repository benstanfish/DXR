from drchecks_reviews import Review
from utils import timestamp
import pandas as pd
import numpy as np

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments

expansion_type = 'type'
all_list, rows = review_comments.get_all_comments_and_responses(expansion_type=expansion_type)
header_list, columns = review_comments.get_all_comments_and_response_headers(expansion_type=expansion_type)

# df = pd.DataFrame(all_list, columns=header_list)
# df.to_excel(f'all_output_{expansion_type}_{timestamp()}.xlsx', index=False)


# df2 = pd.DataFrame(project_info.get_info)
# print(df2)

# a_comment = review_comments.comments[1]
# print(a_comment.latest_response.remark_type)
# print(a_comment.ball_in_court)

# for comment in review_comments.comments:
#     print(comment.id, comment.ball_in_court)

print(rows, columns)

np_list = np.array(all_list)
print(np_list.shape)