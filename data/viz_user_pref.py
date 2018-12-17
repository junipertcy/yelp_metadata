import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ast
import pandas as pd
from collections import OrderedDict


def cal_score(column_idx=2, state_idx=5, cat_idx=-1):
    """Calculate average scores of user preferences for difference states

        column_idx (int): index of target column, either average score or average review counts.
            values might 2 (stars) or 3 (count) according to our data settings.
        cat_idx (int): index of restaurant category column
    """
    state_set = {
        'AZ', 'NV', 'NC', 'OH', 'PA'
    }

    type_set = {
        'Bars', 'American\n(Tra. & New)', 'Italian', 'Mexican', 'Chinese'
    }

    results = dict()

    with open('restaurant.tsv') as dfile:
        dfile.readline() # skip the column names
    
        for line in dfile:
            line = line.strip().split('\t')
            if line[state_idx] not in state_set:
                continue

            if line[state_idx] not in results:
                results[line[state_idx]] = dict()

            line[cat_idx] = ast.literal_eval(line[cat_idx])
            flag = False
            for ele in line[cat_idx]:
                if 'American' in ele:
                    ele = 'American\n(Tra. & New)'
                if ele not in type_set:
                    continue
                if ele not in results[line[state_idx]]:
                    results[line[state_idx]][ele] = []
                results[line[state_idx]][ele].append(float(line[column_idx]))
                break

    # average and normalization
    for state in results:
        for ele in results[state]:
            results[state][ele] = np.mean(results[state][ele])

    for state in results:
        total = sum(results[state].values())
        for ele in results[state]:
            results[state][ele] = results[state][ele]/total

    print(results)
    return results


def viz_heat(df, title='default', outpath='./test.pdf'):
    """
    Heatmap visualization
    :param df: an instance of pandas DataFrame
    :return:
    """
    a4_dims = (22.7, 12.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    sns.set(font_scale=1.2)
    viz_plot = sns.heatmap(df, annot=True, cbar=False, ax=ax, annot_kws={"size": 36}, cmap="Blues", vmin=df.values.min(), fmt='.3f')
    plt.xticks(rotation=0, fontsize=25)
    plt.yticks(rotation=40, fontsize=25)
    plt.xlabel('States', fontsize=30)
    plt.ylabel('Restaurant Types', fontsize=30)
    plt.title(title, fontsize=36)
    viz_plot.get_figure().savefig(outpath, format='pdf')
    plt.close()


if __name__ == '__main__':
    for idx, title in [(2, 'User Average Stars') , (3, 'User Review Average Counts')]:
        test = cal_score(column_idx=idx, state_idx=5, cat_idx=-1)
        df = pd.DataFrame(test)
        viz_heat(df, title, title+'.pdf')
