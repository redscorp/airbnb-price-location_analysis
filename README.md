# Airbnb price analysis

## Objective
This project analyzes Airbnb listings for three major cities (Barcelona, Berlin, Paris). The goal of this project is to identify key factors infuencing price and identify accomodation patterns.

## Data
The data can be found on Inside Airbnb website, which contains publicly available information about listings, such as:
- price
- room type
- neighborhood (district, coordinates)
- minimum nights
- number of reviews
- whether host is a superhost
- host response time

Datasets from 3 cities were merged together to form a single dataset with an additional city identifier

Data could be downloaded from here https://insideairbnb.com/get-the-data/

## Methods
The analysis includes following steps:
- Data cleaning (price conversion, missing values)
- Removal of outliers using IQR method
- Explaratory data analysis
- Correlation analysis
- Linear regression
- Visualization using Matplotlib

## Key findings
- Average prices between cities differ significantly
- Room type is one of the strongest predictors of price
- Price shows week correlation with number of reviews

## Business insights
- Hotel rooms cost is highest on average, meaning higher revenue for hosts
- Pricing differs by district, which should be used to analyze to calculate profitability
- Each factor should be considered (with its weight), when calculating the approximate rental price, in order to calculate profitability

## Limitattions
- Data represents only a snapshot in time, without analysis over time
- Seasonal effetcs are not captured
- Analysis focuses only on 3 big european cities

## Tools
- Python (JupiterLab)
- NumPy, Pandas
- Matplotlib, Seaborn
- SciPy (statistical tests)
- scikit-learn (preprocessing, regression, clustering)
- UMAP 
- Catboost 

## Author
Artem Aleshin,

BSc student Business management and Business analytics,

Lancaster University
