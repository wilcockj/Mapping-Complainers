import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile
import os.path
from os import path
import sys
import os
#maybe get shapefile from us module
usa = geopandas.read_file("states_21basic/states.shp")
#world = geopandas.read_file(geopandas.datasets.get_path('nybb'))
#numberofcomplaints/populations
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
def download_file(url):
    local_filename = 'complaints.csv.zip'
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_length = r.headers.get('content-length')
        with open(local_filename, 'wb') as f:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                dl += len(chunk)
                f.write(chunk)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
    return local_filename
#nybb naturalearth_cities natural_earth_lowres
#world.head()

states = {"AL":0, "AK":0, "AZ":0, "AR":0, "CA":0, "CO":0, "CT":0, "DC":0, "DE":0, "FL":0, "GA":0, 
          "HI":0, "ID":0, "IL":0, "IN":0, "IA":0, "KS":0, "KY":0, "LA":0, "ME":0, "MD":0, 
          "MA":0, "MI":0, "MN":0, "MS":0, "MO":0, "MT":0, "NE":0, "NV":0, "NH":0, "NJ":0, 
          "NM":0, "NY":0, "NC":0, "ND":0, "OH":0, "OK":0, "OR":0, "PA":0, "RI":0, "SC":0, 
          "SD":0, "TN":0, "TX":0, "UT":0, "VT":0, "VA":0, "WA":0, "WV":0, "WI":0, "WY":0}
states2 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
populationbystate = [4903185,731545,7278717,3017825,39512223,5758735,3565287,705749,973764,
                    21477737,10617423,1415872,1792065,12671821,6732219,3155070,2913314,4467673,
                    4648794,1344212,6045680,6949503,9986857,5639632,2976149,6137428,
                    1068778,1934408,3080156,1359711,8882190,2096829,19453561,10488084,762062,11689100,
                    3956971,4217737,12801989,1059361,5148714,884659,6833659,28995881,3205958,623989,
                    8535519,7614893,1787147,5822434,578759]
if not path.isfile('complaints.csv'):
    if query_yes_no("Would you like to download the complaints dataset? It will be about 1.1gb once extracted."):
        print("Downloading File")
        download_file('https://files.consumerfinance.gov/ccdb/complaints.csv.zip')
        print("Extracting File")
        with zipfile.ZipFile('complaints.csv.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove('complaints.csv.zip')
    else:
        print("Can't continue without downloading dataset")
        exit()
complaintsdb = pd.read_csv("complaints.csv")

for x in complaintsdb['State']:
    if x in states:
        states[x] = states[x]+1
for count,x in enumerate(states2):
    #print(states[x])
    states[x] = (states[x]/populationbystate[count])*100000
fig,ax = plt.subplots(figsize=(30,30))
'''
for x in range(50):
    print("%s : %d" % (states2[x],populationbystate[x]))
'''
dfObj = pd.DataFrame(list(states.items()), index = states2)
dfObj.columns = ['STATE_ABBR','numcomplaints']
dfObj = dfObj.drop(['AK','HI','DC'])
print(dfObj)
usa = usa.merge(dfObj, on = 'STATE_ABBR')
print(usa)

plt.style.use('ggplot')
usa.plot(column= 'numcomplaints',ax=ax, legend=True)
plt.axis('off')
plt.title("Consumer Complaints per 100,000 people by State")
plt.show()
