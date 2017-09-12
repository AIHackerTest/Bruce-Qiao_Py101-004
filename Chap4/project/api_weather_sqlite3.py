""" 使用心知天气API """

import requests
import json
import re
from const_value import API, KEY, UNIT, LANGUAGE
from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

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
    weather_dict = []
    weather_dict.append(weather_json['results'][0]['location']['name'])
    weather_dict.append(weather_json['results'][0]['now']['text'])
    weather_dict.append(weather_json['results'][0]['now']['temperature'])
    weather_dict.append(change_date_format(weather_json['results'][0]['last_update']))

    return weather_dict

app = Flask(__name__)
conn = sqlite3.connect(":memory:", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE inquiry_list
            (city text, weather text, temp text, update_time text)
            ''')
conn.commit()

@app.route("/", methods=['POST', 'GET'])
def main():
    app.jinja_env.filters['change_date_format'] = change_date_format
    inquiry_outcome = None
    inquiry_history = None
    help_information = None
    is_updated = None
    error = None

    if request.method == "POST":
        if request.form['action'] == u'查询':
            c.execute('select * from inquiry_list where city=:city',
                        {"city": request.form['location']})
            select = c.fetchone()
            if select:
                inquiry_outcome = select
            else:
                result = fetchWeather(request.form['location'])
                if "status" in result.keys():
                    error=result['status']
                else:
                    inquiry_outcome = json_to_dict(result)
                    c.execute("INSERT INTO inquiry_list VALUES (?,?,?,?)",
                            (inquiry_outcome[0], inquiry_outcome[1],
                             inquiry_outcome[2], inquiry_outcome[3]))

        elif request.form['action'] == u'更正':
            city, weather = (request.form['location']).split(" ")
            c.execute('select * from inquiry_list where city=:city',
                        {"city": city})
            select = c.fetchone()
            if select:
                if weather in ["晴", "阴", "雨", "雪", "多云", "雾"]:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M')
                    c.execute('UPDATE inquiry_list SET weather=:weather, update_time=:update_time WHERE city=:city',
                                {"weather": weather, "update_time": now, "city": city})
                    is_updated = "天气信息更新成功！"
                else:
                    is_updated = "输入信息有误！"
            else:
                is_updated = "该城市不在查询历史中。"

        elif request.form['action'] == u'历史':
            c.execute('SELECT * FROM inquiry_list')
            inquiry_history = c.fetchall()
        else:
            #request.form['action'] == u'帮助':
            help_information = 1
        return render_template("api_weather.html",
            inquiry_outcome=inquiry_outcome,
            inquiry_history=inquiry_history,
            help_information=help_information,
            is_updated=is_updated,
            error=error)
    else:
        return render_template("api_weather.html")

if __name__ == '__main__':
    app.run(debug = True)
