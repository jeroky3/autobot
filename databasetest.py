mysql_db_id = 'autobot'
mysql_db_password = 'autobot'
mysql_db_ip = 'localhost'
mysql_db_port = '3306'
mylsql_db_url = 'mysql+mysqldb://' + mysql_db_id + ':' + mysql_db_password + '@' + mysql_db_ip + ':' + mysql_db_port

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import pymysql
import pandas as pd

pymysql.install_as_MySQLdb()


class mysql_db_ctrl:
    def __init__(self):
        self.systemconn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
                                    port=int(mysql_db_port),
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        self.create_database_all()

        #self.dbconn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
        #                              port=int(mysql_db_port), charset='utf8mb4', database='testdb',
        #                              cursorclass=pymysql.cursors.DictCursor)

    def databaseexists(self, dbname):
        exists = False
        sql = "SELECT 1 FROM Information_schema.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(dbname)
        with self.systemconn.cursor() as cursor:
            cursor.execute(sql)
            dataresult = cursor.fetchall()
            #print(dataresult)
            #self.systemconn.commit()
            if dataresult is None or len(dataresult) == 0:
                exists = False
            else:
                exists = True
        return exists

    def close(self):
        self.conn.close()
        self.systemconn.close()

    def create_database_all(self):
        if not self.databaseexists('userinfo'):
            self.create_database('userinfo')

        if not self.databaseexists('stock'):
            self.create_database('stock')

        if not self.databaseexists('stock_dm'):
            self.create_database('stock_dm')

    def create_database(self, dbname):
        with self.systemconn.cursor() as cursor:
            """ create database """
            sql = 'CREATE DATABASE {}'
            cursor.execute(sql.format(dbname))
            self.systemconn.commit()

    def create_table(self, tablename):
        with self.conn.cursor() as cursor:
            """
            sql = 'CREATE TABLE {} (' \
                    'id int AUTO_INCREMENT PRIMARY KEY,' \
                    'userid varchar(255), ' \
                    'userpasswd varchar(255), ' \
                    'username varchar(255), ' \
                    'address varchar(255), ' \
                    'age int(3), ' \
                    'height FLOAT,' \
                    'weight DECIMAL(4, 2)' \
                  ') '
            cursor.execute(sql.format('usertable', 'fda'))
            conn.commit()
            """

            """ insert row
            sql = "INSERT INTO usertable (userid, userpasswd, username, address, age, height, weight) " \
                  "VALUES( %s, %s, %s, %s, %s, %s, %s ) "
            #cursor.execute(sql, ('user1', 'abcdefg', 'hong', 'seoul', 25, 167.4, 60))
            cursor.execute(sql, ('user3', 'bbbbb', 'gil', 'suwon', 35, 150.3, 47.3389))
            conn.commit()
            """

            """ select row 
            sql = "SELECT * FROM usertable where address = %s "
            cursor.execute(sql, ('suwon'))
            dataresult = cursor.fetchall()
            print(dataresult)
            conn.commit()
            """

            """ update row 
            userid = 'user2'
            sql = "UPDATE usertable set age = 33 where userid = %s"
            cursor.execute(sql, (userid))
            conn.commit()
            """

            """ delete row 
            userid = 'user3'
            sql = "DELETE FROM usertable where userid = %s"
            cursor.execute(sql, (userid))
            self.conn.commit()
            """

mysql_db_ctrl()