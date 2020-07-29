import geopandas
import matplotlib.pyplot as plt
import pandas as pd
usa = geopandas.read_file("C:/Users/james/Desktop/misc files/states_21basic/states.shp")
world = geopandas.read_file(geopandas.datasets.get_path('nybb'))
#nybb naturalearth_cities natural_earth_lowres
world.head()
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
'''
complaintsdb = pd.read_csv("C:/Users/james/Desktop/misc files/Interesting data/complaints.csv")
for x in complaintsdb['State']:
    if x in states:
        states[x] = states[x]+1
'''
fig,ax = plt.subplots(figsize=(30,30))
for x in states:
    if x != "AK" and x != "HI":
        usa[usa.STATE_ABBR == f'{x}'].plot(ax=ax,edgecolor ='b',linewidth=2)
        print("%s : %d" % (x, states[x]))
#usa[usa.STATE_ABBR == 'OR'].plot()
#usa.plot(column=states)
plt.show()