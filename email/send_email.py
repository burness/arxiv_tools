# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name='SendMail')
import time
import requests
# sh = logging.StreamHandler(stream=None)
# logger.addHandler(sh)

# 第三方 SMTP 服务
class SendEmail(object):
    def __init__(self, mail_host, mail_user, mail_pass, area_week_file):
        config = {}
        config['mail_host'] = mail_host
        config['mail_user'] = mail_user
        config['mail_pass'] = mail_pass
        self._set_config(**config)
        self.area_week_file = area_week_file
    
    def _set_config(self, **config):
        self.mail_host = config['mail_host']
        self.mail_user = config['mail_user']
        self.mail_pass = config['mail_pass']

    def set_sender(self, sender_email):
        self.sender_email = sender_email
    
    def set_receivers(self, receivers_email):
        self.receivers_email = receivers_email

    def get_daily_sentence(self):
        try:
            result = requests.get('http://open.iciba.com/dsapi/').json()
            daily = result['note']
        except:
            daily = 'Do Better Every DaY'
        return daily

    def _format_text_html(self):
        '''
        return the html text of the area_week_file
        '''
        # TODO: How to format the html text form the area_week file
        with open(self.area_week_file, 'r') as fread:
            area = self.area_week_file.split('/')[3]
            today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            self.message_text = '<p><h1>Hello All Bros:</h1></p><p><h2>{0}\t{1} Arxiv Paper Lists</h2></p>'.format(area,today)
            for line in fread.readlines():
                paper_all_info = line.split('\t')
                paper_key = paper_all_info[0]
                paper_title = paper_all_info[1]
                paper_link = paper_all_info[2]
                author_list = paper_all_info[3].split(',')
                author_link_list = paper_all_info[4].split(',')
                paper_subject = paper_all_info[5]
                pdf_describe_links = paper_all_info[6]
                paper_link = '<p><a href={0}>{1}</a><br>'.format(paper_link, paper_title)
                author_link = ['<a href={0}>{1}</a>'.format(author_link_list[index],author) for index, author in enumerate(author_list)]
                temp_message_text = paper_link+','.join(author_link)
                self.message_text += temp_message_text + '<br></p>'
            self.message_text += '<br><p>'+self.get_daily_sentence().encode('utf-8')+'</p><p>----By Arxiv Tools</p>'
    
    def _format_head(self):
        self.message = MIMEText(self.message_text, 'html', 'utf-8')
        # self.message['From'] = Header(self.sender_email.split('@')[0]+'<'+self.sender_email+'>', 'utf-8')
        self.message['From'] = self.sender_email
        self.message['To'] =  ','.join(self.receivers_email)
        # self.message['To'] = self.receivers_email
        subject = 'Arxiv Papers'
        self.message['Subject'] = Header(subject, 'utf-8')

    def send(self):
        try:
            self._format_text_html()
            self._format_head()
            smtpObj = smtplib.SMTP_SSL(self.mail_host) 
            logger.info('Trying Connect')
            # logger.info('Connnect Successfully')
            smtpObj.login(self.mail_user,self.mail_pass)
            logger.info('Login Successfully')
            smtpObj.sendmail(self.message['From'], self.receivers_email, self.message.as_string())
            print '邮件发送成功'
        except Exception, e:
            print 'Error: 无法发送邮件'
            print str(e)

if __name__ == '__main__':
    mail_host = 'smtp.qq.com'
    mail_user = '363544964@qq.com'
    mail_pass = 'tfzgdvakzqtpbhhe'
    send_email = SendEmail(mail_host=mail_host, mail_user=mail_user, mail_pass=mail_pass, area_week_file='../papers/pdfs/cs_cv/2017-03-06/summary.csv')
    send_email.set_sender(sender_email='363544964@qq.com')
    send_email.set_receivers(receivers_email=['dss_1990@sina.com','burness1990@163.com'])
    send_email.send()

