import reviews
from reviews import ProjectInfo

xml_path = 'test.xml'

root = reviews.get_root(xml_path)
# proj_info_element = reviews.get_project_info_element(root)
# review_comments_element = reviews.get_review_comments_element(root)

proj_info_element, review_comments_element = reviews.get_review(root)

proj_info = ProjectInfo.from_tree(proj_info_element)
print(proj_info.all_data)

print(proj_info.all_data['Project Name'])