#!/usr/bin/python
# -*- coding=utf8 -*-

import os
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

class ImageModel():
    def __init__(self, db_name) -> None:
        self.con = sqlite3.connect(db_name)
        # 不存在则自动创建
        try:
            self.con.execute('''CREATE TABLE tbl_image (
                    image BLOB NOT NULL,
                    local_path TEXT NOT NULL,
                    remote_url TEXT NOT NULL);''')
        except:
            print('table has been created.')

    def save_image(self, local_path: str, remote_url: str) -> None:
        """保存本地的图片到数据库中 提供的是图片的地址, 而不是图片本身
        注意: 图片会先转化成 png 格式后再存入数据库
        """
        # silly workaround
        img = Image.open(local_path)
        pic_name = local_path.split('.')[0]
        png_path = '{0}.png'.format(pic_name)
        img.save(png_path)
        fp = open(png_path, 'rb')
        img_blob = fp.read()
        try:
            sql = 'INSERT INTO tbl_image (image, local_path, remote_url) VALUES (?,?,?);'
            self.con.execute(sql, (img_blob, local_path, remote_url))
            self.con.commit()
        except:
            print('Failed to write image [{0}]'.format(local_path))
        finally:
            fp.close()
            os.remove(png_path)

    def get_images_count(self) -> int:
        """获取数据库中图片的数量
        """
        cu = self.con.cursor()
        cu.execute('SELECT COUNT(*) FROM tbl_image')
        return cu.fetchall()[0][0]

    def get_all_images(self) -> list[list]:
        """获取数据库中所有的图片( png 格式)
        结果是 list of (img_binary, local_path, remote_url)
        返回的图片是二进制的, 将其转化成numpy数组的方法如下:

        >>> first_image = db.get_all_images()[0]
        >>> image_np = plt.imread(BytesIO(first_image)) # 获得的numpy数组
        """
        cu = self.con.cursor()
        cu.execute('SELECT * FROM tbl_image')
        return cu.fetchall()

if __name__ == "__main__":
    db = ImageModel('./my.db')
    db.save_image('/home/leisik/pictures/Wallpapers/annie-spratt-r9eIL7jtenc-unsplash.jpg', 'test url')
    all_images = db.get_all_images()
    image_np = plt.imread(BytesIO(all_images[0][0]))     # 转化二进制数据为可供显示的 numpy 数组
    plt.imshow(image_np)
    print(image_np)
    plt.show()
