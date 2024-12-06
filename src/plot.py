#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:30:45 2024

@author: zyanchew
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to your combined data file
file = '/Users/zyanchew/Documents/GitHub/accessibility-measure/data/accessibility/combined_accessibility.csv'
save_dir = '/Users/zyanchew/Documents/GitHub/accessibility-measure/results/figures/'

# Read the data
data = pd.read_csv(file)

# Filter columns dynamically for those starting with 'accessibility_'
accessibility_cols = [col for col in data.columns if col.startswith('accessibility_')]

# Set the index to 'visitor_home_cbgs'
data = data.set_index('visitor_home_cbgs')

# Extract the relevant columns
accessibility_data = data[accessibility_cols]

# Calculate statistics
mean_values = accessibility_data.mean()
std_values = accessibility_data.std()
median_values = accessibility_data.median()

# Extract date ranges from column names
date_ranges = [col.split('_')[-1] for col in accessibility_cols]

# Plot mean and standard deviation
plt.figure(figsize=(10, 6))
plt.plot(date_ranges, mean_values, color='tomato', label='Mean')
plt.fill_between(
    date_ranges,
    mean_values - std_values,
    mean_values + std_values,
    color='tomato',
    alpha=0.1,
    label='Standard Deviation'
)
plt.title('Accessibility Metrics Over Time')
plt.xlabel('Time Period')
plt.ylabel('Accessibility')
plt.xticks(rotation=90)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
# Make sure the plot is drawn
plt.draw()
# Save the figure to the specified directory
mean_std_plot_path = os.path.join(save_dir, 'accessibility_mean_std.png')
plt.savefig(mean_std_plot_path)
plt.show()


# Plot median values
plt.figure(figsize=(10, 6))
plt.plot(date_ranges, median_values, color='dodgerblue', label='Median')
plt.title('Median of Accessibility Over Time')
plt.xlabel('Time Period')
plt.ylabel('Accessibility')
plt.xticks(rotation=90)
plt.grid(alpha=0.3)
plt.tight_layout()
# Make sure the plot is drawn
plt.draw()
# Save the figure to the specified directory
median_plot_path = os.path.join(save_dir, 'accessibility_median.png')
plt.savefig(median_plot_path)
plt.show()
