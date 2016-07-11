# Insight_coding_challenge

## The solution file to this coding challenge is src/rolling_median.py 
#### Python 3 is used, therefore the environment needs to have it installed

### Overview of what src/rolling_median.py does:
##### Note that steps 2 through 6 is performed for each transaction
##### Note that EDGE_LIST is a list of lists with the format: [ [timestamp1,['actor1','target1']], [timestamp2,['actor2','target2']], ...etc]

1.     Get transactions
2.     Check validity of entry. If it's missing actor or target, ignore and drop it
3.     Check and update timestamp: 
  3.    If timestamp is older than 60s, drop, jump to call calc_median_degree() to end. This is done in accordance with what the FAQ said about still outputting a value for the median for each valid transaction even if outside 60-second window
  3.     If timestamp is newer than newest, update newest_timestamp value
4.     Delete edges that are older than 60 seconds
5.     Insert each new edge entry into edge_list:
  5.    Sort each edge(target/actor) alphabetically, since this is undirected
  5.    Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order, because each edge entry is already sorted)
6.     Call calc_median_degree()
  6.    Concatenate the 2 columns of nodes in the edge_list
  6.    Use python's counter to count number of occurence of each node in the edgelist, to get the degree count for each node
  6.    Then use python's statistics package to get the median

### src/rolling_median.py already imports all the pacakges it needs. 

The following packages are used/imported:

* import time - needed to deal with timestamps
* import sys - for reading the arugments of the run.sh command
* import json - for processing json
* import os - for checking if output.txt already exists, and deleting it if it does
* from itertools import combinations - used to run combinations (order doesn't matter), Taken from: https://rosettacode.org/wiki/Combinations#Python
* import statistics  - used for finding the median
* from collections import Counter - used for counting number of occurences in edgelist to get the vertex of a node
* import pdb - python debugger, used for debugging

#### Note that this repo started off as a clone of https://github.com/InsightDataScience/coding-challenge

For testing, call "./run_tests.sh" from within the insight_testsuite directory