#!/usr/bin/env python
import os
import random

import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

print(os.getcwd())


@app.route("/")
def hello():
    query = request.args.get('query')
    data = pd.read_csv("../../Կարգին 2+3րդ փլեյլիստ - Sheet3.csv")
    return {"url": random.choice(data.links),
            "query": query}

    # try:
    #     pass
    # except:
    #     print(os.getcwd())
    #     print(os.listdir(".."))
    # # return jsonify({'res':509})
    # # return jsonify()
    # return render_template('index.html')

    # logging.DEBUG(os.curdir())
    # data = pd.read_csv("Kargin_project/Կարգին 2+3րդ փլեյլիստ - Sheet3.csv")
    #
    # return render_template('index.html', html_page_text=data)
    # text = "բարևևևևևևև\nձեզի բորդո գույնի ներկ պետք ա՞"
    # return render_template('index.html', html_page_text=text)

#
# @app.route("/search")
# def search():
#     data = pd.read_csve("Կարգին 2+3րդ փլեյլիստ - Sheet3.csv")
#
#     return render_template('index.html', html_page_text=data)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=True, host='192.168.8.35', port=69)
