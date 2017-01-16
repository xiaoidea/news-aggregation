# coding: utf-8

import MySQLdb

from crawler_tencent import TencentCrawler

# MySQL connection
host = '127.0.0.1'
port = 3306
user = 'root'
passwd = 'root'
charset = 'utf-8'
db = 'news'


class CrawlAndStore(object):
    def collect_news(self):
        CT = TencentCrawler()
        news_obj_list, para_obj_list = CT.start_spider()
        for news, paragraph_list in zip(news_obj_list, para_obj_list):
            self._store(news, paragraph_list)

    def _store(self, news, paragraph_list):
        conn = MySQLdb.connect(host=host, port=port, passwd=passwd, db=db, charset=charset)
        try:
            cursor = conn.cursor()
            sql_news = 'INSERT INTO news_item VALUES (NULL, %s, %s, %s, %s, %s, %s)'
            news_id = cursor.execute(sql_news, news.source, news.url, news.title, news.category, news.last_update_time, news.date)
            sql_para = 'INSERT INTO news_paragraph VALUES (NULL, %d, %s, %d, %s)'
            for paragraph in paragraph_list:
                cursor.execute(sql_para, news_id, paragraph.para_content, paragraph.is_image, paragraph.date)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print e
        finally:
            conn.close()

    def clean(self):
        pass


if __name__ == '__main__':
    CAS = CrawlAndStore()
    # CAS.collect_news()
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='news', charset=charset)