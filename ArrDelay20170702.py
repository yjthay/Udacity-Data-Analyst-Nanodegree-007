import os
import pandas as pd
import numpy as np
os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Data Analyst/Submissions/007/flight data")

#df = pd.read_csv("2008.csv", usecols =['UniqueCarrier','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay','Year','Month'])
#df = df.fillna(0)
#['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']
#table = df.pivot_table(values = 'CarrierDelay', index =['Year','Month'], columns =  ['UniqueCarrier'],aggfunc = np.sum)


output= pd.DataFrame()
for yr in [i for i in xrange(1995,2009)]:
    fname = str(yr)+".csv"
    #df = pd.read_csv(fname, usecols =['UniqueCarrier','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay','Year','Month','Origin','ArrDelay','DepDelay'])
    df = pd.read_csv(fname, usecols =['UniqueCarrier','Year','Month','Origin','ArrDelay','DepDelay'])
    df = df.fillna(0)
    #df['AllDelays'] = df['CarrierDelay']+ df['WeatherDelay']+df['NASDelay']+df['SecurityDelay']+df['LateAircraftDelay']
    table = df.pivot_table(values = 'ArrDelay', index =['Origin','Month','Year'],aggfunc = np.sum)
    table2 = df.pivot_table(values = 'ArrDelay', index =['Origin','Month','Year'],aggfunc = np.count_nonzero)
    table2.name = 'TotalFlights'
    results = pd.concat([table, table2],axis=1)
    if len(output)==0:
        output = pd.DataFrame(results)
    else:
        output = pd.concat([output,pd.DataFrame(results)],axis=0)

# File from http://ourairports.com/data/
airports = pd.DataFrame.from_csv('airports.csv')
states = pd.DataFrame.from_csv('states.csv')
# Looking at just US/ Puerto Rico Airports
airports = airports[airports.iso_country.isin(['US','PR'])]


output['Lat']=np.nan
output['Long']=np.nan
output['State']=np.nan
for i in set(output.index.get_level_values('Origin')):
    try:
        output.ix[output.index.get_level_values('Origin')==i,'Lat'] = airports[airports.iata_code==i].latitude_deg.iloc[0]
        output.ix[output.index.get_level_values('Origin')==i,'Long'] = airports[airports.iata_code==i].longitude_deg.iloc[0]
        state = airports[airports.iata_code==i].iso_region.iloc[0].split('-')[1]
        state = states[states.Abbreviation==state].index[0]
        output.ix[output.index.get_level_values('Origin')==i,'State'] = state
    except:
        #try:
            #output.ix[output.index.get_level_values('Origin')==i,'lat'] = airports[airports.local_code==i].latitude_deg.iloc[0]
            #output.ix[output.index.get_level_values('Origin')==i,'long'] = airports[airports.local_code==i].longitude_deg.iloc[0]
            #output.ix[output.index.get_level_values('Origin')==i,'state'] = airports[airports.local_code==i].iso_region.iloc[0]
        #except:
        output.ix[output.index.get_level_values('Origin')==i,'Lat'] = np.nan
        output.ix[output.index.get_level_values('Origin')==i,'Long'] = np.nan
        output.ix[output.index.get_level_values('Origin')==i,'State'] = np.nan
        print i + " has no state/lat/long and thus dropped"


# Remove Hawaii and Alaska (as they are too far out)
output.ix[output.State=='Hawaii'] = np.nan
output.ix[output.State=='Alaska'] = np.nan

output = output.dropna()


output.to_csv('C:/Users/YJ/Documents/1) Learning/Udacity - Data Analyst/Submissions/007/ArrDelays.csv')

