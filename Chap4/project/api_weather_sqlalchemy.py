""" 使用心知天气API """

import requests
import json
import re
from const_value import API, KEY, UNIT, LANGUAGE
from flask import Flask, render_template, request
from datetime import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy

def fetchWeather(location):
    try:
        result = requests.get(
            API, params={
            'key': KEY,
            'location': location,
            'language': LANGUAGE,
            'unit': UNIT},
            timeout=3)
        return json.loads(result.content)
    except requests.exceptions.Timeout:
        return None

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
# create a database in memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)

class Inquiry_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True)
    weather = db.Column(db.String(80), unique=False)
    temp = db.Column(db.String(20), unique=False)
    update_time = db.Column(db.String(120), unique=False)

    def __init__(self, city, weather, temp, update_time):
        self.city = city
        self.weather = weather
        self.temp = temp
        self.update_time = update_time

db.create_all()

@app.route("/", methods=['POST', 'GET'])
def main():
    #app.jinja_env.filters['change_date_format'] = change_date_format
    inquiry_outcome = None
    inquiry_history = None
    help_information = None
    is_updated = None
    error = None

    if request.method == "POST":
        if request.form['action'] == u'查询':
            select = Inquiry_list.query.filter_by(city=request.form['location']).first()
            if select:
                inquiry_outcome = select
            else:
                result = fetchWeather(request.form['location'])
                if result:
                    if "status" in result.keys():
                        error=result['status']
                    else:
                        inquiry = json_to_dict(result)
                        db.session.add(Inquiry_list(inquiry[0], inquiry[1],
                                            inquiry[2], inquiry[3]))
                        db.session.commit()
                        inquiry_outcome = Inquiry_list.query.filter_by(city=inquiry[0]).first()
                else:
                    error = "网络有些问题，请稍后再试。"

        elif request.form['action'] == u'更正':
            try:
                city, weather = (request.form['location']).split(" ")
                select = Inquiry_list.query.filter_by(city=city).first()
                if select:
                    if weather in ["晴", "阴", "雨", "雪", "多云", "雾"]:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M')
                        select.weather = weather
                        select.update_time = now
                        db.session.commit()
                        is_updated = "天气信息更新成功！"
                    else:
                        is_updated = "输入天气信息有误！"
                else:
                    is_updated = "该城市不在查询历史中。"
            except ValueError:
                is_updated = "请按（城市名 常见天气）格式输入！"

        elif request.form['action'] == u'历史':
            lists = Inquiry_list.query.all()
            inquiry_history = lists
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
