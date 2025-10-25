# Copyright (c) 2018-2025 Ben Fisher

__author__ = "Ben Fisher"
__author_email__ = "benstanfish@gmail.com"
__license__ = "GPL-3"
__maintainer_email__ = __author_email__
__url__ = 'https://github.com/benstanfish/DXR'
__version__ = "0.0.2a"
__python__ = "3.13"


LOG_DIR = './logs'
import os
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)