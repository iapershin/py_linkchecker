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
    return render_template('form.html')

@app.route("/get_result", methods=['GET', 'POST'])
def render_result():
    urls = []
    result_array = []
    if (str(request.form['agent_option'])=="on"):
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
    else:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    for i in request.form['url_list'].splitlines():
      urls.append(i)
    for url in urls:
        headers = {
            'User-Agent': '{}'.format(user_agent)
            }
        try:
            response = requests.get(url,allow_redirects=True,headers=headers)
            result_array.append([url,response.status_code,response.url])
        except requests.exceptions.ConnectionError:
            result_array.append([url,"503","Connetion error. Host is not available"])
    return render_template('view_result.html', result=result_array)

if __name__ == "__main__":
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=sys.argv[3])