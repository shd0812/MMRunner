import logging
import time
import os
from mconf.setting import LOG_PATH,LEVEL
from time import sleep
import threading
import traceback
# PATH = lambda p: os.path.abspath(
#     os.path.join(os.path.dirname(__file__), p)
# )

#记录异常
try:
    a='1'
    b='2'
except:
    f=open("c:log.txt",'a')
    traceback.print_exc(file=f)
    f.flush()
    f.close()


class Log:
    def __init__(self, ):
        #phone_name = '滴滴'
        global logger, resultPath, logPath
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        # logPath = os.path.join(LOG_PATH, (phone_name + time.strftime('%Y-%m-%d-%H', time.localtime())))
        logPath = os.path.join(LOG_PATH, ( time.strftime('%Y-%m-%d-%H', time.localtime())))
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        self.checkNo = 0
        if LEVEL =='info':
            level=logging.INFO
        elif LEVEL =='debug':
            level=logging.DEBUG
        elif LEVEL =='warn' or LEVEL =='warning':
            level=logging.WARNING
        elif LEVEL =='error':
            level=logging.WARNING
        elif LEVEL =='critical':
            level = logging.CRITICAL
        else:
            raise Exception

        logging.basicConfig(level=level,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()

        #self.logger.setLevel(logging.INFO)

        # create handler,write log
        fh = logging.FileHandler(os.path.join(logPath, "outPut.log"))
        # Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
       # console = logging.StreamHandler()
        #console.setLevel(logging.INFO)
       # console.setFormatter(formatter)

        self.logger.addHandler(fh)
        #self.logger.addHandler(console)

    def getMyLogger(self):
        """get the logger
        :return:logger
        """
        return self.logger

    def m_info(self, caseNo):
        """build the start log
        :param caseNo:
        :return:
        """
        startLine = "----  " + caseNo + "   " + "   " + \
                    "  ----"

        self.logger.info(startLine)

    def m_warning(self, caseNo):
        """build the start log
        :param caseNo:
        :return:
        """
        startLine = "----  " + caseNo + "   " + "   " + \
                    "  ----"
        # startLine = "----  " + caseNo + "   " + "START" + "   " + \
        #             "  ----"
        self.logger.warning(startLine)
    def m_debug(self, caseNo):
        """build the start log
        :param caseNo:
        :return:
        """
        startLine = "----  " + caseNo + "   " + "   " + \
                    "  ----"

        self.logger.debug(startLine)
    def m_error(self, caseNo):
        """build the start log
        :param caseNo:
        :return:
        """
        startLine = "----  " + caseNo + "   " + "   " + \
                    "  ----"
        # startLine = "----  " + caseNo + "   " + "START" + "   " + \
        #             "  ----"
        self.logger.error(startLine)



    def writeResult(self, result):
        """write the case result(OK or NG)
        :param result:
        :return:
        """
        reportPath = os.path.join(logPath, "report.txt")
        flogging = open(reportPath, "a")
        try:
            flogging.write(result + "\n")
        finally:
            flogging.close()
        pass

    def resultOK(self, caseNo):
        self.writeResult(caseNo + ": OK")

    def resultNG(self, caseNo, reason):
        self.writeResult(caseNo + ": NG--" + reason)




class myLog:
    """
    This class is used to get log
    """

    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def getLog():
        if myLog.log is None:
            myLog.mutex.acquire()
            myLog.log = Log()
            myLog.mutex.release()

        return myLog.log


if __name__ == "__main__":
    logTest = myLog.getLog()
    # logger = logTest.getMyLogger()
    logTest.m_info("11111111111111111111111")
    logTest.m_info("11111111111111111111111")