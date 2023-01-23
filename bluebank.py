import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
This document processes the data from res/loan_data_json.json and writes the processed data to res/loan_cleaned.csv.
"""

# Reads in json file into the data frame
json_file = open('res/loan_data_json.json')
data = json.load(json_file)
loandata = pd.DataFrame(data)

# Gets the actual annual income
loandata['annual.income'] = np.exp(loandata['log.annual.inc'])

# Iterates over the loan data frame and creates the fico.category column
length = len(loandata)
ficocat = []

for x in range(0, length):
    category = loandata['fico'][x]
    try:
        if 300 <= category < 400:
            cat = 'Very Poor'
        elif 400 <= category < 600:
            cat = 'Poor'
        elif 601 <= category < 660:
            cat = 'Fair'
        elif 660 <= category < 700:
            cat = 'Good'
        elif category >= 700:
            cat = 'Excellent'
        else:
            cat = 'Unknown'
    except:
        cat = 'Unknown'
    ficocat.append(cat)

ficocat = pd.Series(ficocat)
loandata['fico.category'] = ficocat

# Iterates over the loan data frame and creates the int.rate.type column
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

# Finds the number of loans by fico.category and purpose
catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar(color='green', width=0.3)
plt.show()

purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color='red', width=0.3)
plt.show()

# Finds the distribution of annual incomes
ypoint = loandata['annual.income']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint)
plt.show()

# Writes the loan data to a csv file
loandata.to_csv('res/loan_cleaned.csv', index=True)
