# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 16:47:53 2018

@author: adrian mascorro
"""

import csv
import numpy as np
import pandas as pd
from scipy import stats , integrate
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes = True)

#open csv file containing voter registration information for Oregon
with open('vrd.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    
    #dictionary containing dictionary of counties
    countyD = {}
    #skip the header
    next(spamreader, None)
    #read the rows in vdr.csv
    for row in spamreader:
        #split first element in row to get county
        countytokenM = row[0].split(',', 3)
        #split last element in row to get the party name
        partytokenM = row[-1].split(',', 3)
        #if the first element in last row element is num, pop it
        if partytokenM[0].isdecimal():
            partytokenM.pop(0)
        
        #certain parties were listed as other names. I cleaned them up
        #Independent party is listed as party in file
        if partytokenM[0] == "Party":
            partytokenM[0] = "Independent Party"
        #Pacific Green is listed as Green in file
        if partytokenM[0] == "Green":
            partytokenM[0] = "Pacific Green"
        #partisan is NonPartisan, but similar to NonAffiliated, so I am grouping them
        if partytokenM[0] == "Partisan":
            partytokenM[0] = "Nonaffiliated"
        #Elect is Americans Elect
        if partytokenM[0] == "Elect":
            partytokenM[0] = "Americans Elect"
        #Oregon is Working Families Party of Oregon
        if partytokenM[0] == "Oregon":
            partytokenM[0] = "Working Families Party of Oregon"
        
        #skip "Other" party as it offers no valuable information
        if partytokenM[0] == "Other":
            continue
        
        #if county isn't in countyD, add it and add nested dict to it
        if countytokenM[0] not in countyD:
            countyD[countytokenM[0]] = {}
        else:
            #check if party is in nested dict for county. if not, adds it
            if partytokenM[0] not in countyD[countytokenM[0]]:
                #sets the count for the party to 0
                countyD[countytokenM[0]][partytokenM[0]] = 0
            else:
                #adds to the party count in that county
                countyD[countytokenM[0]][partytokenM[0]] = countyD[countytokenM[0]][partytokenM[0]] + 1
    partydf = pd.DataFrame(countyD).T
    partydf.fillna(0, inplace=True)
    #print(partydf)
    #partydf['Republican'].T.plot.bar()
    #plt.show()
    
#open U.S. census data for walkability
with open('walkability.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(spamreader, None)
    count = 0
    
    #CSA Dictionary
    CSAdict = {}
    
    #county Dictionary
    countyD = {'001':"BAKER", '003':"BENTON", '005':"CLACKAMAS", '007':"CLATSOP",
               '009':"COLUMBIA", '011':"COOS", '013':"CROOK", '015':"CURRY", '017':"DESCHUTES",
               '019':"DOUGLAS", '021':"GILLIAM", '023':"GRANT", '025':"HARNEY", '027':"HOOD RIVER",
               '029':"JACKSON", '031':"JEFFERSON", '033':"JOSEPHINE", '035':"KLAMATH",
               '037':"LAKE", '039':"LANE", '041':"LINCOLN", '043':"LINN", '045':"MALHEUR",
               '047':"MARION", '049':"MORROW", '051':"MULTNOMAH", '053':"POLK", '055':"SHERMAN",
               '057':"TILLAMOOK", '059':"UMATILLA", '061':"UNION", '063':"WALLOWA", '065':"WASCO",
               '067':"WASHINGTON", '069':"WHEELER", '071':"YAMHILL"}
    
    #only take in the required county and state number, i.e., only read rows with census data for Oregon
    for row in spamreader:
        count = count + 1
        WalktokenM = row[-1].split(',',len(row[-1]))
        CitytokenM = row[0].split(',',len(row[0]))
        countyNum = CitytokenM[3][1:-1]
        stateNum = CitytokenM[4][1:-1]

        
        #Census state ID is 41. File has it saved as a string
        if stateNum != "41":
            continue   
        
        #convert this string value to number
        WalkI = float(WalktokenM[-4]) #f float(WalktokenM[-1])
        
        if CitytokenM[-2] == '':
            continue
        
        
        #adjust CitytokenM[-2] to not include quotation
        if CitytokenM[-2][0] in ("\""):
            CitytokenM[-2] = CitytokenM[-2][1:]
            #print(CitytokenM[-2])
        
            
        #check if county name is in CSAdict. if not, initialize it and add elements
        if countyD[countyNum] not in CSAdict:
            #empty dict with county name 
            CSAdict[countyD[countyNum]] = {}
            #aggregate walk total 
            CSAdict[countyD[countyNum]]["AggWalk"] = WalkI
            #count how many times county is in csv file
            CSAdict[countyD[countyNum]]["Count"] = 1
            #average is set to 0
            CSAdict[countyD[countyNum]]["Average"] = 0
        #county exists in CSAdict, so add to the aggregate walk num and to the num of times county is in csv file
        else:
            CSAdict[countyD[countyNum]]["AggWalk"] = CSAdict[countyD[countyNum]]["AggWalk"] + WalkI
            CSAdict[countyD[countyNum]]["Count"] = CSAdict[countyD[countyNum]]["Count"] + 1
        #print(CitytokenM," walk\n",WalktokenM, "\n")
    #average the aggwalk and count
    for i in CSAdict:
        CSAdict[i]["Average"] = CSAdict[i]["AggWalk"] / CSAdict[i]["Count"]
                
    #use pandas to print dataframe
    countydf = pd.DataFrame(CSAdict).T
    countydf.fillna(0, inplace=True)
    
    """the following v, w, x, y, and z display a distplot for the Democratic, Republican, 
       Pacific Green, Libertarian, and Consitution Parties
    """
    v = []
    v.append(partydf['Libertarian'])
    sns.distplot(v)
    
    w = []
    w.append(partydf['Constitution'])
    sns.distplot(w)
    
    x = []
    x.append(partydf['Pacific Green'])
    sns.distplot(x)
    
    y = []
    y.append(partydf['Republican'])
    sns.distplot(y)
    
    z = []
    z.append(partydf['Democrat'])
    sns.distplot(z)
    
    """ the following v, w, x, y, and z display a joinplot for the Democratic, Republican, 
       Pacific Green, Libertarian, and Consitution Parties
    """
    sns.jointplot(x="Average",y=partydf['Democrat'],data=countydf);
    sns.jointplot(x="Average",y=partydf['Republican'],data=countydf);
    sns.jointplot(x="Average",y=partydf['Pacific Green'],data=countydf);
    sns.jointplot(x="Average",y=partydf['Libertarian'],data=countydf);
    sns.jointplot(x="Average",y=partydf['Constitution'],data=countydf);
   
    
    
