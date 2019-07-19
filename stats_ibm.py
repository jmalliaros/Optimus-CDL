# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 03:40:03 2019

@author: Michele
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *

from optimus_ibm import result

custom_cols = ["#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD"]

df_ibm = pd.DataFrame([result.keys(), result.values()]).T
df_ibm.columns = ['sol','num_occurrences']
df_ibm['solnum'] = '[' + df_ibm['sol'].apply(lambda x: ' '.join(x)) + ']: ' + df_ibm['num_occurrences'].astype(str)
df_ibm['rel_occ'] = df_ibm['num_occurrences']/df_ibm['num_occurrences'].sum()


p = ggplot(df_ibm,aes(x='sol', y='rel_occ', fill='solnum',label='num_occurrences')) 
p = p + geom_bar(stat='identity',width=0.5, show_legend=False)
p = p + geom_text(position = position_stack(vjust=0.5),size=10)
p = p + scale_fill_manual(values = custom_cols)
p = p + labs(x = 'Solution', y = 'Relative frequency', title="Frequency of the different solutions")
p.draw()
