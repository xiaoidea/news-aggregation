# coding: utf-8

from config import host, user, port, passwd, db
import os.path
import MySQLdb
import time


def _get_conn():
    conn = MySQLdb.connect(host=host, user=user, port=port, passwd=passwd, db=db, charset="utf8")
    return conn


def tencent_core_news():
    core_news = []  # return a list which contains a news dict
    conn = _get_conn()
    try:
        cursor = conn.cursor()
        date = time.strftime("%Y-%m-%d", time.localtime())
        sql = "SELECT news_id, title FROM news_item WHERE source = 'tencent' AND category = 'core' AND date = %s"
        cursor.execute(sql, (date,))
        results = cursor.fetchall()
        for row in results:
            core_news.append({"news_id": row[0], "title": row[1], "source": "tencent", "category": "core"})
    except Exception as e:
        print e
    finally:
        conn.close()
    return core_news


def get_news_content(news_id):
    news_paragraph = []
    conn = _get_conn()
    try:
        cursor = conn.cursor()
        sql = "SELECT para_content, is_image FROM news_paragraph WHERE news_id = %s ORDER BY para_id"
        cursor.execute(sql, (news_id,))
        results = cursor.fetchall()
        for row in results:
            if int(row[1]) == 1:
                news_paragraph.append({"content": os.path.basename(row[0]), "is_image": row[1]})
                pass
            else:
                news_paragraph.append({"content": row[0], "is_image": row[1]})
    except Exception as e:
        print e
    finally:
        conn.close()
    return news_paragraph
