from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import re
import sys

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url_list = None
    if request.method == 'POST' and 'url_list' in request.form:
        url_list = request.form['url_list']
    return render_template('form.html', url_list=url_list)

@app.route("/get_result", methods=['GET', 'POST'])
def render_result():
    input = request.form['url_list']
    urls = []
    result_array = []
    for i in request.form['url_list'].splitlines():
      urls.append(i)
    for url in urls:
        response = requests.get(url,allow_redirects=True)
        result_array.append([url,response.status_code,response.url])
    return render_template('view_result.html', result=result_array)


if __name__ == "__main__":
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=sys.argv[3])