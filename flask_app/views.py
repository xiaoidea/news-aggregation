# coding: utf-8

from flask import render_template
from flask_app import app
import models


@app.route("/")
def index():
    data = dict()
    data["tencent_core"] = models.tencent_core_news()
    return render_template("index.html", data=data)


@app.route("/news/<nid>")
def news_content(nid):
    data = models.get_news_content(nid)
    return render_template("news.html", data=data)


if __name__ == '__main__':
    app.run()
