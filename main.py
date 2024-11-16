from data_visualiser import create_and_save_graph_average_price as show_save_avg
from data_visualiser import create_and_save_graph_cheapest_price as show_save_cheap
from geizhals_scraper import query_each_gpu as scrape_gpus
from json_handling import generate_new_json_for_today as new_json
from json_handling import get_gpu_list_names_with_no_prices as get_gpu_list
from json_handling import update_avg_price_and_price_per_performance as update_json

if __name__ == '__main__':
    new_json()
    if scrape_gpus(get_gpu_list()):
        update_json()
        show_save_avg(save=True, show=True)
        show_save_cheap(save=True, show=True)

# TODO: add performance metrics for 1080p, 1440p, 4k -> atm only 1440p
# TODO: add more options for average price -> atm only the average of the 5 cheapest
# TODO: fixing all typing (JSON typing??)
