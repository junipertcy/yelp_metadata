"""
    This script is to visualize user sources (region level) for the restaurants in four states: AZ, NV, NC, OH, PA

    5 states * 4 regions heat map
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ast
import pandas as pd
from collections import OrderedDict
import json
import os


def cal_rest_state():
    region_dict = {
        'South': {'DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'},
        'Northeast': {'CT', 'ME', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA', 'MA', 'DC'},
        'Midwest': {'IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'},
        'West': {'AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA'},
    }

    state_set = {'AZ', 'NV', 'NC', 'OH', 'PA'}

    user_dict = dict()
    rest_dict = dict()
    results = dict()

    # load user information
    with open('user.tsv') as dfile:
        dfile.readline()
        for line in dfile:
            line = line.strip().split('\t')
            
            # encode the location to region
            line[1] = line[1].split(',')[-1].strip()
            for key in region_dict:
                if line[1] in region_dict[key]:
                    user_dict[line[0]] = key

    # load restaurant information
    with open('restaurant.tsv') as dfile:
        dfile.readline()
        for line in dfile:
            line = line.strip().split('\t')

            # only keep the five states
            if line[5] not in state_set:
                continue               
            for key in region_dict:
                if line[5] in region_dict[key]:
                    # region and state as the dictionary values
                    rest_dict[line[0]] = line[5]

    # load the edges to count the edge distributions
    with open('edge.tsv') as dfile:
        dfile.readline()
        
        for line in dfile:
            line = line.strip().split('\t')
            if len(line) != 9:
                continue         

            # filter out the restaurants not in the five states
            if line[1] not in rest_dict:
                continue

            # filter out the users not in the four regions
            if line[0] not in user_dict:
                continue

            # count the results
            if rest_dict[line[1]] not in results:
                results[rest_dict[line[1]]] = {}
            if user_dict[line[0]] not in results[rest_dict[line[1]]]:
#                results[rest_dict[line[1]]][user_dict[line[0]]] = 0
#            results[rest_dict[line[1]]][user_dict[line[0]]] += 1
                results[rest_dict[line[1]]][user_dict[line[0]]] = set()
            results[rest_dict[line[1]]][user_dict[line[0]]].add(line[0])

    # count
    for state in results:
        for region in results[state]:
            results[state][region] = len(results[state][region])

    # normalize
    for state in results:
        total = sum(results[state].values())
        for region in results[state]:
            results[state][region] = results[state][region]/total

    print(results)
    return results


def viz_heat(df, title='default', outpath='./test.pdf'):
    """
    Heatmap visualization
    :param df: an instance of pandas DataFrame
    :return:
    """
    a4_dims = (15.7, 12.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    sns.set(font_scale=1.2)
    viz_plot = sns.heatmap(df, annot=True, cbar=False, ax=ax, annot_kws={"size": 36}, cmap="Blues", vmin=df.values.min(), fmt='.3f')
    plt.xticks(rotation=0, fontsize=25)
    plt.yticks(rotation=40, fontsize=25)
    plt.xlabel('States', fontsize=30)
    plt.ylabel('US Regions', fontsize=30)
    plt.title(title, fontsize=36)
    viz_plot.get_figure().savefig(outpath, format='pdf')
    plt.close()


if __name__ == '__main__':
    if not os.path.exists('./count/user_source.json'):
        results = cal_rest_state()
        json.dump(results, open('./count/user_source.json', 'w'))
    else:
        results = json.load(open('./count/user_source.json'))
    df = pd.DataFrame(results)
    viz_heat(df, 'Region Distributions of Restaurant Comsumers')
