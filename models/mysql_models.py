####!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

class MysqlModels():

    def __init__(self):
        self.db_host     = "192.168.0.88"
        self.db_user     = "admin"
        self.db_password = "29959952"
        self.db_dbName   = "again"
        print('~~~~~~~~~~~~~~~~~~~~DB Start~~~~~~~~~~~~~~~~~~~~')

    def selectList(self, table, select='*', where='', limit=10, offset=0, order_by='`ID` ASC'):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor()

        sqlText = """SELECT %(select)s FROM `%(table)s` WHERE %(where)s ORDER BY %(order_by)s LIMIT %(limit)s,%(offset)s """ % {'select':select, 'table':table, 'where':where, 'order_by':order_by, 'offset':offset, 'limit':limit}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            results = cursor.fetchall()
            #print(results)
            return results
        except:
            # Rollback in case there is any error
            db.rollback()
            print('error')

        # 关闭数据库连接
        db.close()

if __name__ == '__main__':
    print('单独运行此文件，以下代码将被执行')
    mmm = MysqlModels()
    mmm.selectList('again_goods','*','`ID` < 1000', 0, 5,'`ID` ASC')