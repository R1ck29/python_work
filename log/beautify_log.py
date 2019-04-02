#! python3
# coding: UTF-8

import os
import datetime
import shutil
from distutils import dir_util

today = today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# Replace - to _
old_title = str(yesterday).replace('-', '_')
title = str(today).replace('-', '_')

# define file paths
old_file_path = 'C:/Users/nttdata/Desktop/S13_与信NG/S13_与信NG_ログ/' + str(old_title)
file_path = 'C:/Users/nttdata/Desktop/S13_与信NG/S13_与信NG_ログ/' + str(title)

# the file which is written
new_file = 'beautified_log_' + str(title) + '.txt'

# Create Directory if it does not exist
# TODO: copy from last date file not -1date
if not os.path.exists(file_path):  # フルパスを指定
    os.makedirs(file_path)

    # copy files from yesterday directory
    dir_util.copy_tree(old_file_path, file_path)


def get_file_name():
    """
    Get log file 
    """
    files = []
    text_file = []

    for x in os.listdir(file_path):
        files.append(x)

    for y in files:
        if y[-4:] == '.log':  # ファイル名の後ろ4文字を取り出してそれが.logなら
            text_file.append(y)  # リストに追加

            file_name = text_file.pop()

    return file_name


#get_file_name()

def extract_line():
    contents = ''

    with open(file_path + '/' + str(get_file_name()), 'r') as file_object:  # ファイルまでのフルパス
        lines = file_object.readlines()

        for line in lines:
            if line.find('errorCode') >= 0:
                contents += line[:-1].replace('         ', '\n')
            elif line.find(' at ') >= 0:
                contents += line[:-1].replace(' at ', '\n')

        with open(file_path + '/' + new_file, 'w') as file_object2:  # ファイルまでのフルパス

            file_object2.write(contents)


extract_line()
