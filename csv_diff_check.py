#! python3
# coding: utf-8

import pandas as pd
import os
import csv

# move to work directory
os.chdir("C:/tools/CSV")

df01 = pd.read_csv('比較用_賞データ_fsta.csv', engine='python', encoding='Shift-JIS') # HUEに入れたデータ
df02 = pd.read_csv('賞データ(f-sta).csv', engine='python', encoding='Shift-JIS') # HUEから取り出したデータ

df01['diff'] = df01[['idou_sya_bg', 'sybtrk_sybt_cd']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)

df02['diff'] = df02[['idou_sya_bg', 'sybtrk_sybt_cd']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)

# df01には存在しておらず、df02には存在している行が出る
df_diff = df01[~df01['diff'].isin(df02['diff'])]
df_diff.to_csv('diff_result.csv', index=None)

# idou_sya_bg,sybtrk_sybt_cd,sybtrk_sybdate,sybtrk_sybt_jiyu_cd
