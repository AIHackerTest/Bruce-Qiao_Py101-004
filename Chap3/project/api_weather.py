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

    return x.group('year') + '-' + x.group('month') + '-' + x.group('date') + ' ' + x.group('hour') + ':' + x.group('minute') + ':' + x.group('second')

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
def index():

    Help_information = ["输入城市名，按查询获得天气信息",
                        "按帮助获得帮助信息",
                        "按历史获得查询历史信息"]

    if request.method == "POST":
        if request.form['action'] == u'查询':
            location = request.form['location']
            result = fetchWeather(location)
            if "status" in result.keys():
                return render_template("error_message.html", outcome=result['status'])
            else:
                weather_dict = json_to_dict(result)
                inquiry_list.append(weather_dict)
                return render_template("inquiry_outcome.html", outcome=weather_dict)

        elif request.form['action'] == u'历史':
            return render_template("inquiry_list.html", outcome=inquiry_list)
        else:
            #request.form['action'] == u'帮助':
            return render_template("help.html", outcome=Help_information)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()
