import re

base_name = r'abc % some t|ext that [ aI wand ] toi / replace \ * adn d* ? @ and '

bad_chars = r'[!?@#$%^&*()\[\]|\\\/]'
new_name = re.sub(bad_chars, '', base_name)

print(new_name)