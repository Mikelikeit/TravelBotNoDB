import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_data_with_selenium(url):
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
        time.sleep(1)
        hotels_all_data = {}
        with open('selenium.html', 'w') as file:
            file.write(driver.page_source)
        with open('selenium.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        hotel_cards = soup.find_all('div', class_='hotels-list-item')

        for hotel_card in hotel_cards:
            name_hotel = hotel_card.find('span', class_='HotelCardTitle__StyledHotelName-sc-1pgh6yo-0').text
            price_hotel = hotel_card.find('span', class_='HotelCardPrice__StyledPrice-sc-4mork-2').text.replace(u'\xa0',
                                                                                                                u' ')
            if name_hotel not in hotels_all_data.keys():
                hotels_all_data[name_hotel] = {
                    'price_hotel': price_hotel
                }
        y = 240
        while y < 1200:
            driver.execute_script(f"window.scrollBy(0, {y})")
            time.sleep(0.5)
            with open('selenium.html', 'w') as file:
                file.write(driver.page_source)
            with open('selenium.html') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            hotel_cards = soup.find_all('div', class_='hotels-list-item')

            for hotel_card in hotel_cards:
                name_hotel = hotel_card.find('span', class_='HotelCardTitle__StyledHotelName-sc-1pgh6yo-0').text
                price_hotel = hotel_card.find('span', class_='HotelCardPrice__StyledPrice-sc-4mork-2').text.replace(
                    u'\xa0', u' ')
                if name_hotel not in hotels_all_data.keys():
                    hotels_all_data[name_hotel] = {
                        'price_hotel': price_hotel
                    }
            y += 40

        print(len(hotels_all_data))
        print(hotels_all_data)
    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

#get_data_with_selenium('https://level.travel/search/St.Petersburg-RU-to-Any-CY-departure-01.07.2021-for-7-nights-2-adults-0-kids-1..5-stars')