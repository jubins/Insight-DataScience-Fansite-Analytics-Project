# Table of Contents
1. Depenedencies
2. Code
3. Feature 1
4. Feature 2
5. Feature 3
6. Feature 4

# Dependencies
My entire code is in process_log.py file. To execute my code you need to have Python verion 3.x and I have used some external libraries like Pandas, and python packages like "re", "datetime" and "time".

#Code
I am first cleaning the log file and taking all the required features like host, request, reply code and bytes in a dataframe. Then I have implemented 4 features required for this challenge. On the logfile provided, my third and fourth feature takes some time to execute but the output is correct. For shorter files code gets executed pretty quickly. For each feature implemented in my code there is a comment above the code.

### Feature 1: 
To implement this feature I have counted the frequency of active hosts.

### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth. Bandwidth consumption can be extrapolated from bytes sent over the network and the frequency by which they were accessed.

### Feature 3 
To implement this feature I am checking all the timestamps from in each 60 minute window first timestamp value till the last timestamp in the file, with optimizations, however since I am checking for each window I am incrementing by 1second so this takes some time on big files. However, executes qickly on smaller ones.

### Feature 4 
For this feature I am first checking the failed logins in 20 seconds that have 401 reply code after that I am blocking all host for 5 minutes.


### Thank you
Thank you for this great challenge. I have worked very hard on this and I hope to be part of Insight Data Engineering.