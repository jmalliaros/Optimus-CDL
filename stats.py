# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:49:33 2019

@author: Olivier
"""
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *

from optimus_dwave import res

#Start with a result object SampleSet
df_raw = res.to_pandas_dataframe().sort_values(by='energy')
nrow, ncol = df_raw.shape
nvars = ncol-3

df1 = df_raw.copy()
df1['sol'] = df1.iloc[:,0:nvars].astype(str).apply(lambda x: ' '.join(x), axis=1)
df1.drop(df1.columns[0:(nvars+1)], axis=1, inplace=True)
df = df1.groupby(['energy','sol']).sum().reset_index()
df['solnum'] = "[" + df['sol'] + "]: " + df['num_occurrences'].astype(str) 
df['rel_occ'] = df['num_occurrences']/df['num_occurrences'].sum()


#Remove the solutions that happened less than 0.1% / number of variables
df_interest = df[df['rel_occ']> 0.1/(nrow-3)]

#Number of occurences
energy_uniques, energy_counts = np.unique(df_interest['energy'], return_counts = True)

#Number of different solutions
n_energy_solutions = len(energy_uniques)

#Difference of energy between first and 2nd best solutions
energy_diff = None
if len(energy_uniques) > 1:
    energy_diff = np.abs(energy_uniques[0] - energy_uniques[1])

energy_cat = CategoricalDtype(categories=energy_uniques, ordered=True)
df_interest['energy_cat'] = df_interest['energy'].astype(energy_cat)

#Create the barplot
p = ggplot(df_interest,aes(x='energy_cat', y='rel_occ', fill='solnum',label='solnum')) 
p = p + geom_bar(stat='identity',width=0.5, show_legend=False)
p = p + geom_text(position = position_stack(vjust=0.5),size=9)

if len(energy_uniques) > 1: 
    p = p + geom_segment(aes(x=1.30, y=0, xend=1.7, yend=0), arrow=arrow(angle = 60, length = 0.1,ends='both'),size=1.5)
    p = p + annotate("text", label = energy_diff, x=1.5, y = 0.05, size = 10)

p = p + labs(x = 'Energy', y = 'Relative frequency', title="Energy of the different solutions")
print(p)


