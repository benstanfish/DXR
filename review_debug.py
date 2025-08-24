from drchecks_reviews import Review, ProjectInfo, ReviewComments
import utils
from utils import _NL as NL

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments


for comment in review_comments.comments:
    print(utils._BOLD + utils._RED + comment.id + utils._RESET, 
          utils._BOLD + utils._GREEN + comment.author + utils._RESET, 
          NL + comment.text + NL)

