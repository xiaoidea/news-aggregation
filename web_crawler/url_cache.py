# coding: utf-8

import time

import MySQLdb

from config import host, user, port, passwd, db


def _get_conn():
    conn = MySQLdb.connect(host=host, user=user, port=port, passwd=passwd, db=db, charset="utf8")
    return conn


class URLCache(object):
    """ read url which has already crawled from db into a set

    """
    conn = _get_conn()
    try:
        source_dict = dict()
        date = time.strftime("%Y-%m-%d", time.localtime())
        cursor = conn.cursor()
        sql = 'SELECT url, source FROM cached_url WHERE date = %s'
        cursor.execute(sql, (date,))
        results = cursor.fetchall()
        for row in results:
            if row[1] in source_dict:
                source_dict[row[1]].add(row[0])
            else:
                source_dict[row[1]] = set()
    except Exception as e:
        print e
    finally:
        conn.close()

    @staticmethod
    def need_and_add(url, source):
        if source not in URLCache.source_dict:
            URLCache.source_dict[source] = set(url)
            URLCache._add_in_db(url, source)
            return True
        else:
            if url not in URLCache.source_dict[source]:
                URLCache.source_dict[source].add(url)
                URLCache._add_in_db(url, source)
                return True
            else:
                return False

    @staticmethod
    def _add_in_db(url, source):
        try:
            conn = _get_conn()
            cursor = conn.cursor()
            sql = 'INSERT INTO cached_url VALUES (NULL , %s, %s, %s)'
            cursor.execute(sql, (url, source, URLCache.date))
            conn.commit()
        except Exception as e:
            print e

