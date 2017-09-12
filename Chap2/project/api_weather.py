""" 使用心知天气API """

import requests
import json
import re
from const_value import API, KEY, UNIT, LANGUAGE

def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=5)

    return json.loads(result.content)

def json_to_dict(weather_json):
    weather_dict = {}

    weather_dict['city'] = weather_json['results'][0]['location']['name']
    weather_dict['weather_condition'] = weather_json['results'][0]['now']['text']
    weather_dict['temperature'] = weather_json['results'][0]['now']['temperature']
    weather_dict['update_time'] = change_date_format(weather_json['results'][0]['last_update'])

    return weather_dict

def change_date_format(raw_date):
    expr = r"\b(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<date>\d\d)T(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)\b"
    x = re.search(expr, raw_date)

    return x.group('year') + '-' + x.group('month') + '-' + x.group('date') + ' ' + x.group('hour') + ':' + x.group('minute') + ':' + x.group('second')

def print_inquiry_outcome(weather_dict):
    city_name = weather_dict['city']
    weather_condition = weather_dict['weather_condition']
    temperature = weather_dict['temperature']
    update_time = weather_dict['update_time']

    print(f"{city_name} 的天气为{weather_condition}，温度为{temperature}摄氏度。更新时间为{update_time}。（数据来自心知天气。）")

def print_inquiry_list(inquiry_list):
    for inquiry_list_item in inquiry_list:
        print_inquiry_outcome(inquiry_list_item)

if __name__ == '__main__':
    inquiry_list = []

    while True:
        location = input("请输入要查询的城市名称：")

        if location in ["quit", "q", "Q", "exit"]:
            print_inquiry_list(inquiry_list)
            break
        elif location in ["help", "h", "H"]:
            print("""
            Input city name to get the weather;
            Input "help" to get the help information;
            Input "history" to get the information you inquiried;
            Input "quit" to quit the program.
            """)
        elif location in ["history", "his"]:
            print_inquiry_list(inquiry_list)
        else:
            result = fetchWeather(location)

            if "status" in result.keys():
                print(result['status'])
            else:
                weather_dict = json_to_dict(result)
                print_inquiry_outcome(weather_dict)
                inquiry_list.append(weather_dict)
