#! python3
# coding: utf-8

import pandas as pd
import os

import numpy as np

# helpful modules
import fuzzywuzzy
from fuzzywuzzy import process
import chardet

os.chdir("C:/Users/p003230/Documents/育成計画マッピング")

fuzzy_file = 'test_fuzzy.csv'


df = pd.read_csv(fuzzy_file, engine='python', encoding="utf-8")


# function to replace rows in the provided column of the provided dataframe
# that match the provided string above the provided ratio with the provided string
def replace_matches_in_column(df, column, string_to_match, min_ratio=90):
    # get a list of unique strings
    strings = df[column].unique()

    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings,
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
    print(matches)
    # only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    # replace all rows with close matches with the input matches
    df.loc[rows_with_matches, column] = string_to_match

    df.to_csv("find_similar_one.csv", index=False,  mode='w')

    # let us know the function's done
    print("All done!")


# use the function we just wrote to replace close matches to "d.i khan" with "d.i khan"
replace_matches_in_column(df=df, column='test', string_to_match="分析的に考え問題を特定する力議事録欄コメント")


# get all the unique values in the target column
target_col = df['test'].unique()

# sort them alphabetically and then take a closer look
target_col.sort()
print(target_col)

