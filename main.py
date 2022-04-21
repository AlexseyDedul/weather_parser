import bs4
import feedparser
import requests
import csv

main_filename = "./resourse/"

main_url = 'https://meteoinfo.ru'

list_cities = [
    {
        'city': 'Барановичи',
        'url': 'https://meteoinfo.ru/forecasts/belarus/baranovici'
    },
    {
        'city': 'Березино',
        'url': 'https://meteoinfo.ru/forecasts/belarus/berezino'
    },
    {
        'city': 'Бобруйск',
        'url': 'https://meteoinfo.ru/forecasts/belarus/bobruysr'
    },
    {
        'city': 'Борисов',
        'url': 'https://meteoinfo.ru/forecasts/belarus/borisov'
    },
    {
        'city': 'Брагин',
        'url': 'https://meteoinfo.ru/forecasts/belarus/bragin'
    },
    {
        'city': 'Брест',
        'url': 'https://meteoinfo.ru/forecasts/belarus/brest2'
    },
    {
        'city': 'Верхнидвинск',
        'url': 'https://meteoinfo.ru/forecasts/belarus/verhnedvinsk'
    },
    {
        'city': 'Витебск',
        'url': 'https://meteoinfo.ru/forecasts/belarus/vitebsk'
    },
    {
        'city': 'Гомель',
        'url': 'https://meteoinfo.ru/forecasts/belarus/somel'
    },
    {
        'city': 'Горки',
        'url': 'https://meteoinfo.ru/forecasts/belarus/gorki'
    },
    {
        'city': 'Гродно',
        'url': 'https://meteoinfo.ru/forecasts/belarus/grodno'
    },
    {
        'city': 'Докшицы',
        'url': 'https://meteoinfo.ru/forecasts/belarus/dokchicy'
    },
    {
        'city': 'Житковичи',
        'url': 'https://meteoinfo.ru/forecasts/belarus/zitkovici'
    },
    {
        'city': 'Жлобин',
        'url': 'https://meteoinfo.ru/forecasts/belarus/zlobin'
    },
    {
        'city': 'Кличев',
        'url': 'https://meteoinfo.ru/forecasts/belarus/klicev'
    },
    {
        'city': 'Костюковичи',
        'url': 'https://meteoinfo.ru/forecasts/belarus/kostjvkovici'
    },
    {
        'city': 'Лепель',
        'url': 'https://meteoinfo.ru/forecasts/belarus/lepel'
    },
    {
        'city': 'Лида',
        'url': 'https://meteoinfo.ru/forecasts/belarus/lida'
    },
    {
        'city': 'Лынтуры',
        'url': 'https://meteoinfo.ru/forecasts/belarus/lyntupy'
    },
    {
        'city': 'Марьина Горка',
        'url': 'https://meteoinfo.ru/forecasts/belarus/marina-gorka'
    },
    {
        'city': 'Минск',
        'url': 'https://meteoinfo.ru/forecasts/belarus/minsk'
    },
    {
        'city': 'Мозырь',
        'url': 'https://meteoinfo.ru/forecasts/belarus/mozyr'
    },
    {
        'city': 'Орша',
        'url': 'https://meteoinfo.ru/forecasts/belarus/orsa'
    },
    {
        'city': 'Пинск',
        'url': 'https://meteoinfo.ru/forecasts/belarus/pinsk'
    },
    {
        'city': 'Полоцк',
        'url': 'https://meteoinfo.ru/forecasts/belarus/polock'
    },
    {
        'city': 'Сенно',
        'url': 'https://meteoinfo.ru/forecasts/belarus/senno'
    },
    {
        'city': 'Славгород',
        'url': 'https://meteoinfo.ru/forecasts/belarus/slavgorod'
    },
    {
        'city': 'Слуцк',
        'url': 'https://meteoinfo.ru/forecasts/belarus/sluck'
    },
    {
        'city': 'Шарковщина',
        'url': 'https://meteoinfo.ru/forecasts/belarus/sarcovschina'
    }
]


def print_cities():
    counter = 0
    for city in list_cities:
        counter += 1
        print(f'{counter} - {city["city"]}')

    namber_city = input("Введите номер города: ")

    return list_cities[int(namber_city) - 1]


def get_rss_link(city: dict):
    response = requests.get(city['url'])
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    rss_link = soup.findAll('a')

    main_url_rss = ''

    for l in rss_link:
        if(l['href'].rfind('rss') == 1):
            main_url_rss = l['href']

    return main_url_rss


def get_weather_for_city():
    rss_url = main_url + get_rss_link(print_cities())
    text = feedparser.parse(rss_url)

    list_weather = []

    for t in text['entries']:
        title = t['title']
        summary = t['summary']

        list_weather.append({
            'title': title,
            'summary': summary
        })

    return list_weather


def save_to_file(filename, data):
    with open(filename, 'w', newline="") as file:
        writer = csv.DictWriter(file, data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        print("Файл записан.")


def read_from_file(filename):
    with open(filename, 'r', newline="") as file:
        reader = csv.DictReader(file)
        print("Чтение из файла")
        for row in reader:
            print(f"Город и день: {row['title']} - погода {row['summary']}")


def main():
    while True:
        data = get_weather_for_city()
        file = main_filename + data[0]['title']
        # print(data[0].keys())
        save_to_file(file, data)
        read_from_file(file)
        # for weather in data:
        #     print(weather)


if __name__ == '__main__':
    main()