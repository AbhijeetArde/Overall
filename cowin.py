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
                    print("Avaialble : ", session['available_capacity'])