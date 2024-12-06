#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:03:08 2024

@author: zyanchew
"""

import pandas as pd
import os

# Define the base directory for the data
base_directory = "/Users/zyanchew/Desktop/accessibility-measure/data/accessibility"  
output_file = "/Users/zyanchew/Desktopb/accessibility-measure/data/accessibility/combined_accessibility.csv"  

# Get a list of all CSV files in the directory
file_paths = [
    os.path.join(base_directory, file)
    for file in os.listdir(base_directory)
    if file.endswith('.csv') and 'accessibility_gas' in file.lower()
]

# Sort file paths to ensure chronological order (if needed)
file_paths.sort()

# Initialize the combined dataframe
combined_df = None

# Loop through files and merge them
for i, file_path in enumerate(file_paths):
    print(f"Processing file: {file_path}")
    
    # Read the current file
    df = pd.read_csv(file_path)
    
    # Extract date range from the filename for tracking
    date_range = os.path.basename(file_path).split('_')[-1].split('.')[0]
    # Add `date_range` to column names except for 'visitor_home_cbgs'
    df.rename(
        columns=lambda x: f"{x}_{date_range}" if x != "visitor_home_cbgs" else x,
        inplace=True
    )
    
    # Merge with the combined dataframe
    if combined_df is None:
        # Initialize the first dataframe
        combined_df = df
    else:
        # Merge with the previous combined dataframe on 'visitor_home_cbgs'
        combined_df = pd.merge(
            combined_df,
            df,
            on='visitor_home_cbgs',
        )

# Save the combined dataframe to a CSV file
combined_df.to_csv(output_file, index=False)
print(f"Combined data saved to {output_file}")



