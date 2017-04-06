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

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site
For this feature I have counted the bytes frequency and multiplied this frequency with maximum bytes consumed by each resource, and sorted the result in descending order. Because question asks for resources consuming most bandwidth.

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.


### Other considerations and optional features
It's critical that these features don't take too long to run. For example, if it took too long to detect three failed login attempts, further traffic from the same IP address couldn’t be blocked immediately, and that would present a security breach.
This dataset is inspired by real NASA web traffic, which is very similar to server logs from e-commerce and other sites. Monitoring web traffic and providing these analytics is a real business need, but it’s not the only thing you can do with the data. Feel free to implement additional features that you think might be useful.

## Details of Implementation
With this coding challenge, you should demonstrate a strong understanding of computer science fundamentals. We won't be wowed by your knowledge of various available software libraries, but will be impressed by your ability to pick and use the best data structures and algorithms for the job.

We're looking for clean, well-thought-out code that correctly implements the desired features in an optimized way and highlights your ability to write production-quality code.

We also want to see how you use your programming skills to solve business problems. At a minimum, you should implement the four required features, but feel free to expand upon this challenge or add other features you think would prevent fraud and further business goals. Be sure to document these add-ons so we know to look for them.

### Feature 1 
List in descending order the top 10 most active hosts/IP addresses that have accessed the site.

### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth. Bandwidth consumption can be extrapolated from bytes sent over the network and the frequency by which they were accessed.

### Feature 3 
To implement this feature I am checking all the timestamps from in each 60 minute window first timestamp value till the last timestamp in the file, with optimizations, however since I am checking for each window I am incrementing by 1second so this takes some time on big files. However, executes qickly on smaller ones.

### Feature 4 
For this feature I am first checking the failed logins in 20 seconds that have 401 reply code after that I am blocking all host for 5 minutes.


### Thank you
Thank you for this great challenge. I have worked very hard on this and I hope to be part of Insight Data Engineering.