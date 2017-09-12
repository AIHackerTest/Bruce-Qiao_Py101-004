"""Use OpenWeatherMap API"""

import requests
import json
from datetime import datetime
from const_value_openweathermap import API, APIKEY, LANGUAGE, UNIT

def fetchWeather(location):
    result = requests.get(API, params={
        'APPID': APIKEY,
        'q': location,
        'lang': LANGUAGE,
        'units': UNIT
    }, timeout=10)

    return json.loads(result.content)

def json_to_dict(weather_json):
    weather_dict = {}

    weather_dict['city'] = weather_json['name']
    weather_dict['weather_condition'] = weather_json['weather'][0]['description']
    weather_dict['temperature'] = weather_json['main']['temp']
    weather_dict['update_time'] = weather_json['dt']

    return weather_dict

def change_date_format(unix_date):

    return datetime.fromtimestamp(int(unix_date)).strftime('%Y-%m-%d %H:%M:%S')

def print_inquiry_outcome(weather_dict):
    city_name = weather_dict['city']
    weather_condition = weather_dict['weather_condition']
    temperature = weather_dict['temperature']
    update_time = change_date_format(weather_dict['update_time'])

    print(f"{city_name} 的天气为{weather_condition}，温度为{temperature}摄氏度。更新时间为{update_time}。（数据来自OpenWeatherMap。）")

def print_inquiry_list(inquiry_list):
    for inquiry_list_item in inquiry_list:
        print_inquiry_outcome(inquiry_list_item)

def main():
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

            if result['cod'] != 200:
                print("There is something wrong.")
            else:
                weather_dict = json_to_dict(result)
                print_inquiry_outcome(weather_dict)
                inquiry_list.append(weather_dict)

if __name__ == '__main__':
    main()
