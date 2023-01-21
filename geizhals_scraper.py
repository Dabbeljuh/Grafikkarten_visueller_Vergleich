import time

import requests
from bs4 import BeautifulSoup

from json_handling import get_gpu_list_names_with_no_prices as get_gpu_list
from json_handling import json_today
from json_handling import set_json_prices




def scrape_for_gpu(gpu):
    # TODO: maybe alternative for geizhals needed, after ~4-7 queries no answer and you need to change proxy -> now at around the 3060
    url = "https://geizhals.de/?cat=gra16_512&asuch=" + gpu + "&bpmin=&bpmax=&v=e&hloc=de&plz=&dist=&mail=&bl1_id=30&togglecountry=set&sort=p#productlist"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    price_tags = soup.find_all(class_='gh_price', limit=5)

    price_list = []
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

    return price_list


def query_each_gpu(gpu_list):
    # TODO: either check here for list or elsewhere?
    for gpu in gpu_list:
        print(gpu)
        temp = scrape_for_gpu(gpu)
        print(temp)
        set_json_prices(gpu, temp)
        # slowing down not get blocked -> not as successful -> workaround: waiting an unknown time or change VPN
        time.sleep(5)


def query_specific_gpu(gpu):
    print(gpu)
    temp = scrape_for_gpu(gpu)
    print(temp)
    set_json_prices(gpu, temp)


# print(json_handling.get_gpu_list_names_with_no_prices(json_file))

# query_each_gpu(json_handling.get_gpu_list_names(json_file))

#query_each_gpu(gpu_list=json_handling.get_gpu_list_names_with_no_prices(json_file=json_handling.json_today))

#query_specific_gpu('rx6600')

query_each_gpu(get_gpu_list(json_today))

