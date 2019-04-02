#! python3
# coding: UTF-8

import os


def write_texts(contents, file_path, file_name):

    # 結果を入れるディレクトリ作成
    if not os.path.exists(file_path):  # フルパスを指定
        os.makedirs(file_path)  # 再帰的作成
    # ファイル開く
    with open(file_path + '/' + file_name, 'w') as file_object:  # ファイルまでのフルパス
        # 記入
        file_object.write(contents)

    return file_object
