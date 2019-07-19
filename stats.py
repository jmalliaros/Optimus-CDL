import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *
import networkx as nx


def get_networkx_plot_of_qubo(qubo, old_qubo):
	plt.clf()
	plt.title("Quadratic Interaction Graph")
	g = nx.Graph()
	for e,v in dict(old_qubo.quadratic).items():
		g.add_edge(e[0], e[1], weight=float(v))

	if qubo:
		g2 = nx.Graph()
		for e,v in dict(qubo.quadratic).items():
			g2.add_edge(e[0], e[1], weight=float(v))

	pos = nx.spring_layout(g, seed=1)

	if qubo:
		nx.draw_networkx_edges(
		    g, pos, edgelist=list(g2.edges), width=8, alpha=0.5, edge_color="#ff3300"
		)

		nx.draw_networkx_nodes(g, pos, nodelist=list(g2.nodes), node_size=500, node_color="#ff3300")

	nx.draw_networkx_nodes(g, pos, node_color="#3D9CD9")
	nx.draw_networkx_edges(g, pos, width=2, edge_color="#3D9CD9")
	nx.draw_networkx_labels(g, pos, font_size=16)

	weights = [g[u][v]['weight'] for u,v in g.edges()]

	edge_labels=dict([((u,v,),d['weight'])
	             for u,v,d in g.edges(data=True)])
	nx.draw_networkx_edge_labels(g,pos,edge_labels=edge_labels)

	l, r = plt.xlim()
	plt.xlim(l - 0.35, r + 0.35)
	plt.axis("off")

	plt.savefig("temp.png", format="PNG")

	import base64
	with open("temp.png", "rb") as image_file:
	    encoded_string = base64.b64encode(image_file.read())

	return encoded_string

def get_dwave_plot(res):
	plt.clf()
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
	df_interest = df[df['rel_occ']> 0.1/(nvars)]

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

	p = p + labs(x = 'Energy', y = 'Relative frequency', title="DWave: Energy of the different solutions")

	p.save("temp.png")

	import base64

	with open("temp.png", "rb") as image_file:
	    encoded_string = base64.b64encode(image_file.read())

	return encoded_string


from numpy import exp, cos, linspace
import matplotlib.pyplot as plt


# def damped_vibrations(t, A, b, w):
#     return A*exp(-b*t)*cos(w*t)


# def get_dwave_plot(A, b, w, T, resolution=500):
#     """Return filename of plot of the damped_vibration function."""
#     t = linspace(0, T, resolution+1)
#     u = damped_vibrations(t, A, b, w)
#     plt.figure()  # needed to avoid adding curves in plot
#     plt.plot(t, u)
#     plt.title('A=%g, b=%g, w=%g' % (A, b, w))

#     from io import BytesIO
#     figfile = BytesIO()
#     plt.savefig(figfile, format='png')
#     figfile.seek(0)  # rewind to beginning of file
#     import base64
#     #figdata_png = base64.b64encode(figfile.read())
#     figdata_png = base64.b64encode(figfile.getvalue())
#     return figdata_png
