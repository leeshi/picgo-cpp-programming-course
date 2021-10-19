#!/usr/bin/python
# -*- coding=utf8 -*-

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

import os
import json

IMG_HOST = ['github', 'imgur']

class ImageUploader():
    def __init__(self) -> None:
        self.initilized = False
        self.imgur_client_id = None
        self.imgur_client_secret = None
        # TODO read imgur id and secret from disk
        self.imgur_client = None
        self.file_name = "imgur.credential"   

    def set_imgur_api(self, imgur_client_id: str, imgur_client_secret: str) -> int:
        """
        initilize ImgurClient
        return result -> int
            on success: 0
            on failure: 1. there is a chance of typo or connection problem
        """
        self.imgur_client_id = imgur_client_id
        self.imgur_client_secret = imgur_client_secret
        self.initilized = True
        try:
            self.imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)
        except:
            return 1

        return 0

    def upload_image_imgur(self, local_path: str) -> dict:
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
    def save_credential(self) -> int:
        """
        save the imgur id and secret user added to disk
        return result -> string
            on success: 0
            on failure: 1
        """
        if not self.initilized:
            return 1
            
        jsObj = json.dumps({'id': self.imgur_client_id,
            'secret': self.imgur_client_secret})

        # handle exceptions in saving
        try:
            with open(self.file_name, 'w') as f:
                f.write(jsObj)
        except:
            return 1
        return 0

    def load_credential(self) -> int:
        """
        load saved imgur credential from json formatted text file
        please notice the script path
        no need to run set_imgur_api again
        return result -> int
            on success: 0
            on failure: 1
        """
        if not os.path.exists(self.file_name):
            return 1
        
        try:
            with open(self.file_name, 'r') as f:
                creDict = json.load(f)
                self.set_imgur_api(creDict['id'], creDict['secret'])
        except:
            return 1

        return 0


if __name__ == "__main__":
    image_uploader = ImageUploader()
    image_uploader.set_imgur_api('6b75af0f94d844f', '2100e84114950a3e5f567de219717ff596423c77')

    if (image_uploader.save_credential() == 0):
        print("credential saved")
        if (image_uploader.load_credential() == 0):
            print("credential loaded")
            result = image_uploader.upload_image_imgur(
                    '/home/leisik/pictures/Wallpapers/annie-spratt-r9eIL7jtenc-unsplash.jpg')
            if result['status_code'] == 0:
                print(result['msg'])
                print(result['url'])
            # operation failed
            else:
                print(result['msg'])
            
        else:
            print("failed to load credential")
    else:
        print("failed to save credential")
