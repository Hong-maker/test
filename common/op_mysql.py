# encoding: utf-8

import pymysql

class OpMysql(object):
    # 连接ali云数据库，使用云数据库外网地址
    def __init__(self, host, user, password, database):
        try:
            self.conn = pymysql.connect(host=host, user=user, password=password, database=database)
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print('connect mysql error')

    def select_one(self, query, params=None):
        try:
            result = self.cur.execute(query, params)
            if result > 1:
                print('找到多条数据')
            elif result == 1:
                return self.cur.fetchone()
            else:
                # 查询到的结果为0
                print('找不到符合条件的数据')
        except BaseException as e:
            return '001'

    # 清除用户主账号信息：手机号、用户名
    def clear_basic_auth(self, column_name, column_value):
        table_name = 'basic_auth'
        result = self.cur.execute('UPDATE {} SET {}=%s WHERE {}=%s'.format(table_name, column_name, column_name), (None, column_value))
        if self.cur.rowcount == 1:
            self.conn.commit()

if __name__ == '__main__':
    # 连接dev环境
    opmysql = OpMysql(host='rm-bp173j25673ah67z8ko.mysql.rds.aliyuncs.com', user='TestDep', password='4Ehp1ndpfnlN9D0qvg4SZuig', database='account')
    data = opmysql.select_one("SELECT * from basic_auth where user_id=%s", (1000002450, ))
    print(data)