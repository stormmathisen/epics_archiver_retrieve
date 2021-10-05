import numpy as np # Import numpy to output numpy arrays instead of python lists
import requests # Import requests to access the file at the URL generated
from datetime import datetime # Import datetime to generate ISO 8601 timestamps

#datetime(year, month, day, hour, minute, second, millisecond) in UTC (not GMT, not BST)

fromTime = datetime(2021, 9, 8, 9, 0, 0, 0)
toTime = datetime(2021, 9, 8, 9, 1, 0, 0)
timespec = 'milliseconds'

print(fromTime.isoformat(timespec=timespec))
print(toTime.isoformat(timespec=timespec))

PV = 'CLA-S01-DIA-WCM-01:Q'
# This is a scalar, this scripts grabs one minute of scalars here and 10 seconds of waveforms further down

url = 'http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=' + PV + '&from='\
      + fromTime.isoformat(timespec=timespec) + 'Z&to=' + toTime.isoformat(timespec=timespec) + 'Z' # Create URL
print(url)

r = requests.get(url) # Get data at url
scalars = r.json() # Parse json

# Initialize arrays
values = []
time = []

for event in scalars[0]["data"]:
    time.append(event["secs"]+event["nanos"]*1E-9)
    values.append(event["val"])

scalar_values = np.array(values) # Numpy array of scalar values
scalar_times = np.array(time) # Numpy array of timestamps for scalar values as POSIX times (Seconds since 1970)

toTime = datetime(2021, 9, 8, 9, 0, 10, 0)

PV = 'CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ'
# This is an array

url = 'http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=' + PV + '&from='\
      + fromTime.isoformat(timespec=timespec) + 'Z&to=' + toTime.isoformat(timespec=timespec) + 'Z' # Create URL

print(url)

# Initialize arrays
values = []
time = []

r = requests.get(url)
waveforms = r.json()
dl = len(waveforms[0]["data"]) # Number of shots
lw = len(waveforms[0]["data"][0]["val"]) # Elements per array
values = np.empty((dl,lw))
time = np.empty((dl,1))
i = 0
for event in waveforms[0]["data"]:
    time[i] = event["secs"]+event["nanos"]*1E-9
    values[i,0:len(event["val"])] = event["val"]
    i += 1
wave_values = np.array(values)
wave_times = np.array(time)