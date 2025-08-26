from drchecks_reviews import (
    Review, 
    ReviewComments, 
    _COMMENT_COLUMNS, 
    _RESPONSE_COLUMNS, 
    get_all_comments_and_responses,
    get_all_comments_and_response_headers
)
import pandas as pd
import utils

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments
column_names = review_comments.column_names
comment = review_comments.comments[1]


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

fields_counts = len(_RESPONSE_COLUMNS)
# print(fields_counts)

# Print out the fields to test and see how it works

def print_response_fields(resp, attrs=_RESPONSE_COLUMNS):
    for value, key in zip(resp, attrs.keys()):
        print(utils._BOLD + utils._BLUE + key + utils._RESET, value)

# test_resp = comment.evaluations[0].to_list(_RESPONSE_COLUMNS)
# print_response_fields(test_resp)

# for evaluation in comment.evaluations:
#     print_response_fields(evaluation.to_list())
#     print()

# for backcheck in comment.backchecks:
#     print_response_fields(backcheck.to_list())
#     print()

# max_evals, max_bcs = review.review_comments.max_responses
# print(max_evals, max_bcs)

# c_max_evals, c_max_bcs = comment.total_responses
# print(c_max_evals, c_max_bcs)

# for evaluation in comment.evaluations:
#     print(evaluation.to_list())

# for i in range(max_evals):
#     if i == comment.evaluations_count:
#         print(i, ['']*len(_RESPONSE_COLUMNS))
#     else:
#         print(i, comment.evaluations[i].to_list())

# def padded_evaluations(comment,
#                        review_max_evaluations,
#                        response_columns=_RESPONSE_COLUMNS):
#     padded_list = []
#     if comment.evaluations_count > 0:
#         for i in range(int(review_max_evaluations)):
#             if i == comment.evaluations_count:
#                 padded_list += ['']*len(response_columns)
#             elif comment.evaluations[i] is not None:
#                 padded_list += comment.evaluations[i].to_list(response_columns)
#         return padded_list

# def padded_backchecks(comment,
#                       review_max_backchecks,
#                       response_columns=_RESPONSE_COLUMNS):
#     padded_list = []
#     for i in range(review_max_backchecks):
#         if i == comment.backchecks_count:
#             padded_list += ['']*len(response_columns)
#         else:
#             padded_list += comment.backchecks[i].to_list(response_columns)
#     return padded_list

# padded_evals_list = padded_evaluations(comment, max_evals)
# print(padded_evals_list)

# # padded_bc_list = padded_backchecks(comment, max_bcs)
# # print(padded_bc_list)

# # padded_list = padded_evals_list + padded_bc_list
# # print(padded_list)

# def padded_responses(comment, 
#                      max_responses_tuple,
#                      response_columns=_RESPONSE_COLUMNS):
#     max_evals, max_bcs = max_responses_tuple
#     return padded_evaluations(comment, max_evals) + padded_backchecks(comment, max_bcs)

# full_responses_list = []
# for comment in review.review_comments.comments:
#     full_responses_list.append(padded_evaluations(comment, max_evals))
#     # print(padded_evaluations(comment, 3))
#     # print(padded_evaluations(comment, max_evals))
#     pass
# # print(type(review.review_comments.comments[0]))



# print(full_responses_list)

#endregion

#region New Testing Response Counts

# print(type(review))
# print(type(review_comments))
# print(type(review_comments.comments))

# print(review_comments.max_evaluations)
# print(review_comments.max_backchecks)
# print(review_comments.max_responses)

# for comment in review_comments.comments:
#     print(comment.id, comment.evaluations_count, 
#           review_comments.max_evaluations, 
#           comment.evaluations_count == review_comments.max_evaluations)

# all_responses = []
# max_eval_count, max_bc_count = review_comments.max_responses

# for comment in review_comments.comments:
#     temp = []
#     temp += comment.to_list(_COMMENT_COLUMNS)
#     for evaluation in comment.evaluations:
#         temp += evaluation.to_list(_RESPONSE_COLUMNS)
#     diff_eval = max_eval_count - comment.evaluations_count
#     for i in range(diff_eval):
#         temp += ['']*len(_RESPONSE_COLUMNS)
#     for backcheck in comment.backchecks:
#         temp += backcheck.to_list(_RESPONSE_COLUMNS)
#     diff_bc = max_bc_count - comment.backchecks_count
#     for j in range(diff_bc):
#         temp += ['']*len(_RESPONSE_COLUMNS)
#     all_responses.append(temp)





# def get_all(review_comments: ReviewComments, 
#             comment_attrs=_COMMENT_COLUMNS,
#             response_attrs=_RESPONSE_COLUMNS):
#     """Returns the full List of comments and corresponding responses."""
#     all_responses = []
#     max_eval_count, max_bc_count = review_comments.max_responses

#     for comment in review_comments.comments:
#         temp = []
#         temp += comment.to_list(_COMMENT_COLUMNS)
#         for evaluation in comment.evaluations:
#             temp += evaluation.to_list(_RESPONSE_COLUMNS)
#         diff_eval = max_eval_count - comment.evaluations_count
#         for i in range(diff_eval):
#             temp += ['']*len(_RESPONSE_COLUMNS)
#         for backcheck in comment.backchecks:
#             temp += backcheck.to_list(_RESPONSE_COLUMNS)
#         diff_bc = max_bc_count - comment.backchecks_count
#         for j in range(diff_bc):
#             temp += ['']*len(_RESPONSE_COLUMNS)
#         all_responses.append(temp)
    
#     return all_responses

# all_responses = get_all(review.review_comments)

# df_all = pd.DataFrame(all_responses)
# df_all.to_excel('all_output3.xlsx')


#endregion

#region Expand Column Headers

# evals = 3
# bcs = 2

# for key in _RESPONSE_COLUMNS.keys():
#     print(key, _RESPONSE_COLUMNS[key])

# header = []
# for i in range(evals):
#     for key in _RESPONSE_COLUMNS.keys():
#         header.append(f'Resp {key} {i + 1}')

# for item in header:
#     print(item)



# def expand_response_headers(review_comments: ReviewComments, 
#                             expansion_type='chronological',
#                             attrs=_RESPONSE_COLUMNS):
#     max_evals, max_bcs = review_comments.max_responses
#     header = []
#     if expansion_type.lower() != 'chronological':
#         for i in range(max_evals):
#             for key in attrs.keys():
#                 header.append(f'Eval {i + 1} {key}')
#         for j in range(max_bcs):
#             for key in attrs.keys():
#                 header.append(f'BCheck {j + 1} {key}')
#     else:
#         for k in range(max_evals + max_bcs):
#             for key in attrs.keys():
#                 header.append(f'Resp {k + 1} {key}')
#     return (header, expansion_type)

# header_list = expand_response_headers(review_comments, 'type')
# print(header_list[1])
# for item in header_list[0]:
#     print(item)

expansion_type = 'chronological'

all_list = get_all_comments_and_responses(review_comments, 
                                          expansion_type=expansion_type)
header_list = get_all_comments_and_response_headers(review_comments,
                                                    expansion_type=expansion_type)
# for item in header_list:
#     print(item)

df = pd.DataFrame(all_list, columns=header_list)
df.to_excel(f'all_output_{expansion_type}.xlsx', index=False)


#endregion



