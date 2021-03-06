#! python3
# coding: utf-8
import os
import pandas as pd
import glob
import codecs as cd

list = []


def concat_csv():
    input_file_path = 'hoge'
    os.chdir(input_file_path)
    csv_files = glob.glob('*.csv')
    #cp932
    for i in csv_files:
        with cd.open(i, "r", "Shift-JIS", "ignore") as csv_file:
            list.append(pd.read_csv(csv_file))
    df = pd.concat(list)

    df.to_csv("単価情報データ.csv", encoding="SJIS", index=False)


def concat_excel():
    input_file_path = 'hoge'
    os.chdir(input_file_path)

    path = os.getcwd()
    files = os.listdir(path)
    print(files)
    #files_xlsx = [f for f in files if f[-3:] == 'xlsx']

    # excel_files = glob.glob('*.xlsx')
    df = pd.DataFrame()

    for f in files:
        #data = pd.read_excel(f, '勤怠修正ツール用')

        df_list = pd.read_html(f, '勤怠修正ツール用')
        print(df_list)
        df = pd.DataFrame(df_list[0])

        df = df.append(df)

    # df.to_excel("社員情報.xlsx")

    writer = pd.ExcelWriter('社員情報.xlsx')
    df.to_excel(writer,'sheet1')
    writer.save()

concat_excel()

# input_file_path = 'hoge'
# os.chdir(input_file_path)
#
# input_book = pd.ExcelFile('201608.xlsx')
# input_sheet_name = input_book.sheet_names
# df = input_book.parse(input_sheet_name[0])
# print(df)
