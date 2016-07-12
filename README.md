# Insight_coding_challenge

## The solution file to this coding challenge is src/rolling_median.py 
#### Python 3 is used, therefore the environment needs to have it installed

### Overview of what src/rolling_median.py does:
##### Note that steps 2 through 6 is performed for each transaction
##### Note that EDGE_LIST is a list of lists with the format: [ [timestamp1,['actor1','target1']], [timestamp2,['actor2','target2']], ...etc]

1.     Get transactions. Then for each transaction, do the following:
2.     Check validity of entry - If it's missing actor or target, or if actor==target, ignore and drop it
3.     Check and update timestamp: 
  3.    If timestamp is older than 60s, jump to call calc_median_degree() to end. This is done in accordance with what the FAQ said about still outputting a median value for each transaction even if the transaction is outside 60-second window
  3.     If timestamp is newer than newest, update the global newest_timestamp value
4.     Delete edges that are older than 60 seconds. O(n) runtime complexity because the edgelist is not sorted by timestamp (it's not sorted at all). A b-tree will bring it to O(log n) for each insertion and deletion, but will require resorting.
5.     Insert each new edge entry into edge_list, checking that this new entry doesn't already exist.
  5.    Sort each edge (target, actor) alphabetically, since this is an undirected graph (e.g {target,actor} is equal to {actor,target})
  5.    Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order of the edge because each edge entry is already sorted). O(n) runtime complexity because edgelist is not sorted by edges (where an edge is: node name - node name).
6.     Call calc_median_degree()
  6.    Concatenate the 2 columns of nodes in the edge_list to get list of all nodes with duplicates
  6.    Use python's counter to count number of occurence of each node to get the degree count for each node. O(n) runtime complexity because this list is unsorted, so it's just a linear search. This list of counts is also unsorted.
  6.    Then use python's statistics package to get the median. Probably O(n log n) complexity because requires sorting. Maybe can be done in O(n) time using median-of-medians algorithm, but there's some discussion in the python community about whether it's actually faster, so I stuck with python's statistics library. See https://bugs.python.org/issue21592 and http://stackoverflow.com/questions/10662013/finding-the-median-of-an-unsorted-array

### src/rolling_median.py already imports all the pacakges it needs. 

The following packages are used/imported:
* import time - needed to deal with timestamps
* import sys - for reading the arugments of the run.sh command
* import json - for processing json
* import os - for checking if output.txt already exists, and deleting it if it does
* from collections import Counter - used for counting number of occurences in edgelist to get the vertex of a node
* import statistics  - used for finding the median
* import pdb - python debugger, used for debugging

#### Note that this repo started off as a clone of https://github.com/InsightDataScience/coding-challenge

For testing, call "./run_tests.sh" from within the insight_testsuite directory