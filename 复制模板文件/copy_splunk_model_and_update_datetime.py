import os, sys
import re
import datetime
import time
import shutil

from config import splunk_working_dir, model_dir, monthDic

class SplunkDailyCheck:
    def __init__(self, workingPath, modelPath=None, days=1):
        self.workingPath = workingPath
        self.days = days
        if modelPath is None:
            self.modelPath = os.path.join(workingPath, model_dir)
        else:
            self.modelPath = modelPath
        
        
    def copyModelToWork(self, workDateString):
        """
                    将模板拷贝进工作目录中去
        1、模板拷贝进临时目录，临时目录不存在，以·Model+日期·形式创建 
        2、对临时模板目录中的文件夹名及文件名中含有日期的部分进行更改，改成需要的日期
        3、将临时模板目录中的所有文件递归移动进对应月份中目录中去，并删除临时模板目录
        4、workDateString必须保证是八位数字组成的字符串，否则程序难以达到原有目的
        """
        if not workDateString.isdigit() or len(workDateString) != 8:
            sys.exit(' the date string format is not correct. ')
        #将模板文件拷贝进临时模板目录
        tmpName = 'Model' + workDateString
        if tmpName not in os.listdir(self.workingPath):
            tmpDst = os.path.join(self.workingPath, tmpName)
        else:
            print(' Temporary model directory:', tmpName, 'is already in working directory! ')
            sys.exit( 1 )
        try:
            shutil.copytree(self.modelPath, tmpDst, ignore=shutil.ignore_patterns('*.zip', '*.7z'))
        except Exception as e:
            print(e.args)
            print(' Model files copy process failed! ')
            sys.exit(2)
        
        #更改模板文件名中日期部分
        modeldirs = [
            (parent, dirname)
            for parent, dirnames, _ in os.walk(tmpDst)
            for dirname in dirnames
            ]
        modeldirs.reverse()
        modelfiles = [
            (parent, filename)
            for parent, _, filenames in os.walk(tmpDst)
            for filename in filenames            
            ]
                  
        for parent, filename in modelfiles:
            try:
                old_date = re.findall('\d+', filename)[0]
            except:
                print('file', filename, 'does not have a date.')
                sys.exit( 3 )
            if old_date.isdigit() and len(old_date) == 8:
                newname = filename.replace(old_date, workDateString)
                os.rename(os.path.join(parent, filename), os.path.join(parent, newname))
            else:
                print('model file', filename, 'time format is not correct.')
                sys.exit( 4 )
        for parent, dirname in modeldirs:
            try:
                old_date = re.findall('\d+', dirname)[0]
            except:
                print('directory', dirname, 'does not have a date.')
                sys.exit( 5 )
            if old_date.isdigit() and len(old_date) == 8:
                newname = dirname.replace(old_date, workDateString)
                os.rename(os.path.join(parent, dirname), os.path.join(parent, newname))
            else:
                print('model dir', dirname, 'time format is not correct.')
                sys.exit( 6 )
    
        #创建月份工作目录
        workmonth = monthDic[int(workDateString[4:6])]
        monthdir = os.path.join(self.workingPath, workmonth)
        if workmonth not in os.listdir(self.workingPath):
            os.makedirs(monthdir)
        for f in os.listdir(tmpDst):
            try:
                shutil.move(os.path.join(tmpDst, f), monthdir)
            except Exception as e:
                print('model files', f, 'moving failed.')
                print(e.args)
                sys.exit( 7 )
                
        #删除临时模板目录
        shutil.rmtree(tmpDst, ignore_errors=True)
        
        print(workDateString, 'Model copied successfully.')
        time.sleep(3)
     
    @staticmethod        
    def genDateString(self):
        for d in range(1, self.days+1):
            daysdelta = datetime.timedelta(days=d)
            yield str(datetime.date.today() - daysdelta).replace('-', '')

    def testDateString(self):
        for s in self.genDateString(self):
            print(s)
            
    def copyDaysBeforeModel(self):
        for dateString in self.genDateString(self):
            self.copyModelToWork(dateString)
    
    

if __name__=='__main__':
    testdaily = SplunkDailyCheck(splunk_working_dir, days=1)
#    testdaily.copyModelToWork('20190203')     
#    testdaily.testDateString()  
    testdaily.copyDaysBeforeModel()
    
    
        
             
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


