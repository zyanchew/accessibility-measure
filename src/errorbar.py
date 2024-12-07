#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:03:48 2024

@author: zyanchew
"""

#带状误差图error bar

import pandas as pd
import matplotlib.pyplot as plt
import os

# Input file
input_file = '/Users/zyanchew/Desktop/accessibility-measure/results/table/cluster/cbg_cluster.csv'
save_dir = '/Users/zyanchew/Desktop/accessibility-measure/results/figures/'

# Load data
data = pd.read_csv(input_file)

# Filter columns for 'change_' and include 'cluster'
change_cols = [col for col in data.columns if col.startswith('change_')]
data = data[['cluster'] + change_cols]

# Group data by clusters
grouped = data.groupby('cluster')

# Calculate mean and standard deviation for each cluster
mean_values = grouped.mean()
std_values = grouped.std()

# Define time periods for the x-axis dynamically
time_periods = [col.split('_')[-1] for col in change_cols]

# Plot each cluster
plt.figure(figsize=(10, 6))
colors = ['royalblue', 'limegreen', 'tomato']
labels = ['Cluster 1', 'Cluster 2', 'Cluster 3']

for i, (cluster_id, mean_row) in enumerate(mean_values.iterrows()):
    std_row = std_values.loc[cluster_id]
    plt.plot(time_periods, mean_row, label=labels[i], color=colors[i])
    plt.fill_between(
        time_periods, 
        mean_row - std_row, 
        mean_row + std_row, 
        color=colors[i], 
        alpha=0.1
    )

# Customize plot
plt.legend()
plt.title('Community Response and Recovery Pattern')
plt.xlabel('Time Period')
plt.ylabel('Accessibility Change')
plt.xticks(rotation=90)
plt.tight_layout()
# Save the figure to the specified directory
figsav = os.path.join(save_dir, 'community_clusters.png')
plt.savefig(figsav)
plt.show()