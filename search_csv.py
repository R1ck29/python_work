#! python3
# coding: utf-8

import pandas as pd
import os
import csv
import collections as cl


# move to work directory
os.chdir("C:/Users/p003230/Documents/賞データ移行")


df = pd.read_csv("new_error_stf_info.csv", engine='python', encoding="utf_8")


# put error staff No to list
stf_no = df['idou.sya_bg'].values

# put error reward date to list
rwd_date = df['sybtrk.sybdate'].values


# TODO: make it print error msg
stf_df = pd.read_csv("社員番号_入社日_退社日.csv", engine='python', encoding="utf_8")


def search_stf():
    """
    find staff who retired or not joined
    :return:
    """

    for i in stf_no:

        df_exact = stf_df[stf_df['STF_ADMN_NO'] == i]

        if "Empty DataFrame" in df_exact:
            print("Employee no. " + i + "does not exist")
        else:
            # append every matched staff info in csv file
            df_exact.to_csv("matched_stf_info.csv", index=False, header=None, mode='a')

    return print('Done mapping')


def check_date():
    """
    compare reward received date with his/her entry date and leaving date.

    :return: print emploee number, whether he/she not joined or retired
    """
    matched_df = pd.read_csv("matched_stf_info.csv", engine='python', encoding="utf_8")

    # TODO: matched_stf_info.csv's column name.
    # put entry date No to list
    entry_date = matched_df['ENTRY_DATE'].values

    # put leaving date to list
    leaving_date = matched_df['LEAVING_DATE'].values
    t = 0

    for i in rwd_date:

        if i < entry_date[t]:
            print("Employee number " + str(stf_no[t]) + " has not joined. "
                  + "Reward date: " + str(i) + " < " + "Entry date: " + str(entry_date[t]))
            result = pd.DataFrame([[stf_no[t], str(i), str(entry_date[t]), str(leaving_date[t]), "not joined"]],
                                    columns=['stf_no', 'reward_date', 'entry_date', 'leaving_date', 'result'])
            result.to_csv("errored_stf_status.csv", index=False, mode='a')
        if i > leaving_date[t]:

            print("Employee number " + str(stf_no[t]) + " already left. "
                  + "Reward date: " + str(i) + " > " + "Leaving date: " + str(leaving_date[t]))
            result = pd.DataFrame([[stf_no[t], str(i), str(entry_date[t]), str(leaving_date[t]), "retired"]],
                                    columns=['stf_no', 'reward_date', 'entry_date', 'leaving_date', 'result'])

            result.to_csv("errored_stf_status.csv", index=False, header=None, mode='a')
        #result.to_csv("errored_stf_status.csv", index=False, mode='a')
        t += 1
    return print('Done checking')

#search_stf()
check_date()

