from collections import namedtuple
from collections import defaultdict

WORKING_DIR = r'.'
DAILY_TRADING_VOLUMN_EXCEL = r'.\业务集中日报巡检.xlsx'
LOG_FILE = r'ccbat.txt'


AOMS_USER = namedtuple('AOMS_USER', ['user', 'passwd'])
AOMS_USER.user = '12014457'
AOMS_USER.passwd = 'a4038361'


HOST = 'ccbat03'
COMMAND = 'cat'
PAMAMETER = '/app/webadm/dailycheck/jiaoyi/transnew.20190520.log'
LOG_TXT = r'ccbat.txt'

SPLUNK_URL = r'http://splkh6.spdb.com/zh-CN/app/cc/cc_metric_transaction_overview?earliest=-1d%40d&latest=%40d'
SPLUNK_USER = namedtuple('SPLUNK_USER', ['user', 'passwd'])
SPLUNK_USER.user = '12014457'
SPLUNK_USER.passwd = 'a4038361'

LOG_SEARTH_TITLE = ( 'TRANS SUM',
             (r'STATS BY IVR/CSR/BATCH', ('CSR', 'IVR')),
             (r'STATS BY CARD TYPE', ('D', 'E')),
             r'TRANS TPMC',
             r'TRANS TPS' )

#LOG_TITLE_DIC = defaultdict(LOG_TITLE_LIST)

if __name__=='__main__':
    print(LOG_SEARTH_TITLE[1][0])

