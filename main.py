from json_handling import update_avg_price_and_price_per_performance as update_json
from data_visualiser import create_and_save_graph as show_image


if __name__ == '__main__':
    pass

# TODO: add better names i.e. 'rx6600xt' -> 'AMD Radeon RX 6600 XT'
# TODO: add performance metrics for 1080p, 1440p, 4k -> atm only 1440p
# TODO: add more options for average price -> atm only the average of the 5 cheapest
# TODO: if it gets no data from website, do something more

update_json()
show_image(save=True, show=True)