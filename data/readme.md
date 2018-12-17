# Running Platform:
Python 3.6, Ubuntu 16.04, [Anaconda](https://www.anaconda.com/download/#linux)

# Install required packages
Make sure to install Anaconda first. Then run the following:
* Install [basemap](https://github.com/matplotlib/basemap): `pip install --user git+https://github.com/matplotlib/basemap.git`
* `conda install --yes --file requirements.txt`


# Dataset
You have to request the data via email <xiaolei.huang@colorado.edu>

# How to Run:
1. Build data & crawl: You need to request.
2. Visualizations:
    * state visualization in the Paper *Geographic attributes inference*: `python viz_states.py`
    * user preference visualization *User preferences*: `python viz_user_pref.py`
    * user location visualization *User locations*: `python viz_user_source.py`
3. Check the top ranking restaurant types:
    * `ipython`
    * `import pickle`
    * `counts = pickle.load(open('./counts/rest_rank_types.pkl', 'rb'))`
    * `print(counts.most_common(10))`
