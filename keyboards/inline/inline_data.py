import calendar
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

now_date = datetime.datetime.now()
c = calendar.TextCalendar()

start_city_data = {"Москва": "Moscow",
                   "Санкт-Петербург": "St.Petersburg"}

quantity_people_data = {"Я один": 1,
                        "Нас двое": 2}

quantity_night_data = {"3 ночи": 3,
                       "7 ночей": 7,
                       "11 ночей": 11,
                       "14 ночей": 14}

travel_country_data = {"Кипр": "CY",
                       "Абхазия": "AB",
                       "ОАЭ": "AE",
                       "Египет": "EG"}

travel_city_data = {
    "CY": {
        "Ларнака": "Larnaca",
        "Айа-Напа": "Ayia.Napa"
    }
}

list_url = []
for start_city in start_city_data.items():
    for quantity_people in quantity_people_data.items():
        for quantity_night in quantity_night_data.items():
            for travel_country in travel_country_data.items():
                for day in c.itermonthdays(now_date.year, now_date.month + 1):
                    if day != 0 and day > now_date.day + 7:
                        url = f'https://level.travel/search/{start_city[1]}-RU-to-Any-{travel_country[1]}-departure-{day}.{now_date.month}.{now_date.year}-for-{quantity_night[1]}-nights-{quantity_people[1]}-adults-0-kids-1..5-stars'
                        list_url.append(url)


def get_data_with_selenium(url):
    print(datetime.datetime.now())
    option = Options()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        executable_path="/home/mike_like/my_dev/python/TGbots/TravelBotNoDB/keyboards/inline/chromedriver",
        options=option,
    )
    try:
        driver.get(url=url)
        time.sleep(3.5)
        y = 240
        while y < 900:
            driver.execute_script(f'window.scrollBy(0, {y})')
            time.sleep(1.5)
            block = driver.find_elements_by_class_name('hotels-list-item')
            for name in block:
                print(name.find_element_by_class_name('HotelCardTitle__StyledHotelName-sc-1pgh6yo-0').text)
            y += 50

    except Exception as ex:
        print(ex)

    finally:
        print(datetime.datetime.now())
        driver.close()
        driver.quit()


#for i in list_url:
   # print(i)
   # get_data_with_selenium(i)
