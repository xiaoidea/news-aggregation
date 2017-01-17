# coding: utf-8
import time

import requests
from bs4 import BeautifulSoup

from model.news import News
from model.paragraph import Paragraph
from url_cache import URLCache
import image_tool
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class TencentCrawler(object):
    base_url = r"http://www.qq.com/"
    image_id = 1

    def start_spider(self):
        """ start crawling different categories news from http://www.qq.com/

        :return:
        """
        response = requests.get(self.base_url)
        response.encoding = 'gb18030'
        soup = BeautifulSoup(response.text, "html.parser")
        return self._core_news_spider(soup=soup)
        # self._entertainment_news_spider(soup=soup)

    def _core_news_spider(self, soup):
        """ get core news html document

        :return:
        """
        news_list = []
        try:
            news_contents = soup.find("body").find("div", id="qq-contents2").find_all("div", class_="newsContent")
            if news_contents is not None:
                for news_content in news_contents:
                    li_s = news_content.find_all("li")
                    if li_s is not None:
                        for li in li_s:
                            targets = li.find_all("a")
                            if targets is not None:
                                for target in targets:
                                    url = target.get("href")
                                    title = target.string
                                    news_list.append((url, title))
        except Exception as e:
            print e

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_date = time.strftime("%Y-%m-%d", time.localtime())

        news_obj_list = []
        para_obj_list = []
        for (url, title) in news_list:
            if not URLCache.need_and_add(url, 'tencent'):
                continue
            current_news, current_paragraphs = self._parse_news(url=url, title=title, category='core',
                                                                current_time=current_time, current_date=current_date)
            news_obj_list.append(current_news)
            para_obj_list.append(current_paragraphs)

        return news_obj_list, para_obj_list

    def _entertainment_news_spider(self, soup):
        """ get entertainment news html document

        :return:
        """
        pass

    def _parse_news(self, url, title, category, current_time, current_date):
        """ parse news document into News Model and Paragraph Model in a standard format

        :return: a News object and a list of Paragraph object
        """
        current_news = News(source='tencent', url=url, title=title, category=category, last_update_time=current_time,
                            date=current_date)
        current_paragraphs = []
        response = requests.get(url=url)
        response.encoding = 'gb18030'
        soup = BeautifulSoup(response.text, "lxml")
        soup.prettify()
        content = soup.find("body").find("div", id="content") if soup.find("body") is not None else None
        qq_article = content.find("div", class_="qq_article") if content is not None else None
        bosszone = qq_article.find("div", bosszone="content") if qq_article is not None else None
        p_s = bosszone.find_all("p") if bosszone is not None else None
        if p_s is not None:
            for p in p_s:
                if p.find("img") is not None:
                    img_src = p.find("img")['src']
                    path = image_tool.path_builder(source='tencent', image_id=self.image_id, date=current_date)
                    image_tool.image_download(src=img_src, path=path)
                    self.image_id += 1
                    current_paragraphs.append(Paragraph(para_content=path, is_image=1, date=current_date))
                elif p.string is not None and len(p.string) > 0:
                    current_paragraphs.append(Paragraph(para_content=p.string, is_image=0, date=current_date))
        return current_news, current_paragraphs


if __name__ == '__main__':
    tc = TencentCrawler()
    tc.start_spider()

