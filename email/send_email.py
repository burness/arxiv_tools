# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
class SendEmail(object):
    def __init__(self):
        pass
    
    def set_config(self, **config):
        self.mail_host = config['mail_host']
        self.mail_user = config['mail_user']
        self.mail_pass = config['mail_pass']

    def set_sender(self, sender_email):
        self.sender_email = sender_email
    
    def set_receivers(self, receivers_email):
        self.receivers_email = receivers_email

    def format_text_html(self, area_week_file):
        '''
        return the html text of the area_week_file
        '''
        # TODO: How to format the html text form the area_week file
        self.message_text = '123'
    
    def format_head(self, **params):
        self.message = MIMEText(self.message_text, 'html', 'utf-8')
        self.message['From'] = Header('Arxiv Papers','utf-8')
        # self.message['To'] =  Header('', 'utf-8')
        subject = 'Arxiv Papers'
        self.message['Subject'] = Header(subject, 'utf-8')

    def send(self, **params):
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(self.mail_host, 25)    # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user,self.mail_pass)  
            smtpObj.sendmail(self.sender_email, self.receivers_email, self.message.as_string())
            print '邮件发送成功'
        except smtplib.SMTPException:
            print 'Error: 无法发送邮件'

    
# mail_host='smtp.XXX.com'  #设置服务器
# mail_user='XXXX'    #用户名
# mail_pass='XXXXXX'   #口令 


# sender = 'from@runoob.com'
# receivers = ['429240967@qq.com']

# mail_msg = '''
# # <p>Python 邮件发送测试...</p>
# # <p><a href='http://www.runoob.com'>这是一个链接</a></p>
# # '''
# message = MIMEText(mail_msg, 'html', 'utf-8')
# message['From'] = Header('菜鸟教程', 'utf-8')
# message['To'] =  Header('测试', 'utf-8')

# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')


# try:
#     smtpObj = smtplib.SMTP() 
#     smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
#     smtpObj.login(mail_user,mail_pass)  
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print '邮件发送成功'
# except smtplib.SMTPException:
#     print 'Error: 无法发送邮件'
