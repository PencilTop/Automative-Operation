import os
import re
from datetime import datetime
from config import *

from collections import namedtuple

def GetLogData():
    log_data_dic = {}
    title = ''
    title_pattern_string = '^' + '-'*12 + ' ' + '([\dA-Z\s\/\:\,\(\)]+)' + ' ' + '-'*12 + '$'
    title_pattern = re.compile(title_pattern_string)
    trans_sum_pattern = re.compile('\s+(\d+)$')
    stats_csr_pattern = re.compile('^CSR\s+(\d+)$')
    stats_ivr_pattern = re.compile('^IVR\s+(\d+)$')
    stats_d_pattern = re.compile('^D\s+(\d+)$')
    stats_e_pattern = re.compile('^E\s+(\d+)$')
    trans_tpmc_pattern = re.compile('^(\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2})\s+(\d+)$')
    trans_tps_pattern = re.compile('^(\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}:\d{2})\s+(\d+)$')
    try:
        with open(os.path.join(WORKING_DIR, LOG_FILE), encoding='utf8') as log:
            for line in log.readlines():
                title_match = title_pattern.match(line)
                if title_match is not None:
                    title = title_match.groups()[0]
                if title == LOG_SEARTH_TITLE[0]:
                    trans_sum_match = trans_sum_pattern.match(line)
                    if trans_sum_match is not None:
                        log_data_dic['TRANS_SUM'] = trans_sum_match.groups()[0]
                elif title == LOG_SEARTH_TITLE[1][0]:
                    stats_csr_match = stats_csr_pattern.match(line)
                    stats_ivr_match = stats_ivr_pattern.match(line)
                    if stats_csr_match is not None:
                        log_data_dic['STATS_CSR'] = stats_csr_match.groups()[0]
                    elif stats_ivr_match is not None:
                        log_data_dic['STATS_IVR'] = stats_ivr_match.groups()[0]
                elif title.startswith(LOG_SEARTH_TITLE[2][0]):
                    stats_d_match = stats_d_pattern.match(line)
                    stats_e_match = stats_e_pattern.match(line)
                    if stats_d_match is not None:
                        log_data_dic['STATS_D'] = stats_d_match.groups()[0]
                    elif stats_e_match is not None:
                        log_data_dic['STATS_E'] = stats_e_match.groups()[0]
                elif title == LOG_SEARTH_TITLE[3]:
                    trans_tpmc_match = trans_tpmc_pattern.match(line)
                    if trans_tpmc_match is not None:
                        log_data_dic['TRANS_TPMC'] = trans_tpmc_match.groups()
                elif title == LOG_SEARTH_TITLE[4]:
                    trans_tps_match = trans_tps_pattern.match(line)
                    if trans_tps_match is not None:
                        log_data_dic['TRANS_TPS'] = trans_tps_match.groups()
        return log_data_dic
    except FileNotFoundError as e:
        print('Log file can not be found!')
        print(e.args)


if __name__=='__main__':
    print(GetLogData())
