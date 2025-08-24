from drchecks_reviews import Review
import pandas as pd

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments.to_list
column_names = review.review_comments.column_names

a_comment = review.review_comments.comments[0]
print(a_comment.highest_response)
print(a_comment.highest_evaluation_response)
print(a_comment.highest_backcheck_response)


# df = pd.DataFrame(review_comments, columns=column_names)
# df.to_excel('output.xlsx', index=False)
