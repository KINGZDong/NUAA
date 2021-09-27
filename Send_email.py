#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pip:pip install library_you_need -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
'''
#--------------------------------------------------------------#
#                                                              #
#--------------------------------------------------------------#
#
#                   @Project Name：Auto_Clock_in_NUAA                    #
#
#                   @File Name：Send_email.py                           #
#
#                   @Programmer：Wangzhidong                   #
#
#                   @Start Date：2021/9/27 0027 14:21          #
#
#                   @Last Update：2021/9/27 0027 14:21         #
#-------------------------------------------------------------#   
#Class:
#                  SendEmail
#-------------------------------------------------------------#
'''

import smtplib
from email.mime.text import MIMEText
msg_from = '161983374@qq.com'  # 发送方邮箱
passwd = 'yybemuygyoojbgeb'  # 填入发送方邮箱的授权码
msg_to = '2557833850@qq.com'  # 收件人邮箱

subject = "i南航每日打卡结果"  # 主题
class SendEmails():
    def Send(self, content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")

        except(s.SMTPException):
            print("发送失败")

        finally:
            s.quit()


