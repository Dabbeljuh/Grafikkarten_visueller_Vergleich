import time

import requests
from bs4 import BeautifulSoup

from json_handling import set_json_prices

# Define a custom header with a different user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def scrape_for_gpu(gpu):
    url = 'https://geizhals.de/?cat=gra16_512&asuch={gpu}&bpmin=&bpmax=&v=e&hloc=de&plz=&dist=&mail=&bl1_id=30' \
          '&togglecountry=set&sort=p#productlist'.format(gpu=gpu)

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    price_tags = soup.find_all(class_='gh_price', limit=5)

    price_list = []
    # Check if the request was successful
    if page.status_code == 200:
        # saves the prices as floats in a list and returns the list
        # converts german decimal point (,) to english (.) in order to convert to float
        for price in price_tags:
            # sometimes the price starts with "ab" and sometime not
            if price.text.split()[0] == "ab":
                temp = price.text.split()[2].replace(",", ".")
                price_list.append(float(temp))
            if price.text.split()[0] == "€":
                temp = price.text.split()[1].replace(",", ".")
                price_list.append(float(temp))
    else:
        # Print an error message if the request failed
        print("Request failed: ", page.status_code)
        return price_list, page.status_code

    return price_list, page.status_code


def query_each_gpu(gpu_list):
    # TODO: either check here for list or elsewhere?
    error_check = True
    for gpu in gpu_list:
        print(gpu)
        scraped_data = scrape_for_gpu(gpu)
        if scraped_data[1] == 200:
            set_json_prices(gpu, scraped_data[0])
        else:
            print("Request failed: ", str(scraped_data[1]))
        print(scraped_data)
        time.sleep(1)
    return error_check


def query_specific_gpu(gpu):
    print(gpu)
    scraped_data = scrape_for_gpu(gpu)
    if scraped_data[1] == 200:
        set_json_prices(gpu, scraped_data[0])
    else:
        print("Request failed: " + str(scraped_data[1]))

    print(scraped_data)

# print(json_handling.get_gpu_list_names_with_no_prices(json_file))
# query_each_gpu(json_handling.get_gpu_list_names(json_file))
# query_each_gpu(gpu_list=json_handling.get_gpu_list_names_with_no_prices(json_file=json_handling.json_today))
# query_specific_gpu('rx6600')
# query_each_gpu(json_handling.get_gpu_list_names_with_no_prices())
