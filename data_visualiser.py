import os.path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style

from json_handling import get_sorted_list_by_price_per_performance_by_gpu_name_average_price as sorted_list
from json_handling import get_sorted_list_by_price_per_performance_by_gpu_name_cheapest_price as cheap_sorted_list
from json_handling import json_today
from json_handling import json_today_string
from json_handling import read_json_file


def create_and_save_graph_average_price(json_file=json_today, show=True, save=False, overwrite=False):
    gpu_sorted_list = sorted_list()
    gpu = read_json_file(json_file)

    style.use('seaborn-v0_8-dark')
    # style.use('ggplot')

    bar_width = 0.2
    fig, ax = plt.subplots(figsize=(15, 8))

    ax.set_title("Cost Per Frame: 1440p Euro [" + json_today + "]\n" + "6 Games Average, Medium Quality Settings\n"
                 + "Cost Per Frame                              Average FPS\n")

    for i in gpu_sorted_list:
        if i.startswith('rtx'):
            pcolor = '#76b900'
            pppcolor = 'green'
        else:
            pcolor = '#ED1C24'
            pppcolor = 'darkred'

        ax.barh(i + " " + str(gpu[i]['avg_price']) + " €", gpu[i]['performance'], color=pcolor)
        ax.barh(i + " " + str(gpu[i]['avg_price']) + " €", gpu[i]['price_per_performance'] * 10, color=pppcolor)

    rects = ax.patches
    for rect in rects:
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # diffrent label settings for price and performance
        if type(x_value) == np.float64:
            label = "{:.2f}".format(x_value / 10).replace(".", ",") + " €"
            label_color = 'white'
            ha = "right"
            space = -5
        else:
            label = x_value
            label_color = 'black'
            ha = "left"
            space = 2

        plt.annotate(label,
                     (x_value, y_value),
                     xytext=(space, 0),
                     textcoords="offset points",
                     va='center',
                     ha=ha,
                     color=label_color)

    if save:
        save_path = os.path.dirname(__file__) + "/graph_pngs/"
        save_name = json_today_string.replace(".json", ".png")
        check = save_path + save_name

        if os.path.exists(check) and overwrite:
            plt.savefig(check)
        if os.path.exists(check) and not overwrite:
            pass
        if not os.path.exists(check):
            plt.savefig(check)

    if show:
        plt.show()


def create_and_save_graph_cheapest_price(json_file=json_today, show=True, save=False, overwrite=False):
    gpu_sorted_list = cheap_sorted_list()
    gpu = read_json_file(json_file)

    style.use('seaborn-v0_8-dark')

    bar_width = 0.2
    fig, ax = plt.subplots(figsize=(15, 8))

    ax.set_title(
        "Cheapest Cost Per Frame: 1440p Euro [" + json_today + "]\n" + "6 Games Average, Medium Quality Settings\n"
        + "Cost Per Frame                              Average FPS\n")

    for i in gpu_sorted_list:
        if i.startswith('rtx'):
            pcolor = '#76b900'
            pppcolor = 'green'
        else:
            pcolor = '#ED1C24'
            pppcolor = 'darkred'
        ax.barh(i + " " + str(gpu[i]['price'][0]) + " €", gpu[i]['performance'], color=pcolor)
        ax.barh(i + " " + str(gpu[i]['price'][0]) + " €", gpu[i]['price'][0] / gpu[i]['performance'] * 10,
                color=pppcolor)

    rects = ax.patches
    for rect in rects:
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # diffrent label settings for price and performance
        if type(x_value) == np.float64:
            label = "{:.2f}".format(x_value / 10).replace(".", ",") + " €"
            label_color = 'white'
            ha = "right"
            space = -5
        else:
            label = x_value
            label_color = 'black'
            ha = "left"
            space = 2

        plt.annotate(label,
                     (x_value, y_value),
                     xytext=(space, 0),
                     textcoords="offset points",
                     va='center',
                     ha=ha,
                     color=label_color)

    if save:
        save_path = os.path.dirname(__file__) + "/graph_pngs/"
        save_name = 'cheapest_' + json_today_string.replace(".json", ".png")
        check = save_path + save_name

        if os.path.exists(check) and overwrite:
            plt.savefig(check)
        if os.path.exists(check) and not overwrite:
            pass
        if not os.path.exists(check):
            plt.savefig(check)

    if show:
        plt.show()
