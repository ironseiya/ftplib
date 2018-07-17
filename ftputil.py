# _*_ coding:utf-8 _*_
from ftplib import FTP
import time
import os
import configparser
import shutil
import ast
import zipfile
import logging

class DataFileFtp:
    # 要上传文件路径
    Filepath = ""
    # FTP 地址
    FtpServer = ''
    # FTP 端口
    FtpPort = 21
    # FTP USERNAME
    FtpUser = ''
    # FTP PWD
    FtpPwd = ''
    # 多少时间执行一次（单位 秒）
    Sleep = 60
    ftp = FTP()
    # 复制文件-源路径
    SourceDir = ""
    # 复制文件-源路径下文件名 如 a.txt,b.txt ,如果是空  代带所有文件
    SourceDirFile = ""
    # 目标路径
    TargetDir = ""
    # 保到下 FTP 那个文件夹下。
    FTPSavePath = ""

    # 当前IP地址

    # 当前保存份数

    def __init__(self):

        logging.basicConfig(level=logging.WARNING,
                            filename='./log/log.txt',
                            filemode='w',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        logging.info("程序")
        configname = 'ftp.ini'
        config = configparser.ConfigParser()
        config.read(configname)
        self.FtpServer = config.get('FTP', 'server')
        self.FtpPort = config.get('FTP', 'port')
        self.FtpUser = config.get('FTP', 'user')
        self.FtpPwd = config.get('FTP', 'pwd')
        self.FTPSavePath = config.get('FTP', 'savepath')
        self.SourceDir = config.get('copysourceDir', 'sourceDir')
        self.SourceDirFile = config.get('copysourceDir', 'sourceDirFile')
        # sourceDirFile
        self.TargetDir = config.get('copytargetDir', 'targetDir')
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息

        self.Ip = config.get('local', 'ip')
        self.Split = config.get('local', 'split')
        self.CurrentSplit = config.get('local', 'currentSplit')

        currentSplit = int(self.CurrentSplit) + 1
        if currentSplit > int(self.Split):
            currentSplit = 1

        config.set('local', 'currentSplit', str(currentSplit))  # 添加值

        with open(configname, 'w') as fw:  # 循环写入
            config.write(fw)

        try:
            self.ftp.connect(self.FtpServer, int(self.FtpPort))  # 连接
            self.ftp.login(self.FtpUser, self.FtpPwd)  # 登录，如果匿名登录则用空串代替即可
            try:
                self.ftp.cwd(self.FTPSavePath)
            except Exception as e:
                try:
                    self.ftp.mkd(self.FTPSavePath)
                    self.ftp.cwd(self.FTPSavePath)
                except:
                    msg = 'You have no authority to make directory: %s' % self.FTPSavePath
                    print(msg)
        except Exception as e:
            print("FPT连接登录出错 Connect Errnor" + str(e))

    def UpPathAllFile(self):
        try:
            for filename in os.listdir(self.Filepath):
                # print (self.Filepath+"\\"+filename)
                fl = open(self.Filepath + "\\" + filename, "rb")  # 读取文件
                # fname= fl.name.split("\\")[-1]
                self.ftp.storbinary("STOR " + filename, fl)  # 上传文件
                fl.close()
            self.ftp.quit()
        except:
            print("上传文件出错：UpPathAllFile except")

    def FileCopy(self):
        try:
            if len(self.SourceDirFile) == 0:  # 空 所有文件
                for allfl in os.listdir(self.SourceDir):
                    sourcefilepath = self.SourceDir + "\\" + allfl
                    if os.path.isfile(sourcefilepath):  # 判断是否是文件
                        shutil.copyfile(sourcefilepath, self.TargetDir + "\\" + allfl)
                        pass
            else:  # 复制指定文件
                fs = self.SourceDirFile.split(',')  #
                for fnam in fs:
                    fp = self.SourceDir + "\\" + fnam
                    print(fp)
                    shutil.copyfile(fp, self.TargetDir + "\\" + fnam)
        except:
            print("Copy Error")

    def createZip(self, dir, note=''):
        '''
        将文件夹下的文件保存到zip文件中。
        :param filePath: 待备份文件
        :param savePath: 备份路径
        :param note: 备份文件说明
        :return:
        '''

        today = time.strftime('%Y%m%d')
        now = time.strftime('%H%M%S')
        fileList = []

        targetPath = self.TargetDir + os.sep + self.Ip + os.sep + dir.replace(os.sep, "#")
        ver = "v" + self.CurrentSplit

        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
            print('mkdir successful')

        # 清除对应版本
        for file in os.listdir(targetPath):
            if file.endswith(ver + ".zip"):
                os.remove(targetPath + os.sep + file)

        if len(note) == 0:
            target = targetPath + os.sep + today + now + "v" + self.CurrentSplit + '.zip'
        else:
            target = targetPath + os.sep + today + now + '_' + note + "v" + self.CurrentSplit + '.zip'

        # targetPath = /Users/lbb/PycharmProjects/ftplib/temp/10.66.12.10/#Users#lbb#PycharmProjects#ftplib



        newZip = zipfile.ZipFile(target, 'w')
        for dirpath, dirnames, filenames in os.walk(self.Filepath):
            for filename in filenames:
                fileList.append(os.path.join(dirpath, filename))
        for tar in fileList:
            newZip.write(tar, tar[len(self.Filepath):])  # tar为写入的文件，tar[len(filePath)]为保存的文件名
        newZip.close()
        print('backup to', target)

        # 写入配置文件

    def updateZipFile(self, dir):

        uploadFile = self.TargetDir + os.sep + self.Ip + ".zip"
        try:
            # print (self.Filepath+"\\"+filename)
            fl = open(uploadFile, "rb")  # 读取文件
            # fname= fl.name.split("\\")[-1]
            self.ftp.storbinary("STOR " + self.Ip + ".zip", fl)  # 上传文件
            fl.close()
            self.ftp.quit()
        except:
            print("上传文件出错：UpPathAllFile except")

    def createAllZipFile(self):

        targetPathFile =  self.TargetDir + os.sep + self.Ip + ".zip"
        newZip = zipfile.ZipFile(targetPathFile, 'w')
        fileList = []
        for dirpath, dirnames, filenames in os.walk(self.TargetDir):
            for filename in filenames:
                fileList.append(os.path.join(dirpath, filename))
        for tar in fileList:
            newZip.write(tar, tar[len(self.Filepath):])  # tar为写入的文件，tar[len(filePath)]为保存的文件名
        newZip.close()
        print('backup to', targetPathFile)


def main                                                                                                        ():
    mydatafileftp = DataFileFtp()
    sourceDirs = ast.literal_eval(mydatafileftp.SourceDir)
    for dir in sourceDirs:
        # 本地copy文件
        mydatafileftp.createZip(dir)

        #创建压缩文件
        mydatafileftp.createAllZipFile()

        # 上传到服务器
        mydatafileftp.updateZipFile(dir)


if __name__ == "__main__":
    main()
