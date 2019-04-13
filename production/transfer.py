# -*- coding:utf-8 -*-
import pymysql


def get_loan_number(file):
    connect = pymysql.Connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="root",
        db="lbsmining",
        charset='utf8'
    )
    print("写入中，请等待……")
    cursor = connect.cursor()
    sql = "select text from checkinnyc where record_id <= 4 "
    cursor.execute(sql)
    number = cursor.fetchall()
    fp = open(file, "w")
    loan_count = 0
    for loanNumber in number:
        loan_count += 1
        fp.write(loanNumber[0] + "\n")
    fp.close()
    cursor.close()
    connect.close()
    print("写入完成,共写入%d条数据……" % loan_count)


if __name__ == "__main__":
    file = r"C:\Users\zhangqiao\Desktop\shujuji.txt"
    get_loan_number(file)