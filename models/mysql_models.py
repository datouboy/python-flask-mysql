####!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Time    : 2018/6/19
# @File    : mysql_models.py

import MySQLdb
# 查看try except捕获的异常
import traceback

class MysqlModels():

    def __init__(self):
        self.db_host     = "192.168.0.88"
        self.db_user     = "pythontest"
        self.db_password = "111111"
        self.db_dbName   = "again"
        print('~~~~~~~~~~~~~~~~~~~~ DB Start ~~~~~~~~~~~~~~~~~~~~')

    # 查询列表输出数组
    def selectList(self, table, select='*', where='', limit=10, offset=0, order_by='`ID` ASC'):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        # MySQLdb.cursors.DictCursor 让游标cursor的fetchall函数返回字典，而不是元组
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        if where == '':
            where = ''
        else:
            where = """WHERE %(where)s""" % {'where':where}

        sqlText = """SELECT %(select)s FROM `%(table)s` %(where)s ORDER BY %(order_by)s LIMIT %(limit)s,%(offset)s """ % {'select':select, 'table':table, 'where':where, 'order_by':order_by, 'offset':offset, 'limit':limit}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            results = cursor.fetchall()
            #print(results)
            return results
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ selectList error ~~~~~~~~~~~')
            traceback.print_exc()

        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

    # 根据ID查询具体内容
    def selectContent(self, table, select='*', id=''):
        where = '`ID` = %s' % (id)
        results = self.selectList(table, select, where, 0, 1, '`ID` ASC')
        if len(results) > 0:
            results = results[0]
        else:
            results = []
        #print(results)
        return results


    # 查询列表纪录数，直接返回数字
    def selectCount(self, table, where=''):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor()

        if where == '':
            where = ''
        else:
            where = """WHERE %(where)s""" % {'where':where}

        sqlText = """SELECT COUNT(*) FROM `%(table)s` %(where)s """ % {'table':table, 'where':where}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            results = cursor.fetchall()
            #print(results[0][0])
            return results[0][0]
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ selectCount error ~~~~~~~~~~~')
            traceback.print_exc()

        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

    # 插入新纪录，返回ID
    """
    param = {
        'ID' : 1,
        'Name': 'Zara',
        'Age': 7,
        'Class': 'First'
    }
    """
    def insert(self, table, param):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        '''
        遍历param拼装数据库语句
        table_field 数据库字段名
        table_value 值
        '''
        table_field = ''
        table_value = ''
        for key in param:
            # print(key+':'+param[key])
            table_field += '''`%s`, ''' % (key)

            # 判断值不为NULL或者不是数字类型 则增加单引号
            if param[key] != 'NULL' and isinstance(param[key], int) == False:
                table_value += ''''%s', ''' % (param[key])
            else:
                table_value += '''%s, ''' % (param[key])

        # 字符串处理，删除最后一个逗号
        table_field = table_field[0:-2]
        table_value = table_value[0:-2]

        sqlText = """INSERT INTO `%(table)s` (%(table_field)s) VALUES (%(table_value)s);""" % {'table':table, 'table_field':table_field, 'table_value':table_value}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            # 提交到数据库执行
            db.commit()
            new_id = self.selectList(table, '*', '', 0, 1, '`ID` DESC')
            #print(new_id[0]['ID'])
            return new_id[0]['ID']
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ insert error ~~~~~~~~~~~')
            traceback.print_exc()
        

        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

    # 修改更新数据
    def updata(self, table, where, param):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        if where == '':
            where = ''
        else:
            where = """WHERE %(where)s""" % {'where':where}

        # 遍历param拼装数据库语句
        table_field = ''
        table_value = ''
        set_sql_text = ''
        for key in param:
            # print(key+':'+param[key])
            table_field = '''`%s`''' % (key)

            # 判断值不为NULL或者不是数字类型 则增加单引号
            if param[key] != 'NULL' and isinstance(param[key], int) == False:
                table_value = '''\'%s\'''' % (param[key])
            else:
                table_value = '''%s''' % (param[key])

            set_sql_text += table_field + ' = ' + table_value + ', '

        # 字符串处理，删除最后一个逗号
        set_sql_text = set_sql_text[0:-2]

        sqlText = """UPDATE `%(table)s` SET %(set_sql_text)s %(where)s;""" % {'table':table, 'set_sql_text':set_sql_text, 'where':where}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            # 提交到数据库执行
            db.commit()
            return True
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ updata error ~~~~~~~~~~~')
            traceback.print_exc()
        
        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

    
    # 删除数据
    def delData(self, table, where):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)

        if where == '':
            where = 'WHERE `ID` < 0'
            print('where为空，已拦截')
        else:
            where = """WHERE %(where)s""" % {'where':where}

        sqlText = """DELETE FROM `%(table)s` %(where)s;""" % {'table':table, 'where':where}
        #print(sqlText);
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            # 提交到数据库执行
            db.commit()
            return True
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ delData error ~~~~~~~~~~~')
            traceback.print_exc()
        
        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

    # 清空表中数据
    def truncateTable(self, table):
        db = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_dbName, charset='utf8')
        cursor = db.cursor()

        sqlText = """TRUNCATE `%(table)s`;""" % {'table':table}
        try:
            # 执行sql语句
            cursor.execute(sqlText)
            # 提交到数据库执行
            db.commit()
            return True
        except:
            # 出错后数据回滚
            db.rollback()
            print('~~~~~~~~~~~ truncateTable error ~~~~~~~~~~~')
            traceback.print_exc()
        
        # 关闭指针对象
        cursor.close()
        # 关闭数据库连接
        db.close()

if __name__ == '__main__':
    print('单独运行此文件，以下代码将被执行')
    # 使用方法：
    # mmm = MysqlModels()
    # mmm.selectList('again_goods','*','`ID` < 1000', 0, 5,'`ID` ASC')