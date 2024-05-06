#Top 10 frequent co-purchasing patterns analysis
import networkx
from operator import itemgetter
import matplotlib.pyplot
import string
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
import networkx
import numpy as np
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.pylab as plt
from IPython.display import Image
from community import community_louvain
from collections import Counter
from itertools import chain
#pyo.init_notebook_mode()
import plotly.io as pio
pio.renderers.default = 'browser'

df = open ('amazon-Musics.txt', 'r', encoding='utf-8', errors= 'ignore')
amazonMusics= {}
df.readline()
for line in df:
    cell = line.split ('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip()
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating']= float(cell[8].strip())
    MetaData['DegreeCentrality']= int(cell[9].strip())
    MetaData['ClusteringCoeff'] = float(cell[10].strip())
    amazonMusics[ASIN] = MetaData
df.close()

copurchaseGraph = networkx.Graph()
for asin, metadata in amazonMusics.items():
    copurchaseGraph.add_node(asin)
    for a in metadata ['Copurchased'].split():
        copurchaseGraph.add_node(a.strip())
        similarity=0
        n1= set((amazonMusics[asin]['Categories']).split())
        n2= set ((amazonMusics[a]['Categories']).split())
        n1In2 = n1 & n2
        n1Un2 = n1 | n2
        if (len(n1Un2)) > 0:
            similarity = round (len(n1In2)/len(n1Un2), 2)
        copurchaseGraph.add_edge(asin, a.strip(), weight=similarity)

import pandas as pd
import os
from IPython.display import display, HTML


subgraphs = [nodes for nodes in nx.connected_components(copurchaseGraph) if len(nodes) > 1]




subgraph_sizes = Counter(len(nodes) for nodes in subgraphs)



top_subgraph_sizes = subgraph_sizes.most_common(10)


data = []


total_subgraphs = len(subgraphs)

for i, (size, count) in enumerate(top_subgraph_sizes):

    top_subgraph = [nodes for nodes in subgraphs if len(nodes) == size][0]
    

    edges = copurchaseGraph.subgraph(top_subgraph).number_of_edges()
    nodes = len(top_subgraph)
    

    percentage = (count / total_subgraphs) * 100
    

    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(copurchaseGraph.subgraph(top_subgraph))
    nx.draw(copurchaseGraph.subgraph(top_subgraph), pos, with_labels=False, node_color='skyblue', node_size=200, edge_color='black', linewidths=1)
    plt.title(f"Subgraph {i+1}, Size: {size}, Frequency: {count}")
    

    image_path = f"subgraph_images/subgraph_{i+1}.png"
    plt.savefig(image_path)
    plt.close()
    
    data.append({
        'ID': "G{}".format(i+1),
        'SubGraphs': f"<img src='{image_path}' width='100'>",
        'Nodes': nodes,
        'Edges': edges,
        'Frequency': count,
        'Percentage%': percentage
    })


df = pd.DataFrame(data)

# Display the DataFrame
display(HTML(df.to_html(escape=False)))

# Save the DataFrame as an HTML file
df.to_html('output.html', escape=False)

# Print the path to the saved HTML file
print("HTML file saved as 'output.html'")