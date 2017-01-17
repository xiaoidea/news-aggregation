# coding: utf-8

import sys

import MySQLdb

from crawler_tencent import TencentCrawler
from db_property import host, user, port, passwd, db

reload(sys)
sys.setdefaultencoding("utf-8")


class CrawlAndStore(object):
    def collect_news(self):
        CT = TencentCrawler()
        news_obj_list, para_obj_list = CT.start_spider()
        for news, paragraph_list in zip(news_obj_list, para_obj_list):
            self._store(news, paragraph_list)

    def _store(self, news, paragraph_list):
        conn = MySQLdb.connect(host=host, user=user, port=port, passwd=passwd, db=db, charset="utf8")
        try:
            cursor = conn.cursor()
            sql_news = 'INSERT INTO news_item VALUES (NULL, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql_news, self._transform_news(news))
            news_id = conn.insert_id()
            sql_para = 'INSERT INTO news_paragraph VALUES (NULL, %s, %s, %s, %s)'
            for paragraph in paragraph_list:
                cursor.execute(sql_para,
                               (int(news_id), paragraph.para_content, int(paragraph.is_image), paragraph.date))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print e
        finally:
            conn.close()

    @staticmethod
    def _transform_news(news):
        return news.source, news.url, news.title, news.category, news.last_update_time, news.date

    def clean(self):
        pass


if __name__ == '__main__':
    CAS = CrawlAndStore()
    CAS.collect_news()
    print "**"*100
    print "done!"
    print "**"*100
