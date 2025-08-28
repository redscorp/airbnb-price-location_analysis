# Airbnb City Comparison Project

#### Author: Artem Aleshin

#### Goal: Compare rental prices and accomodation types across Paris, Berlin and Barcelona using Airbnb data.`

# Import necessary libraries

import pandas as pd
import matplotlib.pyplot as plt

#pandas - for working with structured data
# matplotlib - for data visualization

## Loading and preparing the data

# Loading data for Paris, Berlin and Barcelona

paris = pd.read_csv('listings_paris.csv.gz', compression='gzip')
berlin = pd.read_csv('listings_berlin.csv.gz', compression='gzip')
barcelona = pd.read_csv('listings_barcelona.csv.gz', compression='gzip')

# selecting data

columns = ['id', 'name', 'neighbourhood', 'room_type', 'price', 'minimum_nights', 'number_of_reviews']

berlin = berlin[columns].copy()
paris = paris[columns].copy()
barcelona = barcelona[columns].copy()

# Adding column city

berlin['city'] = 'Berlin'
paris['city'] = 'Paris'
barcelona['city'] = 'Barcelona'

# Combining 3 cities in one frame

df = pd.concat([berlin, paris, barcelona], ignore_index=True)

## Cleaning the data

# Deleting $ sign and comma

df['price'] = df['price'].replace({'\$|,': ''}, regex=True)

# Making price a float, ignoring errors

df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Deleting data if wasn't possible to convert (NaN)

df = df.dropna(subset=['price'])

# Deleting outliers
# Calculating IQR and threshold

Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_filtered = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]

# Removing an error in the database ("Neighbourhood highligts" Paris disctict)

df_filtered = df_filtered[df_filtered['neighbourhood'] != 'Neighborhood highlights']

## Beginning with visualization(graphs)

# Making a graph with 3 subgraphs (2 rows, 1 column)

fig, axes = plt.subplots(nrows=2, ncols= 1, figsize=(10,10))

# First graph

mean_price_by_city = df_filtered.groupby('city')['price'].mean()
mean_price_by_city.plot(kind='bar', ax=axes[0], color='skyblue', title='Average price for night by city')
axes[0].set_ylabel('Price (€)')
axes[0].set_xlabel('City')
axes[0].tick_params(axis='x', rotation=0)

# Second graph

mean_price_by_roomtype = df_filtered.groupby('city')['room_type'].value_counts(normalize=True).unstack()
mean_price_by_roomtype.plot(kind='bar', stacked=True, ax=axes[1], title='Room type by city')
axes[1].set_ylabel('Share (%)')
axes[1].set_xlabel('City')
axes[1].tick_params(axis='x', rotation=0)
axes[1].legend(title='Room type', loc='lower left')

plt.tight_layout()
plt.show()

# Before and after graphs

plt.figure(figsize=(12,5))

# Before graph

plt.subplot(1, 2, 1)
df['price'].hist(bins=50, color='orange')
plt.title('Price distribution with outliers')
plt.xlabel('Price (€)')
plt.ylabel('Amount')

# After graph

plt.subplot(1, 2, 2)
df_filtered['price'].hist(bins=50, color='orange')
plt.title('Price distribution without outliers')
plt.xlabel('Price (€)')
plt.ylabel('Amount')
plt.tight_layout()
plt.show()

mean_clean = df_filtered.groupby('city')['price'].mean()
print(mean_clean)

mean_clean.plot(kind='bar', title='Average price per city without outliers')
plt.xlabel('City')
plt.ylabel('Price (€)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Groupping by city and district

avg_price_neigh = df_filtered.groupby(['city', 'neighbourhood'])['price'].mean().reset_index()

# Sorting by descending order, showing 5 most expensive districts in a graph

top_prices = avg_price_neigh.sort_values(by='price', ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(top_prices['neighbourhood'][:5], top_prices['price'][:5])
plt.title('Top 5 most expensive districts overall')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Sorting by ascending order, showing 5 cheapest districts in a graph

bottom_prices = avg_price_neigh.sort_values(by='price', ascending=True)

plt.figure(figsize=(10, 6))
plt.bar(bottom_prices['neighbourhood'][:5], bottom_prices['price'][:5])
plt.title('Top 5 least expensive districts overall')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Graph for top 3 districts of every city

avg_price_neigh = df_filtered.groupby(['city', 'neighbourhood'])['price'].mean().reset_index()

top3_each = avg_price_neigh.groupby('city').apply(lambda x: x.nlargest(3, 'price')).reset_index(drop=True)

# Creating labels

top3_each['label'] = top3_each['neighbourhood'] + '(' + top3_each['city'] + ')'

plt.figure(figsize=(10, 6))
plt.bar(top3_each['label'], top3_each['price'])
plt.title('Top 3 most expensive districts in every city')
plt.xlabel('District (city)')
plt.ylabel('Price (€)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Average price by type of accomodation in every city

roomtype_price = df_filtered.groupby(['city', 'room_type'])['price'].mean().reset_index()

# Making a graph

plt.figure(figsize=(10, 6))
for city in roomtype_price['city'].unique():
    roomtype_subset = roomtype_price[roomtype_price['city'] == city]
    plt.bar(roomtype_subset['room_type'] + f' ({city})', roomtype_subset['price'])

plt.title('Average price by type of accomodation in every city')
plt.ylabel('Price (€)')
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.show()

# Graph for relation between number of reviews and price

plt.figure(figsize=(10, 6))
plt.scatter(df_filtered['number_of_reviews'], df_filtered['price'], alpha=0.2)
plt.title('Correlation between number of reviews and price')
plt.xlabel('Amount of reviews')
plt.ylabel('Price (€)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Filtering min amount of nights

filtered_min_nights = df_filtered[df_filtered['minimum_nights'] <= 30]

# Making a graph for relation between amount of min nights per stay and price

plt.figure(figsize=(10, 6))
plt.scatter(filtered_min_nights['minimum_nights'], filtered_min_nights['price'], alpha=0.2)
plt.title('Correlation between amount of min nights per stay and price')
plt.xlabel('Min nights per stay')
plt.ylabel('Price (€)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
