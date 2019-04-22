import requests
import json

CITIES = {'кольчугино': '546521', 'москва': '524901', 'владимир': '473247'}
PERIODS = {'погода сейчас': 'weather', 'на 3 дня с периодом 3 часа': 'forecast',
           'сутки по 3 часа': 'forecast'}


def get_weather(state):
    city = state[1]
    period = state[3]
    token = '1964414c84dbc3a8d4985dbbccdaa953'
    url = 'http://api.openweathermap.org/data/2.5/' + period
    params = {'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': token}
    r = requests.get(url, params)
    answer = r.json()
    return answer


def test_area(state):
    message = ''
    city = state[1]
    if city not in CITIES:
        message += 'Пожалуйста, проверьте, правильно ли введён город и повторите ввод.'
        state.pop(1)
    else:
        state[1] = CITIES[city]
        message = 'За какой период хотите узнать погоду?\n\n1) Погода сейчас\n2)' \
                  ' Сутки по 3 часа\n3) Трое суток с периодом 3 часа'
    return message, state


def test_period(state):
    message = ''
    period = state[2]
    if period not in PERIODS:
        state.pop(2)
        message += 'Пожалуйста, проверьте, правильно ли введён период и повторите ввод.'
    else:
        state.append(PERIODS[period])
    return message, state


def make_message(answer, state):
    period = state[3]
    message = ''
    if period == 'weather':
        message += weather_now(answer)
    elif period == 'forecast':
        if state[2] == 'трое суток с периодом 3 часа' or state[2] == '3':
             message += weather_few_days(answer['list'][:25])
        else:
            message += weather_few_days(answer['list'][:9])
    return message


def weather_now(answer):
    description = answer['weather'][0]['description']
    weather = answer['main']['temp']
    max = answer['main']['temp_max']
    min = answer['main']['temp_min']
    wind = answer['wind']['speed']
    humidity = answer['main']['humidity']
    data = 'Сейчас {}.\nНа улице {} градусов(от {} до {})' \
           '\nСкорость ветра {} м/с.\nВлажность {}%.' \
           ''.format(description, weather, min, max, wind, humidity)
    return data


def weather_few_days(answer):
    message = ''
    for period in answer:
        temp = period['main']['temp']
        description = period['weather'][0]['description']
        time = period['dt_txt']
        base = time[:11]
        last_time = time[-8:-6]
        if int(last_time[0]) > 0:
            new_time = int(last_time) + 3
        else:
            if int(last_time[1]) == 9:
                new_time = 12
            else:
                new_time = '0{}'.format(int(last_time[1]) + 3)
        if new_time == 24:
            new_time = '0{}'.format(0)
            last_date = time[8:11]
            new_date = int(last_date) + 1
            base = '{}{}{}'.format(time[:8], new_date, ' ')
        changed_time = '{}{}{}'.format(base, new_time, ':00:00')
        message += '{}\nСредняя температура: {}\nПогода: {}\n\n'.format(changed_time, temp, description)
    return message


def process(state):
    attachment = ''
    message = ''
    if len(state) == 1:
        message += 'В каком городе смотреть погоду?'
    elif len(state) == 2:
        message, state = test_area(state)
    elif len(state) == 3:
        message, state = test_period(state)
    if len(state) == 4:
        answer = get_weather(state)
        message = make_message(answer, state)
    return message #, state


if __name__ == '__main__':
    states = ['погода',  '524901', 'сутки по 3 часа']
    print(process(states))
