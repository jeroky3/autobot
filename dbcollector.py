import sys
import datetime
import decimal
import time
import numpy as np

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pymysql
import pandas as pd
from mysqldbctrl import *


class DbCollector(QAxWidget):
    def __init__(self):
        super().__init__()

        self.trData = None
        self.rqcount = 0

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.OnEventConnect.connect(self.eventConnect)
        self.OnReceiveMsg.connect(self.receiveMsg)
        self.OnReceiveTrData.connect(self.receiveTrData)
        self.OnReceiveChejanData.connect(self.receiveChejanData)

        self.dynamicCall('CommConnect()')
        self.logineventloop = QEventLoop()
        self.logineventloop.exec_()
        self.treventloop = QEventLoop()
        self.chejaneventloop = QEventLoop()

        #self.apitest()
        #self.buystock("005930", 1)
        #self.sellstock("005930", 1)

        self.mysqldbctrl = mysql_db_ctrl()
        self.update_stock_info()

    def eventConnect(self, nErrCode):
        if nErrCode == 0:
            print('로그인 성공')
            self.logineventloop.exit()
        elif nErrCode == -100:
            print('사용자 정보교환 실패')
        elif nErrCode == -101:
            print('서버접속 실패')
        elif nErrCode == -102:
            print('버전처리 실패')

    def receiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print('receiveMsg', sScrNo, sRQName, sTrCode, sMsg)

    def setinputvalue(self, sID,    # // TR에 명시된 Input이름
                            sValue):  # // Input이름으로 지정한 값
        self.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def commrqdata(self,  sRQName, #   // 사용자 구분명 (임의로 지정, 한글지원)
          sTrCode,   # // 조회하려는 TR이름
          nPrevNext, # // 연속조회여부
          sScreenNo ): #  // 화면번호 (4자리 숫자 임의로 지정)
        time.sleep(2)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)
        self.rqcount += 1
        print('req count : ', self.rqcount)
        self.treventloop = QEventLoop()
        self.treventloop.exec_()

    def receiveTrData(self, sScrNo, #  // 화면번호
          sRQName,      #// 사용자 구분명
          sTrCode,      #// TR이름
          sRecordName,  #// 레코드 이름
          sPrevNext,    #// 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 2:연속(추가조회) 데이터 있음
          nDataLength,  #// 사용안함.
          sErrorCode,   #// 사용안함.
          sMessage,     #// 사용안함.
          sSplmMsg):     #// 사용안함
        #print('receiveTrData ', sScrNo, sRQName, sTrCode, sRecordName, sPrevNext)

        try:
            nCnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            self.trData = []
            if sRQName == 'opt10001req':
                #for nIdx in range(0, nCnt):
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "종목코드")
                self.trData.append(val)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "종목명")
                self.trData.append(val)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "액면가")
                self.trData.append(decimal.Decimal(val) if val != '' else decimal.Decimal(0))
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "액면가단위")
                self.trData.append(val)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "자본금")
                self.trData.append(int(val))
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "상장주식")
                self.trData.append(int(val))
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "시가총액")
                self.trData.append(int(val))
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "외인소진률")
                self.trData.append(decimal.Decimal(val) if val != '' else decimal.Decimal(0))
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "PER")
                self.trData.append(decimal.Decimal(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "EPS")
                self.trData.append(int(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "ROE")
                self.trData.append(decimal.Decimal(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "PBR")
                self.trData.append(decimal.Decimal(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "EV")
                self.trData.append(decimal.Decimal(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "BPS")
                self.trData.append(int(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "매출액")
                self.trData.append(int(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "영업이익")
                self.trData.append(int(val) if val != '' else None)
                val = self.getopt10001reqdata(sTrCode, sRQName, nCnt, "당기순이익")
                self.trData.append(int(val) if val != '' else None)

        except TypeError as e:
            print('error receiveTrData', e)

        self.treventloop.exit()

    def getopt10001reqdata(self, trcode, rqname, ncnt, fieldname):
        val = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, ncnt, fieldname)
        return val.strip()

    def receiveChejanData(self,
            sGubun, #// 체결구분. 접수와 체결시 '0'값, 국내주식 잔고변경은 '1'값, 파생잔고변경은 '4'
            nItemCnt,
            sFIdList):
        print('receiveChejanData {} {} {}'.format(sGubun, nItemCnt, sFIdList))

        stockcode = self.dynamicCall("GetChejanData(int)", 9001)
        print('종목코드 = ' + stockcode)
        stime = self.dynamicCall("GetChejanData(int)", 908)
        print('체결시간 = ' + stime)
        sname = self.dynamicCall("GetChejanData(int)", 302)
        print('종목명 = ' + sname)
        sname = self.dynamicCall("GetChejanData(int)", 902)
        print('미체결수량 = ' + sname)
        buyprice = self.dynamicCall("GetChejanData(int)", 910)
        print('체결가 = ' + buyprice)

        self.chejaneventloop.exit()
        pass

    def apitest(self):
        self.setinputvalue("종목코드", "039490")
        self.setinputvalue("기준일자", "20160101")
        self.setinputvalue("수정주가구분", "1")
        lRet = self.commrqdata("RQName", "OPT10081", "0", "0600")


    """
    [주문처리단계]
    주문 처리 순서
    SendOrder(주문발생) -> OnReceiveTRData(주문응답) -> OnReceiveMsg(주문메세지수신) -> OnReceiveChejan(주문접수/체결)
    ※ 주의(역전현상) : 주문건수가 폭증하는 경우 OnReceiveChejan 이벤트가 OnReceiveTRData 이벤트보다 앞서 수신될 수 있습니다.        

          [거래구분]
          00 : 지정가
          03 : 시장가
          05 : 조건부지정가
          06 : 최유리지정가
          07 : 최우선지정가
          10 : 지정가IOC
          13 : 시장가IOC
          16 : 최유리IOC
          20 : 지정가FOK
          23 : 시장가FOK
          26 : 최유리FOK
          61 : 장전시간외종가
          62 : 시간외단일가매매
          81 : 장후시간외종가
          ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.
    """

    def sendorder(self,
          sRQName, #// 사용자 구분명
          sScreenNo, #// 화면번호
          sAccNo,  #// 계좌번호 10자리
          nOrderType,  #// 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
          sCode, #// 종목코드 (6자리)
          nQty,  #// 주문수량
          nPrice, #// 주문가격
          sHogaGb,  # // 거래구분(혹은 호가구분)은 아래 참고
          sOrgOrderNo): # // 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.

        self.dynamicCall("SendOrder(Qstring, QString, QString, int, QString, int, int, QString, QString)",
                         [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo])

        self.chejaneventloop.exec_()
        pass

    """
    receiveMsg 1001 sendorder_req KOA_NORMAL_BUY_KP_ORD [100000] 모의투자 매수주문완료
    receiveTrData  1001 sendorder_req KOA_NORMAL_BUY_KP_ORD
    receiveChejanData 0 35 9201;9203;9205;9001;912;913;302;900;901;902;903;904;905;906;907;908;909;910;911;10;27;28;914;915;938;939;919;920;921;922;923;949;10010;969;819
    체결가 = 
    receiveChejanData 0 35 9201;9203;9205;9001;912;913;302;900;901;902;903;904;905;906;907;908;909;910;911;10;27;28;914;915;938;939;919;920;921;922;923;949;10010;969;819
    체결가 = 70300
    receiveChejanData 1 34 9201;9001;917;916;302;10;930;931;932;933;945;946;950;951;27;28;307;8019;957;958;918;990;991;992;993;959;924;10010;25;11;12;306;305;970
    체결가 = 
    """
    def buystock(self, code, qty):
        self.sendorder("sendorder_req", "1001", "8008681611", 1, code, qty, 0, "03", "")


    """
    receiveMsg 1001 sendorder_req KOA_NORMAL_SELL_KP_ORD [100000] 모의투자 매도주문완료
    receiveTrData  1001 sendorder_req KOA_NORMAL_SELL_KP_ORD
    receiveChejanData 0 35 9201;9203;9205;9001;912;913;302;900;901;902;903;904;905;906;907;908;909;910;911;10;27;28;914;915;938;939;919;920;921;922;923;949;10010;969;819
    종목코드 = A005930
    체결시간 = 152912
    종목명 = 삼성전자                                
    미체결수량 = 2
    체결가 = 
    receiveChejanData 1 34 9201;9001;917;916;302;10;930;931;932;933;945;946;950;951;27;28;307;8019;957;958;918;990;991;992;993;959;924;10010;25;11;12;306;305;970
    종목코드 = A005930
    체결시간 = 
    종목명 = 삼성전자                                
    미체결수량 = 
    체결가 = 
    """
    def sellstock(self, code, qty):
        self.sendorder("sendorder_req", "1001", "8008681611", 2, code, qty, 0, "03", "")

    def getstockinfo(self, code):
        #[opt10001: 주식기본정보요청]
        self.setinputvalue("종목코드", code)
        lRet = self.commrqdata("opt10001req", "OPT10001", "0", "1000")
        #print(self.trData)

    def update_stock_info(self):
        # check table date
        if self.mysqldbctrl.checktablehasthecolumn('update_table_date', 'stock_info', datetime.datetime.now().date()):
            return

        # clear Table
        self.mysqldbctrl.clear_table('stock_info')

        krxcollecting = True
        if krxcollecting is True:
            self.update_stock_info_from_krx()
        else:
            self.update_stock_info_from_openapi()

        self.mysqldbctrl.update_date_table_done('stock_info')

    def update_stock_info_from_krx(self):
        #krx 사이트에서 가져오는 게 더 정확하다.
        markettypes = ['stockMkt', 'kosdaqMkt', 'konexMkt']
        marketkind = ['kospi', 'kosdaq', 'konex']
        for i, market in enumerate(markettypes):
            stockdf = pd.read_html(
                'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=' + market,
                header=0)
            stockdf[0].종목코드 = stockdf[0].종목코드.map('{:06d}'.format)
            stockdf[0] = stockdf[0].rename(
                columns={'회사명': 'codename', '종목코드': 'code', '업종':'kind',
                         '주요제품': 'majorproduct', '상장일': 'createdate', '대표자명': 'ceo', '지역': 'home'})
            strcodelist = stockdf[0].code

            kospidaq = marketkind[i]

            for code in strcodelist:
                # check if table has the code
                if self.mysqldbctrl.checktablehasthecolumn('stock_info', 'code', code):
                    continue

                stockseries = stockdf[0].loc[stockdf[0].code == code]
                idx = stockseries.index[0]
                createdate = stockseries.createdate[idx]
                kind = stockseries.kind[idx]
                if type(stockseries.majorproduct[idx]) == str:
                    majorproduct = stockseries.majorproduct[idx]
                else:
                    #pd.isna(stockseries.majorproduct[idx]) or np.isnan(stockseries.majorproduct[idx]):
                    majorproduct = None

                ceo = stockseries.ceo[idx]
                home = stockseries.home[idx]
                codename = stockseries.codename[idx]
                stocksize = None
                thema = None

                stockinfo = self.KOA_Functions("GetMasterStockInfo", code)
                stockinfolist = stockinfo.split(';')
                if len(stockinfolist) >= 2 and stockinfolist[1] != '':
                    stocksize = stockinfolist[1].split('|')[1]
                time.sleep(0.4)
                construction = self.dynamicCall("GetMasterConstruction(QString)", code)
                time.sleep(0.4)
                stockstate = self.dynamicCall("GetMasterStockState(QString)", code)
                time.sleep(0.4)

                print(code, codename, stockinfo)

                self.getstockinfo(code)

                self.trData.append(datetime.datetime.strptime(createdate, '%Y-%m-%d').date())
                self.trData.append(kospidaq)
                self.trData.append(stocksize)
                self.trData.append(thema)
                self.trData.append(kind)
                self.trData.append(construction)
                self.trData.append(stockstate)
                self.trData.append(majorproduct)
                self.trData.append(ceo)
                self.trData.append(home)

                # database save
                sql = "INSERT INTO stock_info (code, name, facevalue, facevalueunit, capital, stockcnt, marketcap, foreignrate, " \
                      "PER, EPS, ROE, PBR, EV, BPS, " \
                      "salesrevenue, opincome, netincome, " \
                      "createdate, kospidaq, stocksize, thema, kind, construction, stockstate, majorproduct, ceo, home) " \
                      "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                      "%s, %s, %s)"

                data = self.trData
                # print(code, codename)
                # ['000020', '동화약품', 1000, 279, 27931, 3869, Decimal('3.00'),
                # Decimal('13.57'), 1021, Decimal('9.0'), Decimal('1.16'), Decimal('8.38'), 11950,
                # 2721, 232, 287, datetime.datetime(1976, 3, 24, 0, 0), '거래소', '소형주', '', '의약품', '정상',
                # '증거금30%|담보대출|신용가능']
                # ['000075', '삼양홀딩스우', 5000, 15, 304, 210, Decimal('0.70'),
                # None, None, None, None, None, None,
                # datetime.date(1992, 2, 21), '거래소', '', '', '금융업', '정상', '증거금40%']
                self.mysqldbctrl.insertstockinfo(sql, tuple(data))

    def update_stock_info_from_openapi(self):

        #stockinfo = self.KOA_Functions("GetMasterStockInfo", "395400")
        #print(stockinfo)
        #return


        """
        # Open API 로 Stock Info 를 가져온다.
        GetCodeListByMarket(BSTR sMarket // 시장구분값)
        [시장구분값]
        0: 코스피 => 코스피 종목 분류시 ETF,ETN, 뮤추얼펀드, 리츠등의 종목을 포함, 상장폐지 종목도 데이터 처리를 위해 대략 3일정도 유지
        10: 코스닥
        3: ELW
        8: ETF
        50: KONEX
        4: 뮤추얼펀드
        5: 신주인수권
        6: 리츠
        9: 하이얼펀드
        30: K - OTC
        """
        # 쿼리 코드리스트 수 kospi count : 12110,  kosdaq count : 10717, konex count :
        # 시장구분이 거래소만 : about 919
        # krx 사이트 종목수 : 940  1,531  131 = 2602
        codelist = self.dynamicCall("GetCodeListByMarket(QString)", "0")
        strcodelist = codelist.split(';')
        #print('Kosdaq Code Count : ', len(codelist))

        for code in strcodelist:

            # check if table has the code
            if self.mysqldbctrl.checktablehasthecolumn('stock_info', 'code', code):
                continue

            '시장구분0|거래소;시장구분1|소형주;업종구분|의약품;'
            kospidaq = ''
            stocksize = ''
            kind = ''
            thema = ''

            stockinfo = self.KOA_Functions("GetMasterStockInfo", code)
            stockinfolist = stockinfo.split(';')
            if len(stockinfolist) >= 1 and stockinfolist[0] != '':
                kospidaq = stockinfolist[0].split('|')[1]
            if kospidaq != '거래소':
                time.sleep(0.1)
                continue
            if len(stockinfolist) >= 2 and stockinfolist[1] != '':
                stocksize = stockinfolist[1].split('|')[1]
            if len(stockinfolist) >= 3 and stockinfolist[2] != '':
                kind = stockinfolist[2].split('|')[1]

            codename = self.dynamicCall("GetMasterCodeName(QString)", code)
            time.sleep(0.2)
            construction = self.dynamicCall("GetMasterConstruction(QString)", code)
            time.sleep(0.2)
            createdate = self.dynamicCall("GetMasterListedStockDate(QString)", code)
            time.sleep(0.2)
            stockstate = self.dynamicCall("GetMasterStockState(QString)", code)
            time.sleep(0.2)

            print(code, codename, stockinfo)

            self.getstockinfo(code)
            # ['000020', '동화약품', '1000', '279', '27931', '3896', '+3.00',
            # '13.67', '1021', '9.0', '1.17', '8.46', '11950', '2721', '232', '287']

            self.trData.append(datetime.datetime.strptime(createdate, '%Y%m%d').date())
            self.trData.append(kospidaq)
            self.trData.append(stocksize)
            self.trData.append(thema)
            self.trData.append(kind)
            self.trData.append(construction)
            self.trData.append(stockstate)

            # database save
            sql = "INSERT INTO stock_info (code, name, facevalue, facevalueunit, capital, stockcnt, marketcap, foreignrate, " \
                  "PER, EPS, ROE, PBR, EV, BPS, " \
                  "salesrevenue, opincome, netincome, " \
                  "createdate, kospidaq, stocksize, thema, kind, construction, stockstate)" \
                  "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data = self.trData
            #print(code, codename)
            # ['000020', '동화약품', 1000, 279, 27931, 3869, Decimal('3.00'),
            # Decimal('13.57'), 1021, Decimal('9.0'), Decimal('1.16'), Decimal('8.38'), 11950,
            # 2721, 232, 287, datetime.datetime(1976, 3, 24, 0, 0), '거래소', '소형주', '', '의약품', '정상',
            # '증거금30%|담보대출|신용가능']
            # ['000075', '삼양홀딩스우', 5000, 15, 304, 210, Decimal('0.70'),
            # None, None, None, None, None, None,
            # datetime.date(1992, 2, 21), '거래소', '', '', '금융업', '정상', '증거금40%']
            self.mysqldbctrl.insertstockinfo(sql, tuple(data))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    DbCollector()