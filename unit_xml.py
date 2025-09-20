# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
from faker import Faker
from .buildtools.buildtools import timestamp


file_name = f'test_xml_{timestamp()}.xml'

fake = Faker()

print(fake.name())