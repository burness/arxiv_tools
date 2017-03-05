import requests
import sys
# import re
import urllib2
from lxml import html
import Queue
from threading import Thread
import time
import os
import logging

# logger = logging.getLogger()
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class ArxivPdfs():
    def __init__(self, url):
        self.url = url
        pass

    def get_links(self) :
        try :
            result = requests.get(self.url)
        except :
            sys.exit(0)
        
        content = html.fromstring(result.content)
        print 'read web successfully'
        pdf_ids = content.xpath('//span[@class="list-identifier"]//a[@title="Abstract"]/text()')
        pdf_links = ['https://arxiv.org'+i+'.pdf' for i in content.xpath('//span[@class="list-identifier"]//a[@title="Download PDF"]/@href')]
        pdf_titles = [i.strip() for i in filter(lambda x : x!='\n', content.xpath('//div[@class="list-title mathjax"]/text()'))]
        pdf_authors = content.xpath('//div[@class="list-authors"]')
        pdf_authors_links = [','.join(pdf_author.xpath('a/@href')) for pdf_author in pdf_authors]
        pdf_authors_links = [','.join(['https://arxiv.org'+j for j in i.split(',')]) for i in pdf_authors_links]
        pdf_authors = [pdf_author.xpath('string(.)') for pdf_author in pdf_authors]
        pdf_authors = [author.replace('\n','') for author in pdf_authors]
        pdf_authors = [author.replace('Authors: ','') for author in pdf_authors]
        pdf_subjects = content.xpath('//span[@class="primary-subject"]/text()')
        return pdf_ids, pdf_titles, pdf_links, pdf_authors, pdf_authors_links, pdf_subjects
        
def download_pdf(url, pdf_dir='./pdfs/'):
    filename = os.path.join(pdf_dir,url.split('/')[-1])
    f = urllib2.urlopen(url)
    data = f.read()
    with open(filename, "wb") as code:
        code.write(data)
    print "Download completed..."


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url = self.queue.get()
            if url is None:
                break
            # download_link(directory, link)
            download_pdf(url)
            self.queue.task_done()

def build_url(area, show_num=1000):
    '''
    build the url of the specified area
    args:
        area: the area
        show_num: the show num, default 1000
    return:
        url: the url of the specified area and show num
    '''
    url = 'https://arxiv.org/list/{0}/pastweek?skip=0&show={1}'.format(area, show_num)
    return url


def pdf_info_write(area,date=None, **pdf_info):
    pdf_num = pdf_info['pdf_num']
    area = area.replace('.','_')
    if not date:
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    summary_file = os.path.join('../papers/pdfs/',area+'/'+date+'/'+'summary.csv')

    with open(summary_file, 'w') as fw:
        for index in xrange(pdf_num):
            line = '{0},{1},{2},{3},{4},{5}'.format(pdf_info['pdf_ids'][index], pdf_info['pdf_titles'][index], pdf_info['pdf_links'][index], 
                    pdf_info['pdf_authors'][index],pdf_info['pdf_authors_links'][index],pdf_info['pdf_subjects'][index])
            fw.write(line+'\n')


def run_all(area, show_num=1000, max_size=100, parallel_num=8):
    url = build_url(area, show_num)
    arxiv_pdfs = ArxivPdfs(url)
    download_queue = Queue.Queue(maxsize=max_size)
    for x in range(parallel_num):
        worker = DownloadWorker(download_queue)
        worker.daemon = True
        worker.start()
    pdf_ids, pdf_titles, pdf_links, pdf_authors, pdf_authors_links, pdf_subjects = arxiv_pdfs.get_links()
    pdf_info = {}
    pdf_info['pdf_num'] = len(pdf_ids)
    pdf_info['pdf_ids'] = pdf_ids
    pdf_info['pdf_titles'] = pdf_titles
    pdf_info['pdf_links'] = pdf_links
    pdf_info['pdf_authors'] = pdf_authors
    pdf_info['pdf_authors_links'] = pdf_authors_links
    pdf_info['pdf_subjects'] = pdf_subjects
    pdf_info_write(area, **pdf_info)
    logger.info('extract pdfs links done, begin to download {0} pdfs '.format(len(pdf_links)))

    for link in pdf_links:
        download_queue.put(link)
    download_queue.join()

if __name__  == '__main__':
    # start = time.time()
    # run_all('cs.cv', show_num=8, max_size=1)
    # logger.info("took time : {0}".format(time.time() - start))
    # test the pdf_info_write
    pdf_num = 7
    pdf_ids = ['1', '2', '3','4']
    pdf_titles = ['1', '2', '3','4']
    pdf_links = ['1', '2', '3','4']
    pdf_authors = ['1', '2', '3','4']
    pdf_authors_links = ['1', '2', '3','4']
    pdf_subjects = ['1', '2', '3','4']
    pdf_info = {}
    pdf_info['pdf_num'] = len(pdf_ids)
    pdf_info['pdf_ids'] = pdf_ids
    pdf_info['pdf_titles'] = pdf_titles
    pdf_info['pdf_links'] = pdf_links
    pdf_info['pdf_authors'] = pdf_authors
    pdf_info['pdf_authors_links'] = pdf_authors_links
    pdf_info['pdf_subjects'] = pdf_subjects
    pdf_info_write('cs.cv',date='2017-03-03', **pdf_info)
