def txt_to_dict(txt_file):
    with open(txt_file) as f:
        content = f.read().splitlines()

    weather_dict = {}

    for line in content:
        weather_dict[line.split(',')[0]] = line.split(',')[1]
    return weather_dict

def print_inquiry_dict(inquiry_dict):
    for city, weather in inquiry_dict.items():
        print(f"{city}: {weather}")

def city_to_weather(weathers, city):
    if city in weathers.keys():
        # print(weathers[city])
        return city, weathers[city]
    else:
        print("There isn't the city in the list.")

def inquiry(txt_file):
    weathers = txt_to_dict(txt_file)
    inquiry_dict = {}

    while True:
        input_city = input("Please input city's name: ")
        if input_city in ["quit", "q", "Q"]:
            print_inquiry_dict(inquiry_dict)
            break
        elif input_city in ["help", "h", "H"]:
            print("""
            Input city name to get the weather;
            Input "help" to get the help information;
            Input "history" to get the information you inquiried;
            Input "quit" to quit the program.
            """)
        elif input_city in ["history", "his"]:
            print_inquiry_dict(inquiry_dict)
        else:
            if city_to_weather(weathers, input_city):
                c, w = city_to_weather(weathers, input_city)
                print(w)
                inquiry_dict[c] = w

inquiry('../resource/weather_info.txt')
