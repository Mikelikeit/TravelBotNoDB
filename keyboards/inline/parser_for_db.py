import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from keyboards.inline.inline_data import list_url

sort_hotels_all_data = []


def get_data_with_selenium(url):
    option = Options()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(
        executable_path="/home/mike_like/my_dev/python/TGbots/TravelBotNoDB/keyboards/inline/chromedriver",
        options=option,
    )
    hotels_all_data = []
    try:
        driver.get(url=url)
        time.sleep(1)
        y = 0

        while y < 500:
            driver.execute_script(f'window.scrollBy(0, {y})')
            time.sleep(1)
            block = driver.find_elements_by_class_name('hotels-list-item')
            for name in block:
                name_hotel = name.find_element_by_class_name('HotelCardTitle__StyledHotelName-sc-1pgh6yo-0').text
                price_hotel = name.find_element_by_class_name('HotelCardPrice__StyledPrice-sc-4mork-2').text
                url_hotel = name.find_element_by_class_name('HotelCardTitle__StyledLink-sc-1pgh6yo-2').get_attribute(
                    'href')
                img_hotel = name.find_element_by_class_name(
                    'HotelCardGallery__StyledGaleryItem-sc-1ynzrrf-2').get_attribute('src')
                hotel_data = {
                    'name_hotel': name_hotel,
                    'price_hotel': price_hotel,
                    'url_hotel': url_hotel,
                    'img_hotel': img_hotel
                }

                hotels_all_data.append(hotel_data)

            y += 40

    except Exception as ex:
        print(ex)

    finally:
        for i in [*{x['name_hotel']: x for x in hotels_all_data}.values()]:
            sort_hotels_all_data.append(i)
        print(len(sort_hotels_all_data))
        driver.close()
        driver.quit()


def get_page(array, page: int = 1):
    page_index = page - 1
    return array[page_index]

# for i in list_url:
# print(i)
# get_data_with_selenium(i)
