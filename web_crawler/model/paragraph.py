# coding: utf-8


class Paragraph(object):
    def __init__(self, para_content, is_image, date, news_id=None):
        self.news_id = news_id
        self.para_content = para_content
        self.is_image = is_image
        self.date = date

    def __str__(self):
        return self.para_content
