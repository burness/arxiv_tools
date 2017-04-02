from spider.download_pdfs import run_all
import time
import logging
import os
from send_email.send_email import SendEmail

logger = logging.getLogger('arxiv_tools')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

USER_INFO_FILE = './flask/static/user_info.csv'
MAIL_HOST = 'smtp.qq.com'
MAIL_USER = '363544964@qq.com'
MAIL_PASS = 'tfzgdvakzqtpbhhe'

def run(user_info_file, download_pdfs=False):
    # user_info key: email, value: name and subjects
    user_info = {}
    subject_set = set()
    with open(user_info_file,'r') as fread:
        for line in fread.readlines():
            info_array = line.split(',')
            name = info_array[0]
            subjects = info_array[1].split('\t')
            print subjects
            for subject in subjects:
                subject_set.add(subject)
            email = info_array[2]
            user_info[email] = name+','+info_array[1]
    # scrapy the subject in subject_set
    logger.info('subject_set {0}'.format(subject_set))
    for subject in subject_set:
        start_time = time.time()
        logger.info('subject: {0}'.format(subject))
        run_all(area=subject, download_pdfs=download_pdfs)
        logger.info('Download {0} successful, and it takes {1} seconds'.format(subject, time.time()-start_time))
    # change the user_info to be the key of subject and the value include the emails and its nicknames
    if not download_pdfs:
        subject_users_dict = {}
        for key, value in user_info.items():
            email = key
            name = value.split(',')[0]
            subject_list = value.split(',')[1].split('\t')
            for subject in subject_list:
                if not subject_users_dict.has_key(subject):
                    temp_list = [email+','+name]
                    subject_users_dict[subject] = temp_list
                else:
                    temp_list = subject_users_dict[subject]
                    temp_list.append(email+','+name)
                    subject_users_dict[subject] = temp_list
        
        # send the emails
        for key, value_list in subject_users_dict.items():
            subject = key
            email_list = []
            for value in value_list:
                email_list.append(value.strip('\n').split(',')[0])
            email_list = ['dss_1990@sina.com','burness1990@gmail.com']
            date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            area_week_file = './papers/pdfs/{0}/{1}/summary.csv'.format(subject.replace('.','_'), date)
            logger.info('area_week_file: {0}, email_list: {1}'.format(area_week_file, email_list))
            send_email = SendEmail(mail_host=MAIL_HOST, mail_user=MAIL_USER, mail_pass=MAIL_PASS, area_week_file=area_week_file)
            send_email.set_sender(sender_email=MAIL_USER)
            send_email.set_receivers(receivers_email=email_list)
            send_email.send()

if __name__ == '__main__':
    run(USER_INFO_FILE, download_pdfs=False)



