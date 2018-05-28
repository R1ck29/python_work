#! python3
# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

import time
import datetime
from dateutil.relativedelta import relativedelta
import jholiday

# IE用ドライバー
driver = webdriver.Ie('パス')

"""
会議室を取る日にちを決める
"""

# 何ヶ月後を予約するかを指定　例）１ヶ月先は１、２ヶ月先は２
target_month = 2

today = datetime.date.today()  # datetimeから今日の日付を取得
get_month = today + relativedelta(months=target_month)

"""
ブラウザ操作開始
"""
# ログイン画面開く
url = 'https://gg2.groupwide.net/iMRRoomBooking/'
driver.get(url)

# ログイン情報
login_id = 'Uから始まるID'
com_id = 'nttdata'
password = 'パスードを入力してください'

"""
LOGIN
"""


def login():
    driver.find_element_by_name("id1").send_keys(login_id)  # idボックスのを探し入力
    driver.find_element_by_name("id2").send_keys(com_id)  # 会社識別子ボックスを探し入力
    driver.find_element_by_name("password").send_keys(password)  # パスワードボックスを探し入力
    driver.find_element_by_xpath("//input[@title='Login'][@type='submit']").click()  # Loginボタン押下
    driver.implicitly_wait(10)


login()

# 指定月まで表示カレンダーを移動。2ヶ月先まで表示するには二回Nextボタン押す必要あり
for i in range(target_month):
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
    driver.find_element_by_link_text("Next").click()  # Nextボタン押下
    time.sleep(3)


def get_dates():
    """
    月の最初の日と最後の日を調べる

    """
    # 会議室を取る月の初日を求める
    first_date = get_month - datetime.timedelta(days=today.day - 1)
    # 会議室を取る月の最終日を求める
    last_date = first_date + relativedelta(months=1) + datetime.timedelta(days=-1)

    return first_date, last_date


first, last = get_dates()


class Main:
    def __init__(self):

        """
       属性の値　data-timeline = "x" ←　以下から該当する数字をxに記入する

       1: 応接室, 　2: 大会議室, 　3: SouthTerrace, 　4: Core - A　6: FR事業部長会議室　
       7: 流サ事業部長会議室, 　8: N -A, 9: N - B, 10: N - C, 11: N - D, 12: N - E
       13: S - A, 　14: S - C, 15: S - D, 16: S - E
        """
        self.start_time = '11:00'  # 開始時間
        self.end_time = '12:00'  # 終了時間
        self.day_name = '(火)'  # 曜日
        self.room_name = '大会議室'  # 会議室名
        self.room_num = '//div[@class="tl ui-selectee"][@data-timeline="12"]'  # 会議室に対応するHTML属性


    def everyday_mtg(self, start_time, end_time, room_name, room_num):

        """"
    　　毎日同じ時間に同じ場所を予約する

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ

            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # dが増えることで日も増える

            holiday_name = jholiday.holiday_name(date=iter_date)
            """
            datetimeから曜日を取得
            weekdayと曜日の対応     
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
            """

            try:
                if holiday_name is None and not iter_date.weekday() == 5 and not iter_date.weekday() == 6:  # 祝日以外、平日のとき

                    if iter_date.weekday() == 0:
                        day_name = '(月)'
                    elif iter_date.weekday() == 1:
                        day_name = '(火)'
                    elif iter_date.weekday() == 2:
                        day_name = '(水)'
                    elif iter_date.weekday() == 3:
                        day_name = '(木)'
                    elif iter_date.weekday() == 4:
                        day_name = '(金)'

                    driver.find_element_by_link_text(str(d)).click()
                    driver.implicitly_wait(10)
                    # 会議室選択
                    driver.find_element_by_xpath(room_num).click()
                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')

                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + room_name + " " + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + " " + str(start_time) + '-' + str(
                            end_time) + ' の予約完了')

            except selenium.common.exceptions.UnexpectedAlertPresentException:
                print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' は祝日です')
            except NoSuchElementException:
                pass
            except ElementNotInteractableException:
                print("クリックできませんでした。")
            except selenium.common.exceptions.StaleElementReferenceException:
                pass

    def mon_mtg(self, start_time, end_time, day_name, room_name, room_num):

        """
        会議体を記載する

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ
            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # iが増えることで日も増える

            # 祝日セット
            holiday_name = jholiday.holiday_name(date=iter_date)

            """
            datetimeから曜日を取得
            weekdayと曜日の対応
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日

            """
            if holiday_name is None and iter_date.weekday() == 0: # 0は月曜日


                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定

                    # 会議室を選択
                    driver.find_element_by_xpath(room_num).click()

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath(
                        '//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + "  " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    pass
                except ElementNotInteractableException:
                    print("クリックできませんでした。")

    def tue_mtg(self, start_time, end_time, day_name, room_name, room_num):

        """
        鈴木の予約: 定例（火曜11:00-12:00）

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ
            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # iが増えることで日も増える

            # 祝日セット
            holiday_name = jholiday.holiday_name(date=iter_date)

            """
            datetimeから曜日を取得
            weekdayと曜日の対応
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日

            """
            if holiday_name is None and iter_date.weekday() == 1: # 1は火曜日


                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定

                    # 会議室を選択
                    driver.find_element_by_xpath(room_num).click()

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath(
                        '//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + "  " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    pass
                except ElementNotInteractableException:
                    print("クリックできませんでした。")


    def wed_mtg(self, start_time, end_time, day_name, room_name, room_num):

        """
        会議体を記載する

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ
            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # iが増えることで日も増える

            # 祝日セット
            holiday_name = jholiday.holiday_name(date=iter_date)

            """
            datetimeから曜日を取得
            weekdayと曜日の対応
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日

            """
            if holiday_name is None and iter_date.weekday() == 2: # 2は水曜日


                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定

                    # 会議室を選択
                    driver.find_element_by_xpath(room_num).click()

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath(
                        '//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + "  " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    pass
                except ElementNotInteractableException:
                    print("クリックできませんでした。")



    def thu_mtg(self, start_time, end_time, day_name, room_name, room_num):

        """
        定例（木曜16:00-18）

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ
            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # iが増えることで日も増える

            # 祝日セット
            holiday_name = jholiday.holiday_name(date=iter_date)

            """
            datetimeから曜日を取得
            weekdayと曜日の対応
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日

            """
            if holiday_name is None and iter_date.weekday() == 3: # 3は木曜日

                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定

                    # 会議室を選択
                    driver.find_element_by_xpath(room_num).click()

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath(
                        '//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + "  " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    pass
                except ElementNotInteractableException:
                    print("クリックできませんでした。")

    def fri_mtg(self, start_time, end_time, day_name, room_name, room_num):

        """
        会議体を記載する

        """

        for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ
            iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
                days=get_month.day - d)  # iが増えることで日も増える

            # 祝日セット
            holiday_name = jholiday.holiday_name(date=iter_date)

            """
            datetimeから曜日を取得
            weekdayと曜日の対応
            0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日

            """
            if holiday_name is None and iter_date.weekday() == 4: # 4は金曜日

                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定

                    # 会議室を選択
                    driver.find_element_by_xpath(room_num).click()

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath(
                        '//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + "  " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + room_name + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    pass
                except ElementNotInteractableException:
                    print("クリックできませんでした。")


# 実行するメソッドを指定する
if __name__ == '__main__':
    # 実行しないメソッドはシャープを行の先頭に入れてコメントアウトしてください。
    """
    1: 応接室, 　2: 大会議室, 　3: SouthTerrace, 　4: Core - A　6: FR事業部長会議室　
    7: 流サ事業部長会議室, 　8: N -A, 9: N - B, 10: N - C, 11: N - D, 12: N - E
    13: S - A, 　14: S - C, 15: S - D, 16: S - E
    """
    # 開始時間, 終了時間, 会議室名, 会議室番号の順です。最後の引数は、11など会議室の該当数字(上記参照)の箇所のみご変更ください。

    # 会議
    #muji_mtg = Main()
    # muji_mtg.tue_mtg('11:00', '12:00', '(火)', '大会議室', '//div[@class="tl ui-selectee"][@data-timeline="2"]')　

    # 定例
    ndbs_mtg = Main()
    ndbs_mtg.thu_mtg('16:00', '18:00', '(木)', 'South_Terrace', '//div[@class="tl ui-selectee"][@data-timeline="3"]')


    # 下記が毎日予約する場合に変更する箇所です
    # 朝会用
    omsTest_mtg = Main()
    # omsTest_mtg.everyday_mtg('09:30', '19:00', 'N-E', '//div[@class="tl ui-selectee"][@data-timeline="11"]')

    # 朝会用
    hiratuka_mtg = Main()
    hiratuka_mtg.everyday_mtg('09:30', '10:15', 'S-E', '//div[@class="tl ui-selectee"][@data-timeline="16"]')
