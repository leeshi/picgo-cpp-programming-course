#!/usr/bin/python
# -*- coding=utf8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# here is how you should use uploader
from back import *

################################### imgur #######################################
uploader = ImageUploader()
uploader.set_imgur_api('6b75af0f94d844f',
        '0f45fb3d25a709ee76aabd9d4d72957b8c839985')

# select an image
# return value is a dict
result = uploader.upload_image_imgur(
        '/home/leisik/pictures/Wallpapers/annie-spratt-r9eIL7jtenc-unsplash.jpg')

# check result
# operation successed
if result['status_code'] == 0:
    print(result['msg'])
    print(result['url'])
# operation failed
else:
    print(result['msg'])
