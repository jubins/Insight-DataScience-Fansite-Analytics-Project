'''
#Python3
@author: jubinsoni
@GitHub: https://www.github.com/jubins
#!Submission for: Insight-DataEngineering Challenge

#Dependencies: To run this code you need Python version 3.x and Pandas. Also set correct paths for Input and Output files below.
'''
import pandas as pd
import re
import datetime
import time
start = time.time()
#copy the file location and readlines
inputfile = 'C:/Users/jubin/Documents/Python Scripts/fansite-analytics-challenge-master/log_input/log.txt'
testfile = 'C:/Users/jubin/Documents/Python Scripts/fansite-analytics-challenge-master/insight_testsuite/tests/test_features/log_input/log.txt'
outputfile = 'C:/Users/jubin/Documents/Python Scripts/fansite-analytics-challenge-master/log_output/'

datafile= open(file=testfile,
                  encoding='utf-8',
                  errors='ignore').readlines()

#cleaning and pre-processing file to extract required information
start = time.time()
host = []
timestamp = []
request = []
httpReplyCode = []
bytes = []

for line in datafile:
    line_split = line.split(' - - ')
    host.append(line_split[0])
    timestamp.append(line_split[1].split(' ')[0].strip('['))
    request_temp = re.search(r'"([^"]*)"', line).group().split(' ')
    request.append(request_temp[1].strip('"') if len(request_temp)>1 else request_temp[0].strip('"'))
    httpcode_temp = re.sub('.*?([0-9]* [0-9]*)$',r'\1', line).split(" ")
    httpReplyCode.append(httpcode_temp[len(httpcode_temp)-2])
    bytes_temp = httpcode_temp[len(httpcode_temp)-1].strip('\n')
    bytes.append('0' if bytes_temp=='-' else bytes_temp)


#Creating a dataframe
start = time.time()
cols = ['host', 'timestamp', 'request', 'httpReplyCode', 'bytes']
httpReplyCode = list(map(int, httpReplyCode))
bytes = list(map(int,bytes))

df = pd.DataFrame({'host':host,
                  'timestamp':timestamp,
                  'request':request,
                  'httpReplyCode':httpReplyCode,
                  'bytes':bytes}, columns=cols)


#Feature 1: List the top 10 most active host/IP addresses that have accessed the site.
start = time.time()
host_df = df['host'].value_counts().head(10)
host_df.to_csv(outputfile+'hosts.txt', header=None, index=host_df.index.values.all(), sep=',', mode='w')


#Feature 2: Identify the 10 resources that consume the most bandwidth on the site.
frequency = df[['request', 'bytes']].groupby(by='request').count().reset_index()
bytesdata = df[['request', 'bytes']].sort_values(by='bytes',ascending=False)
resources = bytesdata.merge(frequency, on='request', how='inner', suffixes=('bytes','frequency'))
resources['totalbytes'] = resources['bytesbytes']*resources['bytesfrequency']
resources = resources.sort_values('totalbytes', ascending=False).request.drop_duplicates()[:10]
resources.to_csv(outputfile+'resources.txt', header=None, index=None, mode='w')



#3. List the top 10 busiest (or most frequently visited) 60-minute periods
import warnings
warnings.filterwarnings('ignore')

def getbusiest_timestamps(df):
    df_timestamp = df[['timestamp']]
    df_timestamp['date'] =df_timestamp['timestamp'].apply(lambda x: x.split(':')[0])
    busiest_dates = df_timestamp.groupby(by='date').count()['timestamp'].nlargest(10).index
    df_timestamp.set_index('date', drop=False, inplace=True)
    busiest_timestamps_list=[]
    for dates in busiest_dates:
        busiest_timestamps_list.append(df_timestamp.ix[dates]['timestamp'].values.tolist())
    busiest_timestamps_list = sum(busiest_timestamps_list,[])
    busiest_timestamps_list=sorted(busiest_timestamps_list, reverse=False)
    return busiest_timestamps_list

busiest_timestamps_list = getbusiest_timestamps(df)
start_time = busiest_timestamps_list[0]
end_time = busiest_timestamps_list[len(busiest_timestamps_list)-1]
end_time = datetime.datetime.strptime(end_time, "%d/%b/%Y:%H:%M:%S")
start_window = datetime.datetime.strptime(start_time, "%d/%b/%Y:%H:%M:%S")

busiest_hours = {}
while (start_window != end_time):
    count=0
    end_window = start_window + pd.Timedelta(seconds=3600)
    for time_stamp in busiest_timestamps_list:
        time_stamp = datetime.datetime.strptime(time_stamp, "%d/%b/%Y:%H:%M:%S")
        if time_stamp >= start_window and time_stamp <= end_window:
            count+=1
    busiest_hours[start_window.strftime('%d/%b/%Y:%H:%M:%S')+" -0400"] = count
    start_window = start_window + pd.Timedelta(seconds=1)

sorted_desc = sorted(busiest_hours, key=busiest_hours.get, reverse=True)

file = open(outputfile+"hours.txt", "w")
for h in sorted_desc[:10]:
    file.write(h+","+str(busiest_hours[h])+"\n")
file.close()



#Feature 4: Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.
def return_seconds(timestamp):
    timestamp = datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S").time()
    dt = timestamp
    (hr, mi, sec) = (dt.hour, dt.minute, dt.second)
    tsum = datetime.timedelta(hours=int(hr), minutes=int(mi), seconds=int(sec))
    return tsum.seconds


blocked_host = []
failed_IP_list = df[(df['httpReplyCode'] == 401)]['host'].unique()
failed_IP_df = df.copy()
failed_IP_df.reset_index(inplace=True)
failed_IP_df = failed_IP_df.set_index(keys='host')


# host='210.246.51.43'
# host='215.298.34.27'
def block(host):
    search_failed_IP = failed_IP_df.ix[host]
    if isinstance(search_failed_IP, pd.DataFrame):
        if (search_failed_IP[search_failed_IP['httpReplyCode'] == 401].shape[0]) > 3:
            time_values = search_failed_IP.set_index('index', drop=False)
            time_values = time_values[3:]['timestamp']
            seconds = (
            (return_seconds(time_values[2:3].values[0])) - return_seconds(time_values[0:1].values[0]) + pd.Timedelta(
                seconds=1).seconds)
            if len(time_values) == 4:
                fivemincheck = (
                return_seconds(time_values[3:4].values[0]) - return_seconds(time_values[2:3].values[0]) + pd.Timedelta(
                    seconds=1).seconds)
            if len(time_values) == 4 and fivemincheck > 300: time_values = time_values[:3]
            if len(time_values) > 4:
                for i, item in enumerate(time_values[3:]):
                    fivemincheck = (
                    return_seconds(time_values.iloc[i]) - return_seconds(time_values.iloc[i - 1]) + pd.Timedelta(
                        seconds=1).seconds)
                time_values = time_values[:3 + i - 1]
            if seconds <= 20:
                blocked_host.append(time_values.index.tolist())


list(map(block, failed_IP_list))
blocked_host = sum(blocked_host, [])

with open(outputfile + 'blocked.txt', 'w') as f:
    f.writelines(datafile[index] for index in blocked_host)

#print ("Total time: {0} seconds".format(time.time()-start))
#Thank you for this great challenge!
