from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputMediaPhoto

from keyboards.inline.menu_keyboards import start_city_keyboard, current_month_keyboard, next_month1_keyboard, \
    next_month_2_keyboard, menu_cd, quantity_people_keyboard, quantity_night_keyboard, travel_country_keyboard, \
    travel_city_keyboard, tours_keyboard, pagination_call, get_page_keyboard

from keyboards.inline.parser_for_db import get_data_with_selenium, get_page, \
    sort_hotels_all_data

from loader import dp


@dp.message_handler(Command("travel"))
async def start_travel(message: types.Message):
    sort_hotels_all_data.clear()
    await get_start_city(message)


async def get_start_city(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await start_city_keyboard()
    if isinstance(message, types.Message):
        await message.answer("Начнем путешествие! Откуда вылетаем?", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Начнем путешествие! Откуда вылетаем?", reply_markup=markup)


async def get_current_month(callback: types.CallbackQuery, start_city, **kwargs):
    markup = await current_month_keyboard(start_city)
    await callback.message.edit_text("Когда вылетаем?", reply_markup=markup)


async def get_next_month1(callback: types.CallbackQuery, start_city, cur_month, **kwargs):
    markup = await next_month1_keyboard(start_city, cur_month)
    await callback.message.edit_reply_markup(markup)


async def get_next_month2(callback: types.CallbackQuery, start_city, cur_month, next_month1, **kwargs):
    markup = await next_month_2_keyboard(start_city, cur_month, next_month1)
    await callback.message.edit_reply_markup(markup)


async def get_quantity_people(callback: types.CallbackQuery, start_city, cur_month, next_month1, next_month2, day,
                              **kwargs):
    markup = await quantity_people_keyboard(start_city, cur_month, next_month1, next_month2, day)
    await callback.message.edit_text("Сколько вас?", reply_markup=markup)


async def get_quantity_night(callback: types.CallbackQuery, start_city, cur_month, next_month1, next_month2,
                             quantity_people, day, **kwargs):
    markup = await quantity_night_keyboard(start_city, cur_month, next_month1, next_month2, quantity_people, day)
    await callback.message.edit_text("На сколько ночей летите?", reply_markup=markup)


async def get_travel_country(callback: types.CallbackQuery, start_city, cur_month, next_month1, next_month2,
                             quantity_people, quantity_night, day, **kwargs):
    markup = await travel_country_keyboard(start_city, cur_month, next_month1, next_month2,
                                           quantity_people, quantity_night, day)
    await callback.message.edit_text("В какую страну полетим?", reply_markup=markup)


async def get_travel_city(callback: types.CallbackQuery, start_city, cur_month, next_month1, next_month2,
                          quantity_people, quantity_night, travel_country, day, **kwargs):
    markup = await travel_city_keyboard(start_city, cur_month, next_month1, next_month2,
                                        quantity_people, quantity_night, travel_country, day)
    await callback.message.edit_text("В какой город в выбранной стране?", reply_markup=markup)


async def get_tours(callback: types.CallbackQuery, start_city, cur_month, next_month1, next_month2, quantity_people,
                    quantity_night, travel_country, day, travel_city, **kwargs):
    await callback.message.edit_text("Подбираю тур! Подождите минутку")

    URL = f'https://level.travel/search/{start_city}-RU-to-{travel_city}-CY-departure-{day}.2021-for-{quantity_night}-nights-{quantity_people}-adults-0-kids-1..5-stars'
    print(URL)
    get_data_with_selenium(URL)

    # markup = await tours_keyboard(start_city, cur_month, next_month1, next_month2, quantity_people,
    # quantity_night, travel_country, day, travel_city)
    you_tours = get_page(sort_hotels_all_data)
    await callback.message.edit_text('Ваши туры готовы')
    await callback.message.answer_photo(photo=you_tours['img_hotel'], caption=f"{you_tours['name_hotel']}\n"
                                                                              f"{you_tours['price_hotel']}",
                                        reply_markup=get_page_keyboard(key="sort_hotels_all_data",
                                                                       max_pages=len(sort_hotels_all_data)))


@dp.callback_query_handler(pagination_call.filter(page='current_page'))
async def empty_page(call: types.CallbackQuery):
    await call.answer(cache_time=60)


@dp.callback_query_handler(pagination_call.filter(key='sort_hotels_all_data'))
async def tours_chose(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    current_page = int(callback_data.get("page"))
    you_tours = get_page(sort_hotels_all_data, page=current_page)
    media = InputMediaPhoto(you_tours['img_hotel'], caption=f"{you_tours['name_hotel']}\n"
                                                            f"{you_tours['price_hotel']}")
    await call.message.edit_media(media=media,
                                  reply_markup=get_page_keyboard(key="sort_hotels_all_data",
                                                                 max_pages=len(sort_hotels_all_data), page=current_page))


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    current_level = callback_data.get("level")
    start_city = callback_data.get("start_city")
    cur_month = callback_data.get("cur_month")
    next_month1 = callback_data.get("next_month1")
    next_month2 = callback_data.get("next_month2")
    quantity_people = callback_data.get("quantity_people")
    quantity_night = callback_data.get("quantity_night")
    travel_country = callback_data.get("travel_country")
    travel_city = callback_data.get("travel_city")
    day = callback_data.get("day")
    tours = callback_data.get("tours")

    levels = {
        "0": get_start_city,
        "1": get_current_month,
        "2": get_next_month1,
        "3": get_next_month2,
        "4": get_quantity_people,
        "5": get_quantity_night,
        "6": get_travel_country,
        "7": get_travel_city,
        "8": get_tours
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call,
        start_city=start_city,
        cur_month=cur_month,
        next_month1=next_month1,
        next_month2=next_month2,
        quantity_people=quantity_people,
        quantity_night=quantity_night,
        travel_country=travel_country,
        travel_city=travel_city,
        day=day,
        tours=tours
    )
