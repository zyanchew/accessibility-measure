#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:08:51 2024

@author: zyanchew
"""

import pandas as pd
import numpy as np
import os

# Base file path
file = '/Users/zyanchew/Documents/GitHub/accessibility-measure/data'
file1 = '/Users/zyanchew/Documents/GitHub/accessibility-measure/data/patterns'
file2 = '/Users/zyanchew/Documents/GitHub/accessibility-measure/data/distancedecay'

# Path to the decay parameters CSV file
decay_params_file = file2 + '/decayparam_gas.csv'

# Read the decay parameters into a DataFrame
decay_params = pd.read_csv(decay_params_file)

# Check the content of the decay parameters file
if not {'date', 'beta', 'y-intercept'}.issubset(decay_params.columns):
    raise ValueError("The decay parameters file must contain 'date', 'beta', and 'y-intercept' columns.")

# Convert dates to strings for matching
decay_params['date'] = decay_params['date'].astype(str)

# Loop through each date in the decay parameters
for index, row in decay_params.iterrows():
    # Extract the date and parameters for the current row
    date = row['date']
    beta = row['beta']
    y = row['y-intercept']

    # Generate the file path for the current dataset
    filename = f'/patterns{date}.csv'
    filepath = file1 + filename

    # Check if the file exists
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue

    # Read and process the data
    a = pd.read_csv(filepath)
    a = a.sort_values(by=['visitor_home_cbgs', 'naics_code'])
    a['naics_code'] = a['naics_code'].astype(str)
    a['service'] = a['naics_code'].str.slice(start=0, stop=4)

    # Filter for gasoline station service
    c = a[(a.service == '4471')]
    c['poinumber'] = c['safegraph_place_id'].groupby(c['visitor_home_cbgs']).transform(np.count_nonzero)
    c['visitcbg'] = c['flow'] * (c['raw_visit_counts'] / c['raw_visitor_counts'])
    c['weights'] = (c['flow'] * (c['raw_visit_counts'] / c['raw_visitor_counts'])) / c['POPULATION']
    c['decayfunction'] = c['haversinedistance']**beta + y
    c['accessibility'] = c['weights'] * (c['haversinedistance']**beta + y)

    # Group by visitor_home_cbgs
    groupedgas = pd.DataFrame()
    groupedgas['latitude'] = c['LATITUDE'].groupby(c['visitor_home_cbgs']).mean()
    groupedgas['longitude'] = c['LONGITUDE'].groupby(c['visitor_home_cbgs']).mean()
    groupedgas['flow'] = c['flow'].groupby(c['visitor_home_cbgs']).sum()
    groupedgas['haversinedistance'] = c['haversinedistance'].groupby(c['visitor_home_cbgs']).mean()
    groupedgas['poinumber'] = c['poinumber'].groupby(c['visitor_home_cbgs']).mean()
    groupedgas['visitcbg'] = c['visitcbg'].groupby(c['visitor_home_cbgs']).sum()
    groupedgas['weights'] = c['weights'].groupby(c['visitor_home_cbgs']).sum()
    groupedgas['decayfunction'] = c['decayfunction'].groupby(c['visitor_home_cbgs']).sum()
    groupedgas['accessibility'] = c['accessibility'].groupby(c['visitor_home_cbgs']).sum()

    # Output file path
    output_filepath = f"{file}/accessibility/accessibility_gas_{date}.csv"

    # Save the grouped data to a CSV file
    groupedgas.to_csv(output_filepath)
    print(f"Processed and saved: {output_filepath}")