# coding: utf-8


class News(object):
    def __init__(self, source, url, title, category, last_update_time, date):
        self.source = source
        self.url = url
        self.title = title
        self.category = category
        self.last_update_time = last_update_time
        self.date = date

    def __str__(self):
        return self.title
