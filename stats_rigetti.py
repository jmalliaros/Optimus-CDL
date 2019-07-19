# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 03:40:03 2019

@author: Olivier
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *

#from optimus_rigetti import result


def plot_this_rigetti(result):
    custom_cols = ["#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD"]
    _, freq = result
    df_rigetti = pd.DataFrame.from_dict(freq.items())
    df_rigetti.columns = ['sol','num_occurrences']
    df_rigetti['sol'] = df_rigetti['sol'].apply(lambda x: str(x).replace('(', '[').replace(',','').replace(')',']')) 
    df_rigetti['solnum'] = df_rigetti['sol'] + ': ' + df_rigetti['num_occurrences'].astype(str)
    df_rigetti['rel_occ'] = df_rigetti['num_occurrences']/df_rigetti['num_occurrences'].sum()


    p = ggplot(df_rigetti,aes(x='sol', y='rel_occ', fill='solnum',label='num_occurrences')) 
    p = p + geom_bar(stat='identity',width=0.5, show_legend=False)
    p = p + geom_text(position = position_stack(vjust=0.5),size=10)
    p = p + scale_fill_manual(values = custom_cols)
    p = p + labs(x = 'Solution', y = 'Relative frequency', title="Frequency of the different solutions")
    p.draw()

    plt.savefig("temp.png", format="PNG")

    with open("temp.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string
