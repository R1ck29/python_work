#! python3
# coding: UTF-8
import sys
import os
import re
#文字コード指定に必要
import codecs, os
import glob
import configparser

#inifileの内容を読み込み
inifile = configparser.SafeConfigParser()
inifile.read("./config.ini")

#結果を入れるディレクトリ作成
if not os.path.exists("results"):
  os.makedirs("results")  # 再帰的作成

#読み込むファイルの条件を指定
r_fname1 = inifile.get("config","extension")
r_fname2 = inifile.get("config","name")

#置換文字列を指定
#name_old = inifile.get("config","name_old") #この文字を含むファイルを操作＋ファイル名の置換元文字列
#name_new = inifile.get("config","name_new") #ファイル名の置換後文字列
text_old = inifile.get("config","text_old") #ファイル内の置換元 文字列
text_new = inifile.get("config","text_new") #ファイル内の置換後文字列
#screenshot_old = inifile.get("config","screenshot_old") #ファイル内の置換元 文字列
#screenshot_new = inifile.get("config","screenshot_new") #ファイル内の置換後文字列
#password_old = inifile.get("config","password_old") #ファイル内の置換元 文字列
#password_new = inifile.get("config","password_new") #ファイル内の置換後文字列

#正規表現のコンパイル
txt = re.compile(r_fname2)
fname_o = re.compile(name_old)

#スクリプト配置フォルダのファイル一覧取得
files = glob.glob("*." + r_fname1)

for file in files:
  
    #まずファイル名に指定文字を含むファイルのみ読込
    if txt.search(file):
        # replacedフォルダに、結果ファイル生成
        if fname_o.search(file):
            file_new = file.replace(name_old,name_new)
            
        else:
            file_new = file
                
        read_file = codecs.open(file, 'r', encoding='utf-8')
        
        if not os.path.exists("results//" + file_new):
            write_file = codecs.open('results//' + file_new, 'w', encoding='utf-8')
        else:
            print("There is a duplicated file: " + file_new)
            write_file = codecs.open('results//_duplicated_' + file_new, 'w', encoding='utf-8')

        lines = read_file.readlines() #読み込み
        lines2 = []
        for url_line in lines:
          #URLとスクショ格納フォルダ名置換
            url_line = url_line.replace(url_old,url_new).replace(screenshot_old,screenshot_new).replace(password_old,password_new)
            lines2.append(url_line) #別リストにする
        else:
            write_file.write(''.join(lines2)) #書き込み
            read_file.close()
            write_file.close()
             
    else:
        #ファイル内に該当の文字がない場合、変更しない。
        
        pass
