""" 使用心知天气API """

import requests
import json
import re
from const_value import API, KEY, UNIT, LANGUAGE
from flask import Flask, render_template, request

def fetchWeather(location):
    result = requests.get(
        API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT},
        timeout=5)

    return json.loads(result.content)

def change_date_format(raw_date):
    expr = r"\b(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<date>\d\d)T(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)\b"
    x = re.search(expr, raw_date)

    return x.group('year') + '-' + x.group('month') + '-' + x.group('date') + ' ' + x.group('hour') + ':' + x.group('minute')

def json_to_dict(weather_json):
    weather_dict = {}

    weather_dict['city'] = weather_json['results'][0]['location']['name']
    weather_dict['weather_condition'] = weather_json['results'][0]['now']['text']
    weather_dict['temperature'] = weather_json['results'][0]['now']['temperature']
    weather_dict['update_time'] = change_date_format(weather_json['results'][0]['last_update'])

    return weather_dict

app = Flask(__name__)
inquiry_list = []

@app.route("/", methods=['POST', 'GET'])
def main():

    inquiry_outcome = None
    inquiry_history = None
    help_information = None
    error = None

    if request.method == "POST":
        if request.form['action'] == u'查询':
            result = fetchWeather(request.form['location'])
            if "status" in result.keys():
                error=result['status']
            else:
                inquiry_outcome = json_to_dict(result)
                inquiry_list.append(inquiry_outcome)

        elif request.form['action'] == u'历史':
            inquiry_history = inquiry_list
        else:
            #request.form['action'] == u'帮助':
            help_information = 1
        return render_template("api_weather.html",
            inquiry_outcome=inquiry_outcome,
            inquiry_history=inquiry_history,
            help_information=help_information,
            error=error)
    else:
        return render_template("api_weather.html")

if __name__ == '__main__':
    app.run(debug = True)
