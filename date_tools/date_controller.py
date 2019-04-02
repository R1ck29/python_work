#!/usr/bin/env python3
# coding: utf-8
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import jholiday




"""
会議室を取る日にちを決める
"""
today = datetime.date.today()  # datetimeから日付を取得

target_month = 2  # 何ヶ月後か決める

get_month = today + relativedelta(months=target_month)


def get_dates(target_month):
    """
    最初の日と最後の日を調べる

    """
    # 会議室を取る月の初日を求める
    first_date = get_month - datetime.timedelta(days=today.day - 1)
    # 会議室を取る月の最終日を求める
    last_date = first_date + relativedelta(months=1) + datetime.timedelta(days=-1)

    return first_date, last_date


first, last = get_dates(target_month)


for i in range(first.day, last.day+1, 1):

    iter_date = today + relativedelta(months=target_month) - datetime.timedelta(days=get_month.day - i)

    """
    datetimeから曜日を取得
    weekdayと曜日の対応     
    0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
    """

    holiday_name = jholiday.holiday_name(date=iter_date)

    if holiday_name is None:

        if iter_date.weekday() == 0:
            print(str(iter_date) + ' is Monday')
        elif iter_date.weekday() == 1:
            print(str(iter_date) + ' is Tuesday')
        elif iter_date.weekday() == 2:
            print(str(iter_date) + ' is Wednesday')
        elif iter_date.weekday() == 3:
            print(str(iter_date) + ' is Thursday')
        elif iter_date.weekday() == 4:
            print(str(iter_date) + ' is Friday')
            
