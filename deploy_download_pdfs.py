from spider.download_pdfs import run_all
import time
import logging
from deploy_email import run, USER_INFO_FILE



if __name__ == '__main__':
    run(USER_INFO_FILE, download_pdfs=True)



