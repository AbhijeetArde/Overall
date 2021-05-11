from flask import Flask, render_template, request
import requests
import datetime
import json

app = Flask(__name__)
x = datetime.datetime.today()
date = x.strftime("%d-%m-%Y")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/suggestions')
def suggestions():
    available_list = []
    import datetime
    import json
    import requests

    browser_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    pincode = '410206'
    x = datetime.datetime.today()
    date = x.strftime("%d-%m-%Y")
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}".format(
        pincode=pincode, date=date)
    response = requests.get(URL, headers=browser_header)
    if (response.ok) and ('centers' in json.loads(response.text)):
        resp_json = json.loads(response.text)['centers']
        if resp_json is not None:
            for each in resp_json:
                for session in each['sessions']:
                    if session['min_age_limit'] == 18:
                        print(each['name'], ":")
                        # if session['available_capacity'] > 0:
                        # print(session)
                        final_list = {each['name']: session['available_capacity']}
                        available_list.append(final_list)
                        print(available_list)
    return render_template('available.html', suggestions=available_list)

if __name__ == '__main__':
    app.run(debug=True)
