#! /usr/bin/env python
#Author: R.B.Liu, C.Li @Brown Univ
#Last update: 2018-3-15
#This script is used to ingest two 2-column csv files and output the p-value of the two-tail student T-test.
#Each csv file should have one column of data ID and one column of data.
#Data ID in both csv files should match with each other.
#DO NOT include any header or comment in the csv files -- only put ID and data in them.
################################
import os, sys, math, re
import numpy as np
import csv
from scipy import stats

#parse command line inputs
if len(sys.argv) != 3:
    print >>sys.stderr, "Usage: python t-test.py {1st csv} {2nd csv} > {p-value txt} \nThe csv files should have NO headers with only ID and replicate columns!"
    exit(1);

csvFile1 = sys.argv[1]
csvFile2 = sys.argv[2]

# Define a 2-D array for each set of data
d1 = []
d2 = []

# Open the csv files and save the columns into array
with open(csvFile1) as csvData1:
    csvReader1 = csv.reader(csvData1)
    for row in csvReader1:
        d1.append(row)

with open(csvFile2) as csvData2:
    csvReader2 = csv.reader(csvData2)
    for row in csvReader2:
        d2.append(row)

# Convert the format of array from string to float
d1f = [[float(y or 0) for y in x] for x in d1]
d2f = [[float(y or 0) for y in x] for x in d2]

# Loop over all rows, and calculate T-test p-value for each row.
# Print ID and p-value in each row, the final output is a txt file.
for i in xrange(len(d1f)):
    print str(int(d1f[i][0])) + ' ' + str(stats.ttest_ind(d1f[i][1:], d2f[i][1:], equal_var = True)[1])

# p-value(equal_var=True) < p-value(equal_var=False)
# Same results with Excel T.TEST function (two-sample equal variance & unequal variance)
