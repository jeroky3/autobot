# database management control

import datetime
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import pymysql
import pandas as pd
from sqlalchemy import create_engine

mysql_db_id = 'autobot'
mysql_db_password = 'autobot'
mysql_db_ip = 'localhost'
mysql_db_port = '3306'
mylsql_db_url = 'mysql+mysqldb://' + mysql_db_id + ':' + mysql_db_password + '@' + mysql_db_ip + ':' + mysql_db_port

pymysql.install_as_MySQLdb()

class mysql_db_ctrl:
    def __init__(self):
        self.systemconn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
                                    port=int(mysql_db_port),
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        self.create_database_all()

        self.userinfo_conn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
                                      port=int(mysql_db_port), charset='utf8mb4', database='userinfo',
                                      cursorclass=pymysql.cursors.DictCursor)
        self.stock_conn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
                                      port=int(mysql_db_port), charset='utf8mb4', database='stock',
                                      cursorclass=pymysql.cursors.DictCursor)
        self.stock_dm_conn = pymysql.connect(user=mysql_db_id, password=mysql_db_password, host=mysql_db_ip,
                                      port=int(mysql_db_port), charset='utf8mb4', database='stock_dm',
                                      cursorclass=pymysql.cursors.DictCursor)

        self.stock_conn_sqlalchemy = create_engine('mysql+pymysql://' + mysql_db_id + ':' + mysql_db_password + '@' +
                                                   mysql_db_ip + '/' + 'stock')

        self.create_tables_all()

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


    def tableexists(self, tablename):
        exists = False
        sql = "SELECT table_name FROM Information_schema.TABLES where table_name = '{}'".format(tablename)
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

    def create_tables_all(self):

        # users
        if not self.tableexists('users'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'userid varchar(255), ' \
                      'userpasswd varchar(255), ' \
                      'username varchar(255), ' \
                      'birthday varchar(6) ' \
                      ') '
            self.create_table(self.userinfo_conn, 'users', tempsql)

        # algorithm

        # backtesting

        # updatetabledate
        # id stock_info stock_history stock_report stock_daily stock_min index_history news_info  oil currency livingrate
        if not self.tableexists('update_table_date'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'stocktableid int, ' \
                      'stock_info date, ' \
                      'stock_history date, ' \
                      'stock_report date, ' \
                      'stock_daily date, ' \
                      'stock_min date, ' \
                      'index_history date, ' \
                      'news_info date, ' \
                      'oil date, ' \
                      'currency date, ' \
                      'livingrate date ' \
                      ') '
            self.create_table(self.stock_conn, 'update_table_date', tempsql)

            sql = "INSERT INTO update_table_date (stocktableid) VALUES (1)"
            with self.stock_conn.cursor() as cursor:
                cursor.execute(sql)
                self.stock_conn.commit()

        # stock_info
        # id, code, name, createdate(?????????), kospidaq(0:kospi, 1:kosdaq),
        # stocksize(????????????, 0: ?????????, 1:????????????, 2: ??????,  ?????????????), thema(?????????), kind(??????),
        # facevalue(?????????), capital(?????????), stockcnt(???????????????),
        # marketcap(????????????), foreign(???????????????), PER, EPS, ROE, PBR, EV, BPS,
        # salesrevenue(?????????), opincome(????????????), netincome(???????????????),
        # construction(????????????), stockstate(????????? ??????, ????????????, ????????????, ????????????, ??????????????????, ????????????, ????????????, ???????????? ??????),
        if not self.tableexists('stock_info'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'code varchar(10), ' \
                      'name varchar(100), ' \
                      'facevalue decimal(8,2),' \
                      'facevalueunit varchar(10),' \
                      'capital int, ' \
                      'stockcnt int, ' \
                      'marketcap int, ' \
                      'foreignrate decimal(6,2), ' \
                      'PER decimal(8,2), ' \
                      'EPS int, ' \
                      'ROE decimal(8,2), ' \
                      'PBR decimal(8,2), ' \
                      'EV decimal(8,2), ' \
                      'BPS int, ' \
                      'salesrevenue int, ' \
                      'opincome int, ' \
                      'netincome int, ' \
                      'createdate date, ' \
                      'kospidaq varchar(10), ' \
                      'stocksize varchar(10), ' \
                      'thema varchar(40), ' \
                      'kind varchar(100), ' \
                      'construction varchar(100), ' \
                      'stockstate varchar(100), ' \
                      'majorproduct varchar(255), ' \
                      'ceo varchar(100), ' \
                      'home varchar(40) ' \
                      ') '
            self.create_table(self.stock_conn, 'stock_info', tempsql)

        # stock_history
        # id, code, issuedate, issuetitle, issuecontents
        if not self.tableexists('stock_history'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'code varchar(10), ' \
                      'issuedate datetime, ' \
                      'issuetitle varchar(100), ' \
                      'issuecontents TEXT, ' \
                      'features varchar(255)' \
                      ') '
            self.create_table(self.stock_conn, 'stock_history', tempsql)

        # stock_report
        # id, code, issuedate, PER, ROE, PBR, ????????????, ???????????????,
        if not self.tableexists('stock_report'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'code varchar(10), ' \
                      'issuedate datetime, ' \
                      'EPS DECIMAL(8,2), ' \
                      'BPS DECIMAL(8,2), ' \
                      'PER DECIMAL(8,2), ' \
                      'PBR DECIMAL(8,2), '  \
                      'ROE DECIMAL(8,2), ' \
                      'ROA DECIMAL(8,2) ' \
                      ') '
            self.create_table(self.stock_conn, 'stock_report', tempsql)

        # index_history
        # id, date, kospi, kosdaq, kospi200, dow, nasdaq, S&P500, hkse, shanghai, tokyo, eurostoxx...
        if not self.tableexists('index_history'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'date date, ' \
                      'kospi DECIMAL(8,2), ' \
                      'kosdaq DECIMAL(8,2), ' \
                      'dow DECIMAL(8,2), '  \
                      'nasdaq DECIMAL(8,2), ' \
                      'snp500 DECIMAL(8,2), ' \
                      'hkse DECIMAL(8,2), ' \
                      'shanghai DECIMAL(8,2), ' \
                      'nikkei DECIMAL(8,2), ' \
                      'eurostoxx DECIMAL(8,2) ' \
                      ') '
            self.create_table(self.stock_conn, 'index_history', tempsql)

        indextables = ['index_kospi', 'index_kosdaq', 'index_kospi200', 'index_dow', 'index_nasdaq', 'index_snp500',
                       'index_hkse', 'index_shanghai', 'index_tokyo', 'index_eurostoxx']
        for t in indextables:
            if not self.tableexists(t):
                tempsql = 'CREATE TABLE {} (' \
                          'id int AUTO_INCREMENT PRIMARY KEY,' \
                          'date date, ' \
                          'high DECIMAL(8,2), ' \
                          'low DECIMAL(8,2), ' \
                          'close DECIMAL(8,2), ' \
                          'volume DECIMAL(10,2), '  \
                          'adjclose DECIMAL(8,2) ' \
                          ') '
                self.create_table(self.stock_conn, t, tempsql)

        # news_info_keyword
        # id, datetime, keyword, kinds, types, bins
        if not self.tableexists('news_info_keyword'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'date datetime, ' \
                      'keyword varchar(50), ' \
                      'kinds varchar(100), ' \
                      'types varchar(100), ' \
                      'bins int ' \
                      ') '
            self.create_table(self.stock_conn, 'news_info_keyword', tempsql)

        # news_info_news_anal
        # id, newsid, newsdate, media, writer, title, kind1, kind2, kind3,
        # accidentkind1, accidentkind2, accidentkind3,
        # people, place, stocknames, keyword, featureweight, contentdetail, url, noanalysis
        if not self.tableexists('news_info_news_anal'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'newsid varchar(255), ' \
                      'newsdate datetime, ' \
                      'media varchar(50), ' \
                      'writer varchar(50), ' \
                      'title varchar(255), ' \
                      'kind1 varchar(100), ' \
                      'kind2 varchar(100), ' \
                      'kind3 varchar(100), ' \
                      'accidentkind1 varchar(100), ' \
                      'accidentkind2 varchar(100), '\
                      'accidentkind3 varchar(100), ' \
                      'people varchar(100), ' \
                      'place varchar(100), ' \
                      'stocknames varchar(100), ' \
                      'keyword varchar(100), ' \
                      'featureweight varchar(100), ' \
                      'contentdetail TEXT, ' \
                      'url varchar(255), ' \
                      'noanalysis varchar(255) ' \
                      ') '
            self.create_table(self.stock_conn, 'news_info_news_anal', tempsql)

        # oil
        # id, date, brent, gas, wti, dubai
        if not self.tableexists('oil'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'date datetime, ' \
                      'brent decimal(8,2), ' \
                      'gas decimal(8,2), '\
                      'wti decimal(8,2), ' \
                      'dubai decimal(8,2) ' \
                      ') '
            self.create_table(self.stock_conn, 'oil', tempsql)

        # currency
        # id, date, usd, jpy, euro, cny
        if not self.tableexists('currency'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'date date, ' \
                      'usd decimal(6,2), ' \
                      'jpy decimal(6,2), '\
                      'euro decimal(6,2), ' \
                      'cny decimal(6,2) ' \
                      ') '
            self.create_table(self.stock_conn, 'currency', tempsql)

        # livingrate
        # id, date, us, kr, eu, jp, cn
        if not self.tableexists('livingrate'):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY,' \
                      'date date, ' \
                      'us decimal(8,2), ' \
                      'kr decimal(8,2), '\
                      'eu decimal(8,2), ' \
                      'jp decimal(8,2), ' \
                      'cn decimal(8,2) ' \
                      ') '
            self.create_table(self.stock_conn, 'livingrate', tempsql)

    def create_table(self, dbconn, tablename, sql):
        try:
            with dbconn.cursor() as cursor:
                cursor.execute(sql.format(tablename))
                dbconn.commit()
                print('success to create table ', tablename)
        except Exception as e:
            print('error to create table ', tablename)

    def drop_table(self, tablename):
        try:
            sql = "DROP TABLE {}"
            with self.stock_conn.cursor() as cursor:
                cursor.execute(sql.format(tablename))
                self.stock_conn.commit()
                print('success to drop table ', tablename)
        except Exception as e:
            print('error to drop table ', tablename)

    def clear_table(self, tablename):
        try:
            sql = "DELETE FROM {}"
            with self.stock_conn.cursor() as cursor:
                cursor.execute(sql.format(tablename))
                self.stock_conn.commit()
                print('success to clear table ', tablename)
        except Exception as e:
            print('error to clear table ', tablename)


    def insertstockinfo(self, sql, data=None):
        with self.stock_conn.cursor() as cursor:
            if data is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, data)
            self.stock_conn.commit()

    def insertstockdaily(self, sql, data=None):
        with self.stock_dm_conn.cursor() as cursor:
            if data is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, data)
            self.stock_dm_conn.commit()


    def checktablehasthecolumn(self, tablename, colname, coldata=None):
        exists = False
        """ select row  """
        sql = "SELECT {} FROM {} "
        if coldata is not None:
            sql = sql + " where {} = %s "
        with self.stock_conn.cursor() as cursor:
            if coldata is not None:
                cursor.execute(sql.format(colname, tablename, colname), (coldata))
            else:
                cursor.execute(sql.format(colname, tablename))
            dataresult = cursor.fetchall()
            if dataresult is None or len(dataresult) == 0:
                exists = False
            else:
                exists = True
            #self.stock_conn.commit()

        return exists

    def update_date_table_done(self, colname):
        """ update row """
        sql = "UPDATE update_table_date set {} = '{}' where stocktableid = 1".format(colname, datetime.datetime.now().date())
        with self.stock_conn.cursor() as cursor:
            cursor.execute(sql)
            self.stock_conn.commit()

    # stock_daily
    def create_stock_daily_table(self, code):
        # stock_daily
        # id, date, code, stockname, profitrate, close, open, high, low,
        # volume, volavg5, volavg20,
        # closeavg5, closeavg20, closeavg60, closeavg120
        # closeavg5rate, closeavg20rate, closeavg60rate, closeavg120rate
        tablename = 'A' + code
        if not self.tableexists(tablename):
            tempsql = 'CREATE TABLE {} (' \
                      'id int AUTO_INCREMENT PRIMARY KEY, ' \
                      'stockdate date, ' \
                      'open int, ' \
                      'high int, ' \
                      'low int, ' \
                      'close int, ' \
                      'profit decimal(8,2), ' \
                      'profitrate decimal(6,2), ' \
                      'volume int, ' \
                      'volumemoney int, ' \
                      'creditrate decimal(6,2), ' \
                      'personalvol int, ' \
                      'investmentvol int, ' \
                      'foreignvol int, ' \
                      'foreignersvol int, ' \
                      'program int, ' \
                      'foreignrate decimal(6,2), ' \
                      'foreignbuy int, ' \
                      'investmentbuy int, '\
                      'personalbuy int, ' \
                      'volavg5 int, ' \
                      'volavg20 int, ' \
                      'closeavg5 int, ' \
                      'closeavg20 int, ' \
                      'closeavg60 int, ' \
                      'closeavg120 int' \
                      ') '

            self.create_table(self.stock_dm_conn, tablename, tempsql)

    def select_stock_info(self, sql, tablename=None, colname=None):
        with self.stock_conn.cursor() as cursor:
            cursor.execute(sql)
            dataresult = cursor.fetchall()
            return dataresult


    def select_stock_dm_data(self, sql, tablename, selectcolname=None):
        with self.stock_dm_conn.cursor() as cursor:
            if selectcolname is None:
                cursor.execute(sql.format(tablename))
            else:
                cursor.execute(sql.format(selectcolname, tablename))
            dataresult = cursor.fetchall()

            return dataresult

    def insert_stock_dm_data(self, trdata):
        pass

    def update_stock_dm_data(self, sql):
        with self.stock_dm_conn.cursor() as cursor:
            cursor.execute(sql)
            self.stock_dm_conn.commit()


if __name__ == '__main__':
    mysql_db_ctrl()