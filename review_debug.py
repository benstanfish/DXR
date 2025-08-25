from drchecks_reviews import Review, ReviewComments, _RESPONSE_COLUMNS
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

max_evals, max_bcs = review.review_comments.max_responses
# print(max_evals, max_bcs)

c_max_evals, c_max_bcs = comment.total_responses
# print(c_max_evals, c_max_bcs)

# for evaluation in comment.evaluations:
#     print(evaluation.to_list())

# for i in range(max_evals):
#     if i == comment.evaluations_count:
#         print(i, ['']*len(_RESPONSE_COLUMNS))
#     else:
#         print(i, comment.evaluations[i].to_list())

def padded_evaluations(comment,
                       review_max_evaluations,
                       response_columns=_RESPONSE_COLUMNS):
    padded_list = []
    for i in range(review_max_evaluations):
        if i == comment.evaluations_count:
            padded_list += ['']*len(response_columns)
        else:
            padded_list += comment.evaluations[i].to_list(response_columns)
    return padded_list

def padded_backchecks(comment,
                      review_max_backchecks,
                      response_columns=_RESPONSE_COLUMNS):
    padded_list = []
    for i in range(review_max_backchecks):
        if i == comment.backchecks_count:
            padded_list += ['']*len(response_columns)
        else:
            padded_list += comment.backchecks[i].to_list(response_columns)
    return padded_list

def padded_responses(review_comments: ReviewComments, 
                     response_columns=_RESPONSE_COLUMNS):
    max_evals, max_bcs = review_comments.max_responses
    response_list = []
    for comment in review_comments.to_list:
        temp_list = padded_evaluations(comment, max_evals) + padded_backchecks(comment, max_bcs)
        response_list.append(temp_list)
    return response_list

full_list = padded_responses(review.review_comments)


padded_evals_list = padded_evaluations(comment, max_evals)
# print(padded_evals_list)

padded_bc_list = padded_backchecks(comment, max_bcs)
# print(padded_bc_list)

padded_list = padded_evals_list + padded_bc_list
# print(padded_list)


#endregion