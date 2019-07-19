import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 03:40:03 2019

@author: Michele
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *


def plot_this(result):
	plt.clf()
	custom_cols = ["#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD","#3D9CD9", "#33DAB0", "#486BDD"]

	df_ibm = pd.DataFrame([result.keys(), result.values()]).T
	df_ibm.columns = ['sol','num_occurrences']
	df_ibm['solnum'] = '[' + df_ibm['sol'].apply(lambda x: ' '.join(x)) + ']: ' + df_ibm['num_occurrences'].astype(str)
	df_ibm['rel_occ'] = df_ibm['num_occurrences']/df_ibm['num_occurrences'].sum()


	p = ggplot(df_ibm,aes(x='sol', y='rel_occ', fill='solnum',label='num_occurrences')) 
	p = p + geom_bar(stat='identity',width=0.5, show_legend=False)
	p = p + geom_text(position = position_stack(vjust=0.5),size=10)
	# p = p + scale_fill_manual(values = custom_cols)
	p = p + labs(x = 'Solution', y = 'Relative frequency', title="IBM: Frequency of the different solutions")
	p = p + theme(axis_text_x=element_text(rotation=45, hjust=1))
	p.draw()

	plt.savefig("temp.png", format="PNG")

	import base64
	with open("temp.png", "rb") as image_file:
	    encoded_string = base64.b64encode(image_file.read())

	return encoded_string