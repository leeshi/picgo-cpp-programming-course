#!/usr/bin/python
# -*- coding=utf8 -*-

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

import os

IMG_HOST = ['github', 'imgur']

class ImageUploader():
    def __init__(self) -> None:
        self.initilized = False
        self.imgur_client_id = None
        self.img_client_secret = None
        # TODO read imgur id and secret from disk
        self.imgur_client = None

    def set_imgur_api(self, imgur_client_id, imgur_client_secret) -> None:
        self.imgur_id = imgur_client_id
        self.img_secret = imgur_client_secret
        self.initilized = True
        self.imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

    def upload_image_imgur(self, local_path):
        """
        upload an image to imgur
        @local_path: the local image path
        
        return result -> dict
            on success: status_code == 0, url is the image url
            on failure: status_code == 1, 2, 3 means ImgurClientError, unset
            imgur information and wrong path respectively
        """
        if self.imgur_client == None:
            result = {
                'status_code': 2,
                'msg': 'client_id and client_secret have not yet been set'
            }
            return result

        if not os.path.exists(local_path):
            result = {
                'status_code': 3,
                'msg': 'File not found.'
            }
            return result

        try:
            a = self.imgur_client.upload_from_path(local_path)
            link = a['link']
            result = {
                'status_code': 0,
                'url': link,
                'msg': 'Operation successful'
            }
            return result
        except ImgurClientError as e:
            print(e.error_message)
            result = {
                'status_code': 1,
                'msg': 'Something went wrong with imgurclient'
            }
            return result

if __name__ == "__main__":
    image_uploader = ImageUploader()
    image_uploader.set_imgur_api('6b75af0f94d844f', '0f45fb3d25a709ee76aabd9d4d72957b8c839985')
    upload_result = image_uploader.upload_image_imgur('/home/leisik/pictures/Wallpapers/annie-spratt-r9eIL7jtenc-unsplash.jpg')
    print(upload_result)
