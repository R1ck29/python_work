#! python3
# coding: utf-8


import pandas as pd


df = pd.read_csv('test_data2.csv')

# Delete name col
new = df.drop('name', axis=1)
print(new)

# Save as new file
new.to_csv("deleted_col.csv")
print('Deleted')
