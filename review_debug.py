from drchecks_reviews import Review
import pandas as pd
import utils

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments.to_list
column_names = review.review_comments.column_names
comment = review.review_comments.comments[1]


#region Testing Response Counts

# print(comment.highest_response)
# print(comment.highest_evaluation_response)
# print(comment.highest_backcheck_response)

# df = pd.DataFrame(review_comments, columns=column_names)
# df.to_excel('output.xlsx', index=False)

# a_list = comment.to_list()
# df1 = pd.DataFrame(a_list, index=column_names).T # Required for a single row of data not to be treated as a column
# df1.to_excel('output2.xlsx', index=False)

# evaluations = comment.evaluations
# backchecks = comment.backchecks

# print(comment.evaluations_count, comment.backchecks_count)

# etot, btot = review.review_comments.comments[1].response_counts
# print(etot, btot)

# for evaulation in evaluations:
#     print(evaulation.to_list())

# for backcheck in backchecks:
#     print(backcheck.to_list())

# max_evals, max_bcs = review.review_comments.max_responses
# print(f'{utils._BOLD}{utils._RED}Max Evaluations{utils._RESET}: {max_evals} and ' +
#       f'{utils._BOLD}{utils._GREEN}Max Backchecks{utils._RESET}: {max_bcs}')

#endregion

#region Testing Response Counts and Listing


#endregion