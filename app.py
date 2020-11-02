from flask import Flask, render_template, request
import requests
import sys

DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('templates/form.html')

@app.route("/get_result", methods=['GET', 'POST'])
def render_result():
    urls = []
    result_array = []
    if (str(request.form['agent_option'])=="on"):
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
    else:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    for i in request.form['url_list'].splitlines():
      urls.append(i.rstrip())
    for url in urls:
        if url == '':
            pass
        else:
          headers = {
              'User-Agent': '{}'.format(user_agent)
              }
          try:
              response = requests.get(url,allow_redirects=True,headers=headers)
              result_array.append([url,response.status_code,response.url])
          except requests.exceptions.ConnectionError:
              result_array.append([url,"503","Connection error. Host is not available"])
          except requests.exceptions.MissingSchema:
              result_array.append([url,"503","Invalid url"])
          except requests.exceptions.ConnectTimeout:
              result_array.append([url,"408","Request timeout"])
    return render_template('templates/view_result.html', result=result_array)

if __name__ == "__main__":
    app.run()