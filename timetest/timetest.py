# Austin Griffith
# Sudoku Solver Time Tester


import numpy as np
import pandas as pd
import random
import time
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats

import reduction as rd
import backtrack as bt
import backtracknp as btnp


#%%
data = pd.read_csv('normal.csv',dtype=str).drop('solutions',axis=1)

samples = 5
seed = 10071994
random.seed(903353429)
rand = random.sample(range(data.shape[0]),samples)
sampledata = data.iloc[rand].reset_index(drop=True)['quizzes']

maintest = []
normfile = 'normtemp.csv'

for s in sampledata:
    singletest = []
    
    n = 9
    temp = [s[i:i+n] for i in range(0, len(s), n)]
    puzzle = []
    for t in temp:
        puzzle.append([t[i] for i in range(0, len(t))])
    pd.DataFrame(puzzle).to_csv(normfile,index=False,header=False)


    singletest.append(rd.mainout(normfile))
    singletest.append(bt.mainout(normfile))
    singletest.append(btnp.mainout(normfile))
    
    maintest.append(singletest)
    
    
col = ['Red','Bktk','Bktk NP']
times = pd.DataFrame(maintest,columns=col)

#%%

#times.to_csv('times.csv')
times = pd.read_csv('times.csv')


#%%
# plot the time to complete for each method
resol = 200

sns.distplot(times['Red'],kde=False)
plt.title('Reduction Method Time to Complete')
plt.xlabel('Time [s]')
plt.ylabel('Frequency')
plt.savefig('reduction.png', dpi=resol, bbox_inches='tight')
plt.close()


sns.distplot(times['Bktk'],kde=False)
plt.title('Backtrack Method Time to Complete')
plt.xlabel('Time [s]')
plt.ylabel('Frequency')
plt.savefig('back.png', dpi=resol, bbox_inches='tight')
plt.close()


sns.distplot(times['Bktk NP'],kde=False)
plt.title('Backtrack Numpy Method Time to Complete')
plt.xlabel('Time [s]')
plt.ylabel('Frequency')
plt.savefig('backnp.png', dpi=resol, bbox_inches='tight')
plt.close()

#%%
# hard sudokus
datahard = pd.read_csv('hardest.csv')
datahard['sudoku'] = datahard['sudoku'].str.replace('.','0')

samples = 1
seed = 10071994
random.seed(903353429)
rand = random.sample(range(datahard.shape[0]),samples)
sampleharddata = datahard.iloc[rand].reset_index(drop=True)['sudoku']

maintesthard = []
hardfile = 'hardtemp.csv'

for s in sampleharddata:
    singletest = []
    
    n = 9
    temp = [s[i:i+n] for i in range(0, len(s), n)]
    puzzle = []
    for t in temp:
        puzzle.append([t[i] for i in range(0, len(t))])
    pd.DataFrame(puzzle).to_csv(hardfile,index=False,header=False)

    singletest.append(rd.mainout(hardfile))
    singletest.append(bt.mainout(hardfile))
    
    maintesthard.append(singletest)

col = ['Red','Bktk']
timeshard = pd.DataFrame(maintesthard,columns=col)

timeshard.to_csv('timeshard.csv')
timeshard = pd.read_csv('timeshard.csv')