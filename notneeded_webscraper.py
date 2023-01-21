import requests
from bs4 import BeautifulSoup


def scrape_for_gpu(gpu):
    url = "https://geizhals.de/?cat=gra16_512&asuch=" + gpu + "&bpmin=&bpmax=&v=e&hloc=de&plz=&dist=&mail=&bl1_id=30&togglecountry=set&sort=p#productlist"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    price_tags = soup.find_all(class_='gh_price')

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
