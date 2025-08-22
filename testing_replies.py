import reviews
from reviews import ProjectInfo, ReviewComments
from remarks import Comment

xml_path = 'test.xml'

root = reviews.get_root(xml_path)
# proj_info_element = reviews.get_project_info_element(root)
# review_comments_element = reviews.get_review_comments_element(root)

proj_info_element, review_comments_element = reviews.get_review(root)
proj_info = ProjectInfo.from_tree(proj_info_element)
# print(proj_info.all_data)
# print(proj_info.all_data['Project Name'])


review_comments = ReviewComments.from_tree(review_comments_element)
# print(type(review_comments.comments[0]))
# print(review_comments.comment_count)

# i = 0
# for comment in review_comments.comments:
#     print(i, comment.author)
#     i += 1

# print(review_comments.comments[2].print_responses())
# for resp in review_comments.comments[1].get_responses:
#     print(resp.id, resp.author, resp.date_created)

# print('-'*50)

# for resp in review_comments.comments[1].get_chronological_responses:
#     print(resp.id, resp.author, resp.date_created)

# print(review_comments._total_evaulations_count)
# print(review_comments._total_backchecks_count)
# print(review_comments.total_responses_count)

max_evals, max_bcs = review_comments.max_response_counts
print(max_evals, max_bcs)
