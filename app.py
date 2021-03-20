from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('form.html')

@app.route("/get_result", methods=['GET', 'POST'])
def render_result():
    if (str(request.form['agent_option'])=="on"):
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
    else:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    return render_template('view_result.html', user_agent=user_agent)

def make_request(url,user_agent):
    if url == '':
        pass
    else:
        headers = {
            'user-agent': '{}'.format(user_agent),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'upgrade-insecure-Requests': '1'
        }
        try:
            response = requests.get(url,allow_redirects=True,headers=headers,timeout=3)
            return url,response.status_code,response.url
        except requests.exceptions.ConnectionError:
            return url,"503","Connection error. Host is not available"
        except requests.exceptions.MissingSchema:
            return url,"503","Invalid url"
        except requests.exceptions.Timeout:
            return url,"408","Request timeout"
        except requests.exceptions.ConnectTimeout:
            return url,"408","Request timeout"

app.jinja_env.globals.update(make_request=make_request)


if __name__ == "__main__":
    app.run()
