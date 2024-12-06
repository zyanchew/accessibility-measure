# Dynamic Accessibility Measurement

## Overview
This project is part of my bachelor's graduation thesis. It focuses on analyzing human mobility data to study accessibility changes in response to extreme events. By examining mobility data before, during, and after the event, this project aims to identify trends in community resilience and recovery. The accessibility to gas station of each census block group in the study area is calculated for different phases of a hurricane event.

## Data
The dataset was sourced from [Safegraph], containing anonymized visits of Point-of-Interests (POI). The data includes:
- POI information
- Location
- Visits counts
- Date range

## Methodology
1. Data preprocessing: Cleaning and organizing the data. (The raw datasets from Safegraph is huge and it is not the main focus for this project objective. Therefore, this step is pre-done and the pre-processed dataset had been uploaded in respiratory for the following step)
2. Accessibility measurement: Quantifying accessibility metrics for each communnity, and calculating the changes in accessibility before, during and after the event.
3. Trend analysis: Examining communities response patterns during different phases of the event.

Accessibility metric: ![Equation to calculate accessibility of a census block group](images/accessibility_metrics.png)

In this project, accessibility metric indicating how accessible is a certain services to a community based on the number of visit of certain category of POI in the area. The distance decay function is included in the accessibility metric to reflect the sensitivity of distance between community and POI.

To assess the ability of community in response to extreme event, the changes in accessibility before, during, and after the event is claculated. Based on communities response patterns during different phases of the  event, agglomerative clustering algorithm is used for trend analysis. 

## Results
Key insights included:
- Changes in accessibility metrics pre- and post-event.
- Variations in community resilience.



