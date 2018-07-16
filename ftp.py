# coding=utf-8
from ftplib import FTP
import time
import os
import configparser
import shutil


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

    def __init__(self):
        configname = 'config.ini'
        config = configparser.ConfigParser()
        config.read(configname)
        self.Filepath = config.get('DataFilePath', 'Filepath')
        self.FtpServer = config.get('FTP', 'server')
        self.FtpPort = config.get('FTP', 'port')
        self.FtpUser = config.get('FTP', 'user')
        self.FtpPwd = config.get('FTP', 'pwd')
        self.Sleep = config.get('FTP', 'sleep')
        self.FTPSavePath = config.get('FTP', 'savepath')
        self.SourceDir = config.get('copysourceDir', 'sourceDir')
        self.SourceDirFile = config.get('copysourceDir', 'sourceDirFile')
        # sourceDirFile
        self.TargetDir = config.get('copytargetDir', 'targetDir')
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        try:
            self.ftp.connect(self.FtpServer, self.FtpPort)  # 连接
            self.ftp.login(self.FtpUser, self.FtpPwd)  # 登录，如果匿名登录则用空串代替即可
            self.ftp.cwd(self.FTPSavePath)
        except:
            print("FPT连接登录出错 Connect Errnor")

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


def main():
    var = 1
    while (var == 1):
        mydatafileftp = DataFileFtp()
        mydatafileftp.FileCopy()
        time.sleep(10)
        mydatafileftp.UpPathAllFile()
        print("上传文件成功 OK " + str(time.clock()))
        time.sleep(int(mydatafileftp.Sleep))


if __name__ == "__main__":
    # main()
    mydatafileftp = DataFileFtp()
    print(mydatafileftp.Filepath)
