#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 
#_*_coding:utf-8_*_

import os
import shutil
import stat
import datetime
from collections import namedtuple

USERS = './passwd-test'
BASE_USERS = './base_users'
USERS_LOG = './users.log'

def CopyBaseUsers():
    if not os.path.isfile(BASE_USERS) or not os.path.isfile(USERS_LOG):
        try:
            shutil.copyfile(USERS, BASE_USERS)
            print(r'基础用户信息拷贝完毕。')
            f = open(USERS_LOG, 'w')
            f.close
            print(r'日志文件创建完毕。')
        except Exception as e:
            print(r'基础用户文件或日志文件创建失败。')
            print(e.args)       

def ReadUsers(users_file):
    try:
        with open(users_file) as file:
            for line in file.readlines():
                if not line.startswith(r'#'):
                    usermsg = line.split(':')
                    user = namedtuple('User', ['name',
                                               'passwd',
                                               'uid',
                                               'gid',
                                               'fulname',
                                               'home',
                                               'shell'])
                    user.name = usermsg[0]
                    user.passwd = usermsg[1]
                    user.uid = usermsg[2]
                    user.gid = usermsg[3]
                    user.fulname = usermsg[4]
                    user.home = usermsg[5]
                    user.shell = usermsg[6]
                    yield user
    except Exception as  e:
        print("{} 打开失败。".format(users_file))
        print(e.args)
        
def ContrastUsers(base_users, users):
    sorted_base_users = list(sorted(base_users, key=lambda user: user.name))
    sorted_users = list(sorted(users, key=lambda user: user.name))
    base_users_count = len(sorted_base_users)
    users_count = len(sorted_users)
    base_user_index = 0
    user_index = 0
    now = datetime.datetime.now
    while base_user_index < base_users_count and user_index < users_count:
        base_user = sorted_base_users[base_user_index]
        user = sorted_users[user_index]
        if base_user.name > user.name:
            yield "{} 检测 新增用户：{}".format(now(), user.name)
            user_index += 1
        elif base_user.name < user.name:
            yield "{} 检测 删除用户：{}".format(now(), base_user.name)
            base_user_index += 1
        else:
            if base_user.passwd != user.passwd:
                yield "{} 检测 用户 {} 密码 更改".format(now(), base_user.name)
            if base_user.uid != user.uid:
                yield "{} 检测 用户 {} uid 更改".format(now(), base_user.name)
            if base_user.gid != user.gid:
                yield "{} 检测 用户 {} gid 更改".format(now(), base_user.name)
            if base_user.fulname != user.fulname:
                yield "{} 检测 用户 {} 全名 更改".format(now(), base_user.name)
            if base_user.home != user.home:
                yield "{} 检测 用户 {} 家目录 更改".format(now(), base_user.name)
            if base_user.shell != user.shell:
                yield "{} 检测 用户 {} shell 更改".format(now(), base_user.name)
            user_index += 1
            base_user_index += 1
    if base_user_index == base_users_count and user_index < users_count:
        while user_index < users_count:
            user = sorted_users[user_index]
            yield "{} 检测 新增用户：{}".format(now(), user.name)
            user_index += 1
    elif base_user_index < base_users_count and user_index == users_count:
        while base_user_index < base_users_count:
            base_user = sorted_base_users[base_user_index]
            yield "{} 检测 删除用户：{}".format(now(), base_user.name)
            base_user_index += 1
    yield "{} 检测 结束".format(now())
        
def WriteLogs(iter_logs, log_file):
    try:
        with open(log_file, 'a') as log:
            for il in iter_logs:
                print(il)
                log.writelines(il+'\n')
    except Exception as e:
        print("{} 写入失败".format(log_file))
        print(e.args)
            
        
if __name__=='__main__':
    #    CopyBaseUsers()
    base_users = ReadUsers(BASE_USERS)
    users = ReadUsers(USERS)
    ilogs = ContrastUsers(base_users, users)
    WriteLogs(ilogs, USERS_LOG)
    print('用户检测完毕，日志已写入日志文件。')
    
