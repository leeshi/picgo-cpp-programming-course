#!/usr/bin/python
# -*- coding=utf8 -*-

import sqlite3
import os
import matplotlib.image as mp

class Image():
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

    def save_image(self, img, local_path, remote_url):
        """将图片存到数据库中, 需要提供本地路径, 以及图床地址
        """
        img_blob = sqlite3.Binary(img)
        try:
            sql = 'INSERT INTO tbl_image (image, local_path, remote_url) VALUES (?,?,?);'
            self.con.execute(sql, (img_blob, local_path, remote_url))
            self.con.commit()
        except:
            print('Failed to write image [{0}]'.format(local_path))

    def get_images_count(self):
        """获取数据库中图片的数量
        """
        cu = self.con.cursor()
        cu.execute('SELECT COUNT(*) FROM tbl_image')
        return cu.fetchall()[0][0]

    def get_all_images(self):
        """获取数据库中所有的图片
        """
        cu = self.con.cursor()
        cu.execute('SELECT * FROM tbl_image')
        return cu.fetchall()

if __name__ == "__main__":
    # 读取图片 使用matplotlib
    img = mp.imread('/home/leisik/pictures/Wallpapers/jeremy-bishop-uAfZBP-GtiA-unsplash.jpg')
    img_db = Image('my.db')
    img_db.save_image(img, 'test path', 'test url')
    print(img_db.get_images_count())
    print(img_db.get_all_images())
    # img_db.save_image(img, 'local_path', 'remote_url')
