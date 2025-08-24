from drchecks_reviews import Review, ProjectInfo, ReviewComments

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments

print(review_comments.max_evaulations)