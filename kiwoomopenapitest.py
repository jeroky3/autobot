import sys

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class openapi(QAxWidget):
    def __init__(self):
        super().__init__()

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
        self.apitest()

        #self.buystock("005930", 1)
        #self.sellstock("005930", 1)

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
        self.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)
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
        print('receiveTrData ', sScrNo, sRQName, sTrCode)
        self.treventloop.exit()

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


app = QApplication(sys.argv)
openapi()