from drchecks_reviews import Review
from utils import timestamp
import pandas as pd

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments

# expansion_type = 'type'
# all_list = review_comments.get_all_comments_and_responses(expansion_type=expansion_type)
# header_list = review_comments.get_all_comments_and_response_headers(expansion_type=expansion_type)

# df = pd.DataFrame(all_list, columns=header_list)
# df.to_excel(f'all_output_{expansion_type}_{timestamp()}.xlsx', index=False)


df2 = pd.DataFrame(project_info.get_info)
print(df2)



