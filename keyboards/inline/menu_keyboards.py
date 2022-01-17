import calendar
import datetime

import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from config import open_weather_token
from keyboards.inline.inline_data import start_city_data, quantity_people_data, quantity_night_data, \
    travel_country_data, travel_city_data
from keyboards.inline.parser_for_db import sort_hotels_all_data

now_date = datetime.datetime.now()
c = calendar.TextCalendar()

menu_cd = CallbackData("show_menu", "level", "start_city", "cur_month", "next_month1", "next_month2", "day",
                       "quantity_people", "quantity_night", "travel_country", "travel_city", "tours")

pagination_call = CallbackData("paginator", "key", "page")


def make_callback_data(level, start_city=0, cur_month=0, next_month1=0, next_month2=0, day=0, quantity_people=1,
                       quantity_night=7, travel_country=0, travel_city=0, tours=0):
    return menu_cd.new(level=level,
                       start_city=start_city,
                       cur_month=cur_month,
                       next_month1=next_month1,
                       next_month2=next_month2,
                       day=day,
                       quantity_people=quantity_people,
                       quantity_night=quantity_night,
                       travel_country=travel_country,
                       travel_city=travel_city,
                       tours=tours,
                       )


async def start_city_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)

    for key in start_city_data:
        button_text = f"{key}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           start_city=start_city_data[key])

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def current_month_keyboard(start_city):
    CURRENT_LEVEL = 1
    current_month = []
    markup = InlineKeyboardMarkup(row_width=7)

    for day in c.itermonthdays(now_date.year, now_date.month):
        if day == 0 or day < now_date.day:
            day = ' '
            current_month.append(day)
        else:
            current_month.append(day)

    for w in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        button_text = f'{w}'
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL))
        )
    for i in current_month:
        button_text = f'{i}'
        if button_text != ' ':
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL + 3,
                                                                                        day=f'{int(i)}.{int(now_date.month)}',
                                                                                        start_city=start_city))
            )
        else:
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL,
                                                                                        day=i))
            )
    markup.insert(
        InlineKeyboardButton(text=" ", callback_data=make_callback_data(level=CURRENT_LEVEL)))

    markup.insert(
        InlineKeyboardButton(text=f"{calendar.month_name[now_date.month]}", callback_data=make_callback_data(
            level=CURRENT_LEVEL)))

    markup.insert(
        InlineKeyboardButton(text=">>", callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                         start_city=start_city,
                                                                         cur_month=now_date.month))
    )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )

    return markup


async def next_month1_keyboard(start_city, cur_month):
    CURRENT_LEVEL = 2
    current_month = []
    new_year_month = 1
    markup = InlineKeyboardMarkup(row_width=7)
    if now_date.month == 12:
        for day in c.itermonthdays(now_date.year + 1, new_year_month):
            if day == 0:
                day = ' '
                current_month.append(day)
            else:
                current_month.append(day)
    else:
        for day in c.itermonthdays(now_date.year, now_date.month + 1):
            if day == 0:
                day = ' '
                current_month.append(day)
            else:
                current_month.append(day)

    for w in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        button_text = f'{w}'
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL))
        )
    for i in current_month:
        button_text = f'{i}'
        if button_text != ' ':
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL + 2,
                                                                                        day=f'{int(i)}.{int(now_date.month + 1)}',
                                                                                        start_city=start_city))
            )
        else:
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL,
                                                                                        day=i))
            )
    markup.insert(
        InlineKeyboardButton(text="<<", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    if now_date.month == 12:
        markup.insert(
            InlineKeyboardButton(text=f"{calendar.month_name[new_year_month]}", callback_data=make_callback_data(
                level=CURRENT_LEVEL)))

        markup.insert(
            InlineKeyboardButton(text=">>", callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                             start_city=start_city,
                                                                             cur_month=cur_month,
                                                                             next_month1=new_year_month))
        )
    else:
        markup.insert(
            InlineKeyboardButton(text=f"{calendar.month_name[now_date.month + 1]}", callback_data=make_callback_data(
                level=CURRENT_LEVEL)))

        markup.insert(
            InlineKeyboardButton(text=">>", callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                             start_city=start_city,
                                                                             cur_month=cur_month,
                                                                             next_month1=now_date.month + 1))
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 2))
    )

    return markup


async def next_month_2_keyboard(start_city, cur_month, next_month1):
    CURRENT_LEVEL = 3
    current_month = []
    new_year_month = 1
    markup = InlineKeyboardMarkup(row_width=7)
    if now_date.month == 12:
        for day in c.itermonthdays(now_date.year + 1, new_year_month + 1):
            if day == 0:
                day = ' '
                current_month.append(day)
            else:
                current_month.append(day)
    else:
        for day in c.itermonthdays(now_date.year, now_date.month + 2):
            if day == 0:
                day = ' '
                current_month.append(day)
            else:
                current_month.append(day)

    for w in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        button_text = f'{w}'
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL))
        )
    for i in current_month:
        button_text = f'{i}'
        if button_text != ' ':
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                                        day=f'{int(i)}.{int(now_date.month + 2)}',
                                                                                        start_city=start_city))
            )
        else:
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=make_callback_data(level=CURRENT_LEVEL,
                                                                                        day=i))
            )
    markup.insert(
        InlineKeyboardButton(text="<<", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                         cur_month=cur_month)))
    if now_date.month == 12:
        markup.insert(
            InlineKeyboardButton(text=f"{calendar.month_name[new_year_month + 1]}", callback_data=make_callback_data(
                level=CURRENT_LEVEL)))

        markup.insert(
            InlineKeyboardButton(text=" ", callback_data=make_callback_data(level=CURRENT_LEVEL,
                                                                            start_city=start_city,
                                                                            cur_month=cur_month,
                                                                            next_month1=next_month1,
                                                                            next_month2=new_year_month + 1))
        )
    else:
        markup.insert(
            InlineKeyboardButton(text=f"{calendar.month_name[now_date.month + 2]}", callback_data=make_callback_data(
                level=CURRENT_LEVEL)))

        markup.insert(
            InlineKeyboardButton(text=" ", callback_data=make_callback_data(level=CURRENT_LEVEL,
                                                                            start_city=start_city,
                                                                            cur_month=cur_month,
                                                                            next_month1=next_month1,
                                                                            next_month2=now_date.month + 2))
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 3))
    )

    return markup


async def quantity_people_keyboard(start_city, cur_month, next_month1, next_month2, day):
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup(row_width=2)

    for key in quantity_people_data:
        button_text = f"{key}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           quantity_people=quantity_people_data[key],
                                           start_city=start_city,
                                           cur_month=cur_month,
                                           next_month1=next_month1,
                                           next_month2=next_month2,
                                           day=day

                                           )

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 3,
                                                                            start_city=start_city))
    )

    return markup


async def quantity_night_keyboard(start_city, cur_month, next_month1, next_month2, quantity_people, day):
    CURRENT_LEVEL = 5
    markup = InlineKeyboardMarkup(row_width=2)

    for key in quantity_night_data:
        button_text = f"{key}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           quantity_night=quantity_night_data[key],
                                           start_city=start_city,
                                           cur_month=cur_month,
                                           next_month1=next_month1,
                                           next_month2=next_month2,
                                           quantity_people=quantity_people,
                                           day=day
                                           )

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            start_city=start_city,
                                                                            cur_month=cur_month,
                                                                            next_month1=next_month1,
                                                                            next_month2=next_month2,
                                                                            ))
    )

    return markup


async def travel_country_keyboard(start_city, cur_month, next_month1, next_month2, quantity_people, quantity_night,
                                  day):
    CURRENT_LEVEL = 6
    markup = InlineKeyboardMarkup(row_width=1)

    for key in travel_country_data:
        button_text = f"{key}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           start_city=start_city,
                                           cur_month=cur_month,
                                           next_month1=next_month1,
                                           next_month2=next_month2,
                                           quantity_people=quantity_people,
                                           quantity_night=quantity_night,
                                           day=day,
                                           travel_country=travel_country_data[key])

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            start_city=start_city,
                                                                            cur_month=cur_month,
                                                                            next_month1=next_month1,
                                                                            next_month2=next_month2,
                                                                            quantity_people=quantity_people))
    )

    return markup


async def travel_city_keyboard(start_city, cur_month, next_month1, next_month2,
                               quantity_people, quantity_night, travel_country, day):
    CURRENT_LEVEL = 7
    markup = InlineKeyboardMarkup(row_width=1)

    for key in travel_city_data[travel_country]:
        def get_weather(city, open_weather_token):
            global wd
            code_to_smile = {
                "Clear": "\U00002600",
                "Clouds": "\U00002601",
                "Rain": "\U00002614",
                "Drizzle": "\00002614",
                "Thunderstorm": "\000026A1",
                "Snow": "\U00001F328",
                "Mist": "\U00001F32B"
            }
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            )
            data = r.json()
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]

            return cur_weather, wd

        if travel_city_data[travel_country][key] == "Ayia.Napa":
            rename_city = "Ayia Napa"
            weather = get_weather(rename_city, open_weather_token)
        else:
            weather = get_weather(travel_city_data[travel_country][key], open_weather_token)
        button_text = f"{key} \n" \
                      f"{weather[1]} {weather[0]}℃"

        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           start_city=start_city,
                                           cur_month=cur_month,
                                           next_month1=next_month1,
                                           next_month2=next_month2,
                                           quantity_people=quantity_people,
                                           quantity_night=quantity_night,
                                           travel_country=travel_country,
                                           day=day,
                                           travel_city=travel_city_data[travel_country][key])
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text='Все города', callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                                 start_city=start_city,
                                                                                 cur_month=cur_month,
                                                                                 next_month1=next_month1,
                                                                                 next_month2=next_month2,
                                                                                 quantity_people=quantity_people,
                                                                                 quantity_night=quantity_night,
                                                                                 travel_country=travel_country,
                                                                                 day=day,
                                                                                 travel_city='Any'))
    )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            start_city=start_city,
                                                                            cur_month=cur_month,
                                                                            next_month1=next_month1,
                                                                            next_month2=next_month2,
                                                                            quantity_people=quantity_people,
                                                                            quantity_night=quantity_night))
    )

    return markup


async def tours_keyboard(start_city, cur_month, next_month1, next_month2,
                         quantity_people, quantity_night, travel_country, day, travel_city,
                         ):
    CURRENT_LEVEL = 8


def get_page_keyboard(max_pages: int, key="sort_hotels_all_data", page: int = 1):
    previous_page = page - 1
    previous_page_text = "<< "

    current_page = page
    current_page_text = f'<{page}>'

    next_page = page + 1
    next_page_text = " >>"

    markup = InlineKeyboardMarkup()
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_call.new(key=key, page='current_page')
        )
    )
    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Купить",
            url=sort_hotels_all_data[current_page - 1]['url_hotel']
        )
    )

    return markup
