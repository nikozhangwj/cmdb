# encoding: utf-8

#载入traceback和mysqldb模块
import traceback
from MySQLdb import cursors
from django.db import connection

#定义mysql登陆变量
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "dfl^!G321"
MYSQL_DB = "cmdb_niko"
MYSQL_CHARSET = "utf8"


class mysql_connection(object):
    """docstring for mysql_ut"""
    #定义数据库操作函数
    @classmethod
    def mysql_ut(cls,SQL,args=(),fetch=True,one=False):
        cnt, result = 0, None
        cur = None
        try:
            cur = connection.cursor()
            cnt = cur.execute(SQL,args)
            if fetch:
                result = cur.fetchone() if one else cur.fetchall()
            else:
                connection.commit()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            if cur:
                cur.close()

        return cnt,result

        

