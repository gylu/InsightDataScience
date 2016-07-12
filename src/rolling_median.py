#!/usr/bin/env python3

# Example of program that calculates the  median degree of a venmo transaction graph

# Overview of what this code does:
# 1.     Get transactions

# 2.     Check validity of entry. If it's missing actor or target, ignore and drop it

# 3.     Check and update timestamp: 
# 3a.    If timestamp is older than 60s, drop, jump to call calc_median_degree() to end. This is done in accordance with what the FAQ said about still outputting a value for the median for each valid transaction even if outside 60-second window
# 3b.     If timestamp is newer than newest, update newest_timestamp value

# 4.     Delete edges that are older than 60 seconds

# 5.     Insert each new edge entry into edge_list:
# 5a.    Sort each edge(target/actor) alphabetically, since this is undirected
# 5b.    Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order, because each edge entry is already sorted)

# 6.     Call calc_median_degree()
# 6a.    Concatenate the 2 columns of nodes in the edge_list
# 6b.    Use python's counter to count number of occurence of each node in the edgelist, to get the degree count for each node
# 6c.    Then use python's statistics package to get the median

#Note that /venmo_input/venmo-trans.txt is listed in gitignore because it's so big


####### Implementation of the above outline #######
import sys
import os
import json #use for json parser
import time #needed to deal with timestamps
import statistics
from collections import Counter
import pdb

sys_argv0 = sys.argv[0]
sys_argv1 = sys.argv[1] #'./venmo_input/venmo-trans.txt'
sys_argv2 = sys.argv[2] #'./venmo_output/output.txt'

NEWEST_TIMESTAMP=0.00 #global vairable
EDGE_LIST=[] #of the format: [ [timestamp1,['actor1','target1']], [timestamp2,['actor2','target2']], ...etc]
OUTPUT_FILE=""
DEBUG=False
if DEBUG: print("\nStarted")

def main():
    global NEWEST_TIMESTAMP
    global EDGE_LIST
    global OUTPUT_FILE
    global DEBUG
    if os.path.exists(sys_argv2):
        os.remove(sys_argv2) #clear out old ./venmo_output/output.txt file. note that the location is based on where run.sh was called
    OUTPUT_FILE = open(sys_argv2, 'a+')

    #1. Get all transactions
    #future optimization: this may be able to be optimized to process one-at-a-time as each json object line in the text file is read
    transactions = []
    for line in open(sys_argv1, 'r'): #2. Check validity, check for empty actors or targets
        line_json_parsed = json.loads(line)
        if line_json_parsed['actor']!="" and line_json_parsed['target']!="" and line_json_parsed['actor']!=line_json_parsed['target']: #2 Make sure actor and target fields exist
            transactions.append(line_json_parsed)

    for transaction in transactions:
        #pdb.set_trace() 
        actor = transaction['actor']
        target = transaction['target']
        transaction_timestamp = time.mktime(time.strptime(transaction['created_time'],"%Y-%m-%dT%H:%M:%SZ"))
        if DEBUG: print("\nNew transactionTimestamp: ",transaction_timestamp);
        if (check_and_update_timestamp(transaction_timestamp)):     #3. Check and update timestamp. Note that this created_time field is always utc time
            if DEBUG: print("updated NEWEST_TIMESTAMP: ",NEWEST_TIMESTAMP)
            if DEBUG: print("EDGE_LIST before clean: ", EDGE_LIST)
            EDGE_LIST = [entry for entry in EDGE_LIST if entry[0] > NEWEST_TIMESTAMP-60] #4. Delete edges that are older than 60 seconds
            if DEBUG: print("EDGE_LIST after clean: ", EDGE_LIST) 
            update_edge_list(transaction_timestamp,sorted([actor,target])); # 5.      Insert each new edge entry into edge_list
            if DEBUG: print("EDGE_LIST after update: ", EDGE_LIST)
        calc_median_degree(); # 6.     Call calc_median_degree()
    OUTPUT_FILE.close();





####### Functions are defined here #######

# 3.     Check and update timestamp: 
# 3a.    If timestamp is older than 60s, drop, jump to call calc_median_degree() to end. This is done in accordance with what the FAQ said about still outputting a value for the median for each transaction even if it's outside 60-second window
# 3b.    If timestamp is newer than newest, update newest_timestamp value
def check_and_update_timestamp( timestampToBeChecked_epoch_utc ): 
    global NEWEST_TIMESTAMP
    if DEBUG: print("prev NEWEST_TIMESTAMP: ",NEWEST_TIMESTAMP)
    if (timestampToBeChecked_epoch_utc < NEWEST_TIMESTAMP-60):
        return False
    elif (timestampToBeChecked_epoch_utc > NEWEST_TIMESTAMP):
        NEWEST_TIMESTAMP=timestampToBeChecked_epoch_utc;
    return True #whether or not this was the newest timestamp or just a valid one, return true
 

# 5.     Insert each new edge entry into edge_list:
# 5a.    Sort each edge(target/actor) alphabetically, since this is undirected (already done)
# 5b.    Check that the edge doesn't already exist, if it does, update timestamp of that edge (no need to check for reverse order, because each edge entry is already sorted)
def update_edge_list(transaction_timestamp,new_edge_to_be_added):
    global EDGE_LIST
    edge_doesnt_exist_yet=True;
    for element in EDGE_LIST:
        if (element[1]==new_edge_to_be_added):
            edge_doesnt_exist_yet=False;
            if(element[0]<transaction_timestamp):
                element[0]= transaction_timestamp;
            break;
    if edge_doesnt_exist_yet: #looped through whole existing EDGE_LIST and didn't break out of loop, meaning this is a new edge
        EDGE_LIST.append([transaction_timestamp,new_edge_to_be_added])
    return True;

# 6.     Call calc_median_degree()
# 6a.    Concatenate the 2 columns of nodes in the edge_list
# 6b.    Use python's counter to count number of occurence of each node in the edgelist, to get the degree count for each node
# 6c.    Then use python's statistics package to get the median
def calc_median_degree():
    global EDGE_LIST
    global OUTPUT_FILE
    all_edges=getColumn(EDGE_LIST,1)
    list_of_all_nodes_with_duplicates = [item for sublist in all_edges for item in sublist] #Concatenate the 2 columns of nodes. Followed this: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    counts_of_occurences=list(Counter(list_of_all_nodes_with_duplicates).values()) # 6b.    Use python's counter to count number of occurence of each node in the edgelist, to get the degree count for each node
    if DEBUG: print("counts_of_occurences: ",counts_of_occurences)
    median_degree_untruncated=statistics.median(counts_of_occurences) # 6c.    Then use python's statistics package to get the median
    before_decimal, after_decimal = str('%.3f'%(median_degree_untruncated)).split('.')
    median_degree='.'.join((before_decimal, after_decimal[0:2]))
    OUTPUT_FILE.write(median_degree)
    OUTPUT_FILE.write("\n")
    return True;

#helper function for getting columns
def getColumn(matrix, i):
    return [row[i] for row in matrix]



if __name__ == "__main__":
    main()
