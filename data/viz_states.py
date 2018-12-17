import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import pandas as pd
from matplotlib.colors import rgb2hex
import matplotlib.cm
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 350

import numpy as np
import sys


def plot_map(filep, title, state_idx=1):
    remove = ["Northern Mariana Islands", "US Virgin Islands", "Puerto Rico", "Guam", "x"]
    all_states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

    count_dict = dict()

    # read data file
    with open(filep) as dfile:
        dfile.readline()
        
        for line in dfile:
            line = line.strip().split('\t')
            
            if len(line[state_idx]) != 2:
                line[state_idx] = line[state_idx].split(',')[-1].strip()
                        
            if line[state_idx] in all_states:
                line[state_idx] = all_states[line[state_idx]]

                if line[state_idx] not in count_dict:
                    count_dict[line[state_idx]] = 0
                count_dict[line[state_idx]] += 1

    # normalize by z-score
    mean_v = np.mean(list(count_dict.values()))
    std_v = np.std(list(count_dict.values()))
    for s in count_dict:
        count_dict[s] = (count_dict[s] - mean_v)/std_v

    # create map
    fig, ax = plt.subplots(figsize=(10,6))
    m = Basemap(llcrnrlon=-119,llcrnrlat=19,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=29.5,lat_2=45.5,lon_0=-96)
    #shape files from https://www2.census.gov/geo/tiger/PREVGENZ/st/st00shp/st99_d00_shp.zip
    m.readshapefile('us_map/st99_d00', name='states', drawbounds=True)

    # states and colors
    cmap = plt.get_cmap("Oranges")
    cmin = min(count_dict.values())
    cmax = max(count_dict.values())
    norm = matplotlib.colors.Normalize(vmin=cmin, vmax=cmax)

    statenames = []
    colors = {}
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        if statename not in remove:
            colors[statename] = cmap(norm(count_dict.get(statename, 0)))[:3]
        statenames.append(statename)

    # plot
    for nshape, seg in enumerate(m.states):
#        print(statenames)
        if statenames[nshape] not in remove:
            color = rgb2hex(colors[statenames[nshape]])
            edge = "#000000"
            # translate alaska and hawaii
            if statenames[nshape] == 'Alaska':
                seg = [(0.35 * x + 1100000, 0.35 * y - 1300000) for x, y in seg]
            if statenames[nshape] == 'Hawaii':
                # remove small islands
                if (seg[0][1]) > 2.4e6: continue
                seg = [(x + 5400000, y - 1500000) for x, y in seg]
            poly = Polygon(seg, facecolor=color, edgecolor=edge, lw=0.5)
            ax.add_patch(poly)

    thing = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    thing.set_array([])
    #m.colorbar(thing)
    ax.set_title(title)
    plt.show()


# run user
plot_map('user.tsv', 'User Distributions',state_idx=1)
# run restaurant
#plot_map('rest_states.tsv', state_idx=5)
plot_map('restaurant.tsv', 'Restaurant Distributions', state_idx=5)
