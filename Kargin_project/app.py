#!/usr/bin/env python
import os
import random

import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/api", methods=["GET", "POST"])
def hello():
    # query = request.args.get('query')
    inp = request.json.get('urls')
    print(inp)

    return jsonify({'inp': inp})
    # data = pd.read_csv("../kargin_done.csv")
    # return jsonify({"url": random.choice(data.links),
    #         "inp": inp})


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, host='192.168.8.156', port=509)
