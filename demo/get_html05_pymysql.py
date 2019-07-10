# -*- coding:utf-8 -*-
import pymysql

def test05():

    # - 初始化数据信息
    username = 'root'
    password = 'root'
    host_addr = 'localhost'
    port_num = 3306
    database = 'software_homes'
    err_log = ""
    conn = ""

    try:
        import pymysql
        conn = pymysql.connect(database=database, user=username, password=password,
                               host=host_addr,
                               port=port_num, charset="utf8")
        err_log += '已连接Mysql\n数据库链接成功.'
        
    except Exception as e:
        err_log += '数据库链接失败，请检查数据库链接!'
    finally:
        print(err_log)
        if conn:
            return conn
        else:
            return False


if __name__ == "__main__":
    conn = test05()
    cr = conn.cursor()
    cr.execute('select * from data_mining_urls limit 10;')
    results = cr.fetchall()
    for line in results:
        print(line)
