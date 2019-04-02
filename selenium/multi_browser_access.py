#!python3.6
# -*- coding:utf-8 -*-

import time
import threading
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import glob
import numpy as np


th_objs = []  # list for thread
driver = {}  # webdriver object which is to put each threads

# define 10 browser's window sizes and positions
browsers = [
    {"size-x": "460", "size-y": "260", "pos-x": "0",    "pos-y": "0"},
    {"size-x": "460", "size-y": "260", "pos-x": "450",  "pos-y": "0"},
    {"size-x": "460", "size-y": "260", "pos-x": "900", "pos-y": "0"},
    {"size-x": "460", "size-y": "260", "pos-x": "0", "pos-y": "250"},
    {"size-x": "460", "size-y": "260", "pos-x": "450",    "pos-y": "250"},
    {"size-x": "460", "size-y": "260", "pos-x": "900",  "pos-y": "250"},
    {"size-x": "460", "size-y": "260", "pos-x": "0", "pos-y": "470"},
    {"size-x": "460", "size-y": "260", "pos-x": "450", "pos-y": "470"},
    {"size-x": "460", "size-y": "260", "pos-x": "900", "pos-y": "470"},
    {"size-x": "460", "size-y": "260", "pos-x": "900", "pos-y": "500"}
]

# website URL
stg_url = ""
pro_url = ""
user_id = []
password = []
# user who got error will be added to this list
error_users = []
users = []
# get data file names in the folder
path = 'C:/打刻/splited'
filenames = glob.glob(path + "/*.csv")

# get input info
site_choice = input("どちらで実行しますか？" + "\n" + "1.ステージング" + "\n" + "2.本番" + "\n")
# get input info
clock_in_out_choice = input("どちらで実行しますか？" + "\n" + "1.出勤" + "\n" + "2.退勤" + "\n")


def set_execute_mode(clock_in_out_choice):
    """
    Make User choose which button to push, then store mode in a variable
    :return: in_or_out
    """

    if clock_in_out_choice == "1" or clock_in_out_choice == "１":
        in_or_out = "in"

    elif clock_in_out_choice == "2" or clock_in_out_choice == "２":
        in_or_out = "out"

    else:
        print("入力に誤りがあります。")

    return in_or_out


def make_user_lists():
    """
    Read each input files to get IDs which is same as Password,then put them into two dimensional array.
    :return: every_file_info_list
    """
    every_file_info_list = []
    for filename in filenames:

        # read csv file
        df = pd.read_csv(filename, engine='python', encoding='utf-8')
        user_id = []  # reset user_id list
        # Iterate through each columns to add value in lists
        for index, row in df.iterrows():

            user_id.append(row['id'])
            password.append(row['password'])

        every_file_info_list.append(user_id)

    every_file_info_list = np.array(every_file_info_list)  # make the array numpy array

    return every_file_info_list


# スレッドでブラウザを制御する関数
def proc(idx, in_or_out, every_file_info_list):
    browser = browsers[idx]
    tid = threading.get_ident()

    driver[tid] = webdriver.Chrome('C:/Users/p003230/PycharmProjects/python_projects/chromedriver.exe')

    # set sizes and positions
    driver[tid].set_window_size(browser['size-x'], browser['size-y'])
    driver[tid].set_window_position(browser['pos-x'], browser['pos-y'])

    print("idx: ", idx, "id:", threading.get_ident())
    # set output file paths
    output_file = 'C:/打刻/10_browsers/打刻ユーザ_{}.csv'.format(in_or_out)
    error_output_file = 'C:/打刻/10_browsers/打刻エラーユーザ_{}.csv'.format(in_or_out)

    for user_info in tqdm(every_file_info_list):

        try:
            # decide which site to access
            if site_choice == "1" or site_choice == "１":
                driver[tid].get(stg_url)
            elif site_choice == "2" or site_choice == "２":
                driver[tid].get(pro_url)

            driver[tid].implicitly_wait(10)
            driver[tid].find_element_by_name('user_id').send_keys(user_info)  # type user id
            driver[tid].find_element_by_name('password').send_keys(user_info)  # type password

            if in_or_out == "in":
                driver[tid].find_element_by_class_name('btn0').click()  # 出勤ボタン

            elif in_or_out == "out":
                driver[tid].find_element_by_xpath("//input[@value=' 退  勤 ']").click()  # 退勤ボタン
            driver[tid].implicitly_wait(10)
            driver[tid].find_element_by_class_name('back').click()  # 戻るボタン

            driver[tid].refresh()  # refresh the page
            users.append(user_info)  # append user_info which is done

        except NoSuchElementException:

            # when the error message is "ユーサIDまたはパスワードに誤りがあります", then do below
            #print("ERROR! " + user_info)
            error_users.append(user_info)
            pass
    driver[tid].quit()  # close finished window

    # Save User ID which has finished as CSV file
    users_df = pd.DataFrame(columns=['id'])
    users_df["id"] = users
    users_df.to_csv(output_file, index=False, mode='w')

    # Save User ID which has finished as CSV file
    error_users_df = pd.DataFrame(columns=['id'])
    error_users_df["id"] = error_users
    error_users_df.to_csv(error_output_file, index=False, mode='w')

    return print("Browser Number " + idx + " is Done!")


if __name__ == '__main__':
    # register thread
    for idx in range(0, len(browsers)):
        th_objs.append(threading.Thread(target=proc, args=(idx, set_execute_mode(clock_in_out_choice), make_user_lists()[idx])))

    # execute the thread
    for i in range(0, len(browsers)):
        th_objs[i].start()
