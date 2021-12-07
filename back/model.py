#!/usr/bin/python
# -*- coding=utf8 -*-

import sqlite3
import os
import matplotlib.image as mp

class Image():
    def __init__(self, db_name) -> None:
        self.con = sqlite3.connect(db_name)
        # 不存在则自动创建
        if not os.path.exists(db_name):
            self.con.execute('''CREATE TABLE tbl_image (id integer PRIMARY KEY AUTO_INCREMENT, image BLOB NOT NULL, local_path TEXT NOT NULL, remote_url TEXT NOT NULL);''')

    def save_image(self, img, local_path, remote_url):
        img_blob = sqlite3.Binary(img)
        try:
            sql = 'INSERT INTO tbl_image (image, local_path, remote_url) VALUES (?,?,?);'
            self.con.execute(sql, (img_blob, local_path, remote_url))
            self.con.commit()
            self.con.close()
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
    img = mp.imread('/home/leisik/pictures/Wallpapers/jeremy-bishop-uAfZBP-GtiA-unsplash.jpg')
    img_db = Image('./tbl_image.db')
    print(img_db.get_images_count())
    print(img_db.get_all_images())
    # img_db.save_image(img, 'local_path', 'remote_url')
