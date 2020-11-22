#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.set_option('display.max_columns', 75)


# In[2]:


nbaData_path="/Users/guanlxy/Desktop/NBASalary/"
temp=pd.read_csv(nbaData_path+"NBAdata.csv")
stats=temp.copy()
stats=stats.drop("#", axis=1)
stats=stats.drop("blank2", axis=1)
stats=stats.drop("blanl", axis=1)



stats.rename(columns={"Season Start": "Season"}, inplace=True)
stats.rename(columns={"Tm": "Team"}, inplace=True)
stats.rename(columns={"Player Name": "Name"}, inplace=True)
stats.rename(columns={"Player Salary in $": "Salary"}, inplace=True)
stats.rename(columns={"G": "GP"}, inplace=True)

#mapping numeric values onto positions
mapping = {'PG': 1, 'SG': 2, 'SF': 3, 'PF': 4, 'C':5}
stats['Pos'] = stats['Pos'].map(mapping)


# In[3]:


#ratio of Games started to games played
stats["GS/GP"]=stats["GS"]/stats["GP"]

#removing last row from dataset because it's null
stats=stats[:-1]


# In[4]:


#stats should be a on a per-game basis instead of totals to eliminate the effect of games played
stats["MPG"]=stats["MP"]/stats["GP"]
stats["ORPG"]=stats["ORB"]/stats["GP"]
stats["DRPG"]=stats["DRB"]/stats["GP"]
stats["RPG"]=stats["TRB"]/stats["GP"]
stats["APG"]=stats["AST"]/stats["GP"]
stats["SPG"]=stats["STL"]/stats["GP"]
stats["BPG"]=stats["BLK"]/stats["GP"]
stats["TPG"]=stats["TOV"]/stats["GP"]
stats["PFPG"]=stats["PF"]/stats["GP"]
stats["PPG"]=stats["PTS"]/stats["GP"]
stats["FGPG"]=stats["FG"]/stats["GP"]
stats["FGAPG"]=stats["FGA"]/stats["GP"]
stats["3PPG"]=stats["3P"]/stats["GP"]
stats["3PAPG"]=stats["3PA"]/stats["GP"]
stats["2PPG"]=stats["2P"]/stats["GP"]
stats["2PAPG"]=stats["2PA"]/stats["GP"]
stats["FTPG"]=stats["FT"]/stats["GP"]
stats["FTAPG"]=stats["FTA"]/stats["GP"]

#drop all total columns
drop_column = ['MP', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA']
stats.drop(drop_column, axis=1, inplace = True)


# In[5]:


#splitting stats into 3 categories for later on, when looking at which group of stats is the best predictor of salary
advanced=['% of Cap','PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']
regular=['% of Cap','ORPG', 'DRPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'PFPG', 'PPG', 'FGPG', 'FGAPG', '3PPG', '3PAPG', '2PPG', '2PAPG', 'FTPG', 'FTAPG']
basic=['% of Cap','Pos', 'Age', 'MPG', 'GP']

#change salary from object to float
stats["Salary"] = stats.Salary.astype(float)

#removed stars from some players names
stats['Name'] = stats['Name'].map(lambda x: x.rstrip('*'))


# In[6]:


#dataset had total stats for a player if he was on two teams in one season, but we wanted to look at data on specific teams, too, so the "TOT" value wouldn't work
stats=stats[~stats["Team"].str.contains("TOT", na=False)]

#players don't qualify if they've played in less than or equal to 15 games on a team
stats=stats[stats['GP']>15]

#if no salary is in the dataset, we can't use that row
stats=stats.dropna(subset = ['Salary'])


#if a player still had a NaN at this point, it meant they didn't take any shots that season, so give them values of 0s for the percentages columns
empty=['TS%','3PAr','FTr','TOV%','FG%','3P%','2P%','eFG%','FT%']
for i in empty:
    stats[i].fillna(0, inplace=True)


# In[7]:


#teams have changed names and locations over the years, this is keeping the franchises consistent
stats["Team"].replace("CHH", "NOP", inplace=True)
stats["Team"].replace("NOH", "NOP", inplace=True)
stats["Team"].replace("NOK", "NOP", inplace=True)
stats["Team"].replace("NJN", "BRK", inplace=True)
stats["Team"].replace("WSB", "WAS", inplace=True)
stats["Team"].replace("SEA", "OKC", inplace=True)
stats["Team"].replace("VAN", "MEM", inplace=True)
stats["Team"].replace("CHA", "CHO", inplace=True)
len(stats["Team"].unique())
#now only thirty teams in the league


# In[8]:


#salary cap for all years from 1995 to 2017
from pandas import *
my_dic = pd.read_excel('/Users/guanlxy/Desktop/NBASalaryPredictions-master/salaryCap.xlsx', index_col=0).to_dict()
cap=my_dic['Salary Cap']


# In[9]:


#to normalize salaries, make them as a percentage of the salary cap in that year
stats['Cap'] = stats['Season'].map(cap)
stats['% of Cap']=(stats['Salary']/stats['Cap'])*100


# In[10]:


stats.to_csv(nbaData_path+'nbasalary.csv')

