#! python3
# coding: utf-8

import pandas as pd
import os
import csv
import collections as cl
import json

# データが格納されている作業ディレクトリまでパス指定
os.chdir("C:/Users/p003230/Documents/賞データ移行")

def make_lists():
    df = pd.read_csv("new_error_stf_info.csv", engine='python', encoding="utf_8")

    # put errored staff No to list
    stf_no = df['idou.sya_bg'].values

    # put errored reward date to list
    rwd_date = df['sybtrk.sybdate'].values

    return stf_no, rwd_date


# TODO: merge 2 lists into dict

"""
ys = cl.OrderedDict()
for i in range(len(stf_no)):
    data = cl.OrderedDict()
    data["rwd_date"] = rwd_date[i]

    ys[stf_no[i]] = data
print(ys)
#print("{}".format(json.dumps(ys,indent=4)))

fw = open('test.json', 'w')
# ココ重要！！
# json.dump関数でファイルに書き込む
#json.dump(ys, fw, indent=4)
"""



# --------------search--------------
# TODO: make it print error msg

def search_stf(stf_no):
    stf_df = pd.read_csv("社員番号_入社日_退社日.csv", engine='python', encoding="utf_8")

    for errors in stf_no:

        df_exact = stf_df[stf_df['STF_ADMN_NO'] == errors]
       # print(df_exact)

        if str(df_exact) in "Empty DataFrame":
            print(errors + "は存在しない社員です。")
        else:
            # search through csv
            print(df_exact)

       # df_exact.to_csv("matched_stf_info.csv", index=False, header=None, mode='a')
    return
make_lists()
search_stf()



