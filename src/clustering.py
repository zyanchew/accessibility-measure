#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 19:39:30 2024

@author: zyanchew
"""

import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.metrics import silhouette_score
import os

# File paths
input_file = '/Users/zyanchew/Desktop/accessibility-measure/results/table/accessibility/accessibility_changes.csv'
output_file = '/Users/zyanchew/Desktop/accessibility-measure/results/table/cluster/cbg_cluster.csv'
save_dir = '/Users/zyanchew/Desktop/accessibility-measure/results/figures/'

# Load the data
c = pd.read_csv(input_file)

# Select the columns for clustering (two weeks before, during, and three weeks after the event)
c1 = pd.DataFrame(c, columns=['visitor_home_cbgs', 'change_0819-0826', 'change_0826-0902', 'change_0902-0909', 
                              'change_0909-0916', 'change_0916-0923'])
c1 = c1.set_index('visitor_home_cbgs')

# Prepare data for clustering
z = c1.values

# Hierarchical clustering (dendrogram)
i = sch.linkage(z, metric='euclidean', method='ward')
plt.figure(figsize=(10, 6))
sch.dendrogram(i, orientation='right', leaf_font_size=4, labels=c1.index)
plt.title('Dendrogram')
plt.ylabel('CBG')
plt.xlabel('Euclidean distances')
# Save the figure to the specified directory
figsav = os.path.join(save_dir, 'dendogram.png')
plt.savefig(figsav)
plt.show()

# Fit Agglomerative Clustering (with 3 clusters)
cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
cluster_labels = cluster.fit_predict(z)

c['cluster'] = cluster_labels  # First, add original labels
# Map original cluster labels to custom labels
custom_labels = {0: '2', 1: '3', 2: '1'}
c['cluster'] = c['cluster'].map(custom_labels)


# Plot the clusters (use the cluster labels for coloring)
plt.figure(figsize=(10, 6))
plt.scatter(z[cluster_labels == 2, 0], z[cluster_labels == 2, 1], s=5, c='royalblue', label='Cluster 1')
plt.scatter(z[cluster_labels == 0, 0], z[cluster_labels == 0, 1], s=5, c='limegreen', label='Cluster 2')
plt.scatter(z[cluster_labels == 1, 0], z[cluster_labels == 1, 1], s=5, c='tomato', label='Cluster 3')
plt.title('Clusters of CBG')
plt.legend()
# Save the figure to the specified directory
figsav = os.path.join(save_dir, 'cluster_scatter.png')
plt.savefig(figsav)
plt.show()

# Save the clustered data to a CSV file
c.to_csv(output_file)

# Evaluate how the number of clusters affects clustering performance (using silhouette score)
silhouette_scores = []
for i in range(2, 8):
    cluster = AgglomerativeClustering(n_clusters=i, affinity='euclidean', linkage='ward')
    cluster_labels = cluster.fit_predict(z)
    score = silhouette_score(z, cluster_labels)
    silhouette_scores.append(score)

# Plot the silhouette scores
plt.figure(figsize=(10, 6))
plt.plot(range(2, 8), silhouette_scores, marker='o', linestyle='-', color='b')
plt.title('Silhouette Score vs. Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
# Save the figure to the specified directory
figsav = os.path.join(save_dir, 'silhouette_score.png')
plt.savefig(figsav)
plt.show()