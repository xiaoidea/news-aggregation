# coding: utf-8
import os
import requests


def path_builder(source, image_id, date):
    return r"{}{}img{}{}_{}_{}.jpg".format(os.path.abspath(os.curdir), os.sep, os.sep, source, image_id, date)


def image_download(src, path):
    pic = requests.get(src)
    with open(path, 'wb') as fp:
        fp.write(pic.content)


if __name__ == '__main__':
    path = path_builder('tencent', '1', '2017-01-16')
    image_download(r"http://inews.gtimg.com/newsapp_bt/0/1038326496/641", path)
