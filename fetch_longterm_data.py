import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import cx_Oracle
import datetime
import calendar



def fetch_data(url):
    # go to website
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    time.sleep(5)

    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    action.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
    time.sleep(5)
    copied_text = pyperclip.paste()

    driver.quit()

    return copied_text


def send_to_db(data,username,password,month,year):

    try:
        connect_todata = cx_Oracle.connect(username + '/' + password + '@localhost/orcl')

        cursor = connect_todata.cursor()
        sql_query = "SELECT * FROM mf_nav_history WHERE DATEPART(month, NAV_DATE) = :1 AND DATEPART(year, NAV_DATE) = :2"
        data=(month,year)
        cursor.execute(sql_query,data)
        rows = cursor.fetchall()
        if not rows:
            l1 = list(cursor.execute('select ISIN from mf_trans_master'))

            l3 = []

            for line in data:
                if ";" in line:
                    l = line.split(';')
                    if l[2] is not None:
                        l3.append([l[1], l[2], l[7], l[4]])

            for isin in l1:
                for each in l3:
                    if each[1] == isin:
                        query = ('insert into mf_nav_history values(:1, :2, :3, :4)')
                        data = (each[0], each[1], each[2], each[3])
                        cursor.execute(query, data)


        cursor.close()

    except cx_Oracle.Error as error:
        print(error)




def main():
    username = input("Enter database username: ")
    password = input("Enter database password: ")

    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    years=['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']

    for year in years:
        for month in months:
            if((year=='2023') and (month in ['Jul','Aug','Sep','Oct','Nov','Dec'])):
                break

            else:
                num_month = (months.index(month) + 1)
                days_in_month = calendar.monthrange(int(year), num_month)[1]
                day_name = datetime.date(int(year), int(num_month), int(days_in_month)).strftime("%A")

                if (day_name == 'Saturday'):
                    days_in_month -= 1
                elif (day_name == 'Sunday'):
                    days_in_month -= 2

                datee = (str(days_in_month) + '-' + month + '-' + year)
                url = ('https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=' + datee)

                data = fetch_data(url)

                send_to_db(data, username, password, num_month, int(year))


main()

