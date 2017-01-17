# coding: utf-8
"""
download picture in news

"""

import os
import requests
from random import Random


def _random_str(random_length=8):
    """ generate random string used in picture file path to handle browser cache

    :param random_length:
    :return:
    """
    string = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def path_builder(source, image_id, date):
    tmp = os.path.abspath(os.curdir).replace("web_crawler", "flask_app")
    return r"{}{}static{}img{}{}_{}_{}_{}.jpg".format(tmp, os.sep, os.sep, os.sep, source, image_id, date, _random_str())


def image_download(src, path):
    pic = requests.get(src)
    with open(path, 'wb') as fp:
        fp.write(pic.content)


if __name__ == '__main__':
    path = path_builder('tencent', '1', '2017-01-16')
    print path
