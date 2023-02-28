import json
import os
from datetime import datetime

# today's date in YYYY/MM/DD format
today = datetime.now().isoformat().split("T")
save_path = os.path.dirname(__file__) + "/data_jsons/"
json_today_string = "gpus_" + str(today[0]) + ".json"
json_today = save_path + json_today_string


# checks if a json file with this name already exists
def where_json(file_name):
    return os.path.exists(file_name)


# copy the backup with blank prices in a new json file named after todays date
# if a file with today's date already exists skip the copying
def generate_new_json_for_today():
    if where_json(json_today):
        return True
    else:
        with open('gpus.json', "r+") as fromfile, open(json_today, "w+") as tofile:
            tofile.write(fromfile.read())


def read_json_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def get_gpu_list_names(json_file=json_today):
    file = read_json_file(json_file)
    gpu_name_list = []
    for gpu in file:
        gpu_name_list.append(gpu)
    return gpu_name_list


def get_gpu_list_names_with_no_prices(json_file=json_today):
    file = read_json_file(json_file)
    gpu_name_list = []
    for gpu in file:
        if len(file[gpu]['price']) == 0:
            gpu_name_list.append(gpu)
    return gpu_name_list


def get_price_list_for_gpu(gpu, json_file=json_today):
    file = read_json_file(json_file)
    if gpu in file:
        return file[gpu]['price']
    else:
        return 'gpu not in json file'


def set_json_prices(gpu, price, json_file=json_today):
    data = read_json_file(json_file)
    # TODO: more or less than 5 prices? and if handle it here or somewhere else
    if gpu in data and len(data[gpu]['price']) != 5:
        data[gpu].update({"price": price})

    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


# updates the prices for the gpu in the json file
def set_avg_prices(gpu, json_file=json_today):
    data = read_json_file(json_file)
    price_list = get_price_list_for_gpu(gpu)
    avg_price = round(sum(price_list) / len(price_list))
    # just checks if average price has not default of 0.0
    # TODO: try / except block probably better in all setter and getter
    if gpu in data and len(data[gpu]['price']) == 5 and data[gpu]['avg_price'] == 0.0:
        data[gpu].update({"avg_price": avg_price})
    else:
        # TODO: return string probably not really helpful
        return 'gpu not in data or prices not set or average price already set'
    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_average_price_for_gpu(gpu, json_file=json_today):
    file = read_json_file(json_file)
    # TODO: try / except block see set_avg_prices todo
    if gpu in file:
        return file[gpu]['avg_price']
    else:
        return 'gpu not in json file'


def set_price_per_performance(gpu, json_file=json_today):
    data = read_json_file(json_file)
    price_perf = get_average_price_for_gpu(gpu) / get_performance_for_gpu(gpu)
    if gpu in data and data[gpu]['price_per_performance'] == 0.0 and data[gpu]['avg_price'] != '0.0':
        data[gpu].update({"price_per_performance": round(price_perf, 2)})
    else:
        return 'gpu not in json file or already set or average price not done'
    # TODO: wiederholt sich oft, vielleicht bessere variante suchen?
    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_performance_for_gpu(gpu, json_file=json_today):
    file = read_json_file(json_file)
    if gpu in file:
        return file[gpu]['performance']
    else:
        return 'gpu not in json file'


# TODO: needs to run at startup somewhere
def update_avg_price_and_price_per_performance(json_file=json_today):
    file = read_json_file(json_file)
    for gpu in file:
        if file[gpu]['avg_price'] == 0.0:
            set_avg_prices(gpu, json_file)
        if file[gpu]['price_per_performance'] == 0.0:
            set_price_per_performance(gpu, json_file)


def get_sorted_list_by_price_per_performance_by_gpu_name_average_price(json_file=json_today):
    gpu_list = get_gpu_list_names()
    data = read_json_file(json_file)
    new_sorted_dict_by_price_per_performance = {}

    for gpu in gpu_list:
        new_sorted_dict_by_price_per_performance[gpu] = data[gpu]['price_per_performance']

    sorted_gpu = sorted(new_sorted_dict_by_price_per_performance.items(), key=lambda item: item[1], reverse=True)

    sorted_gpu_dict = {}
    for key, value in sorted_gpu:
        sorted_gpu_dict[key] = value

    return sorted_gpu_dict


def get_sorted_list_by_price_per_performance_by_gpu_name_cheapest_price(json_file=json_today):
    gpu_list = get_gpu_list_names()
    data = read_json_file(json_file)
    new_sorted_dict_by_price_per_performance = {}

    for gpu in gpu_list:
        new_sorted_dict_by_price_per_performance[gpu] = data[gpu]['price'][0] / data[gpu]['performance']

    sorted_gpu = sorted(new_sorted_dict_by_price_per_performance.items(), key=lambda item: item[1], reverse=True)

    sorted_gpu_dict = {}
    for key, value in sorted_gpu:
        sorted_gpu_dict[key] = value

    return sorted_gpu_dict

# print(get_sorted_list_by_price_per_performance_by_gpu_name())
# update_avg_price_and_price_per_performance()
# TODO: save jsons in jsons folder and not here


#generate_new_json_for_today()
