#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 19:22:15 2024

@author: zyanchew
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

# File paths
input_file = '/Users/zyanchew/Desktop/accessibility-measure/results/table/accessibility/combined_accessibility.csv'
output_file_changes = '/Users/zyanchew/Desktop/accessibility-measure/results/table/accessibility/accessibility_changes.csv'
save_dir = '/Users/zyanchew/Desktop/accessibility-measure/results/figures/'

# Function for moving average
def moving_average(x, window_size=3):
    return np.convolve(x, np.ones(window_size), 'valid') / window_size

# Read data
data = pd.read_csv(input_file)

# Filter columns dynamically for those starting with 'accessibility_'
accessibility_cols = [col for col in data.columns if col.startswith('accessibility_')]

# Set the index to 'visitor_home_cbgs' for easier manipulation
data.set_index('visitor_home_cbgs', inplace=True)

# Extract the relevant columns for accessibility
accessibility_data = data[accessibility_cols]

# Moving average calculation
averaged_data = []
for row in accessibility_data.iterrows():
    x = row[1].values
    smoothed = moving_average(x)
    averaged_data.append(smoothed)

# Store the averaged data in a DataFrame
smoothed_df = pd.DataFrame(averaged_data, columns=accessibility_cols[2:], index=accessibility_data.index)


# Calculate mean for pre-event period (using first 8 time periods)
pre_event_columns = accessibility_cols[2:10]
mean_values = smoothed_df[pre_event_columns].mean(axis=1)

# Calculate the accessibility change as percentage relative to the mean
change_data = pd.DataFrame()
for period in accessibility_cols[2:]:
    change_data[f'change{period[13:]}'] = (smoothed_df[period] - mean_values) / mean_values  # Remove 'accessibility_' prefix

# Save accessibility changes to CSV
change_data.to_csv(output_file_changes)

# Plot accessibility change over time for each row
plt.figure(figsize=(10, 6))
for row in change_data.iterrows():
    plt.plot(change_data.columns, row[1], linewidth=0.5, color=[0.75, 0.75, 0.75])

plt.xlabel('Time Period')
plt.ylabel('Accessibility Changes')
plt.xticks(ticks=np.arange(len(change_data.columns)), labels=[col[7:] for col in change_data.columns], rotation=90)  # Extract date range for x-ticks
plt.tight_layout()
# Save the figure to the specified directory
figsav = os.path.join(save_dir, 'accessibility_change.png')
plt.savefig(figsav)
plt.show()


