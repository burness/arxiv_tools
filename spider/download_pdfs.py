#-*-coding:utf-8-*-
import requests
import sys
import urllib2
from lxml import html
import Queue
from threading import Thread
import time
import os
import logging
import codecs

# logger = logging.getLogger()
logger = logging.getLogger('arxiv_tools')
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s' )
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)

class ArxivPdfs():
    def __init__(self, url):
        self.url = url

    def get_links(self) :
        try :
            result = requests.get(self.url)
        except :
            sys.exit(0)
        
        content = html.fromstring(result.content)
        print 'read web successfully'
        pdf_ids = content.xpath('//span[@class="list-identifier"]//a[@title="Abstract"]/text()')
        pdf_links = ['https://arxiv.org'+i+'.pdf' for i in content.xpath('//span[@class="list-identifier"]//a[@title="Download PDF"]/@href')]
        pdf_describe_links = [link.replace('pdf', 'abs', 1) for link in pdf_links]
        pdf_titles = [i.strip().replace('$','') for i in filter(lambda x : x!='\n', content.xpath('//div[@class="list-title mathjax"]/text()'))]
        pdf_authors = content.xpath('//div[@class="list-authors"]')
        pdf_authors_links = [','.join(pdf_author.xpath('a/@href')) for pdf_author in pdf_authors]
        pdf_authors_links = [','.join(['https://arxiv.org'+j for j in i.split(',')]) for i in pdf_authors_links]
        pdf_authors = [pdf_author.xpath('string(.)') for pdf_author in pdf_authors]
        pdf_authors = [author.replace('\n','') for author in pdf_authors]
        pdf_authors = [author.replace('Authors: ','') for author in pdf_authors]
        pdf_authors = [author.replace(',','') for author in pdf_authors]
        pdf_subjects = content.xpath('//span[@class="primary-subject"]/text()')
        return pdf_ids, pdf_describe_links, pdf_titles, pdf_links, pdf_authors, pdf_authors_links, pdf_subjects
        
def download_pdf(url, area, pdf_dir='./papers/pdfs/'):
    area = area.replace('.','_')
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    pdf_dir = os.path.join(pdf_dir, area+'/'+date)
    
    filename = os.path.join(pdf_dir,url.split('/')[-1])
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        with open(filename, "wb") as code:
            code.write(data)
        logger.info("Download {0} completed...".format(filename))
    except:
        logger.info("Download {1} error".format(filename))


class DownloadWorker(Thread):
    def __init__(self, queue, area):
        Thread.__init__(self)
        self.queue = queue
        self.area = area

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url = self.queue.get()
            if url is None:
                break
            # download_link(directory, link)
            download_pdf(url, self.area)
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
    summary_file = os.path.join('./papers/pdfs/',area+'/'+date+'/'+'summary.csv')

    with codecs.open(summary_file, 'w', encoding='utf-8') as fw:
        for index in xrange(pdf_num):
            print pdf_info['pdf_ids'][index], pdf_info['pdf_titles'][index], pdf_info['pdf_links'][index]
            print pdf_info['pdf_authors_links'][index]
            print pdf_info['pdf_subjects'][index]
            print pdf_info['pdf_describe_links'][index]
            # coding format here
            line = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(pdf_info['pdf_ids'][index], pdf_info['pdf_titles'][index], pdf_info['pdf_links'][index], 
                    pdf_info['pdf_authors'][index].encode('utf-8'), pdf_info['pdf_authors_links'][index], pdf_info['pdf_subjects'][index], pdf_info['pdf_describe_links'][index])
            logger.info(line)
            fw.write(line.decode('utf-8'))
    logger.info('Write to {0} successful'.format(summary_file))

def run_all(area, show_num=2, max_size=100, parallel_num=8, download_pdfs=False, pdf_dir='./papers/pdfs/'):
    
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    pdf_dir = os.path.join(pdf_dir, area+'/'+date)
    if not os.path.exists(pdf_dir.lower()):
        try:
            os.makedirs(pdf_dir)
        except:
            logger.info('Other thread Create')
    url = build_url(area, show_num)
    area = area.replace('.','_')
    logger.info('url: {0}'.format(url))
    arxiv_pdfs = ArxivPdfs(url)
    if download_pdfs:
        download_queue = Queue.Queue(maxsize=max_size)
        for x in range(parallel_num):
            worker = DownloadWorker(download_queue, area)
            worker.daemon = True
            worker.start()
    pdf_ids, pdf_describe_links, pdf_titles, pdf_links, pdf_authors, pdf_authors_links, pdf_subjects = arxiv_pdfs.get_links()
    if download_pdfs:
        for link in pdf_links:
            download_queue.put(link)
            download_queue.join()
    # print pdf_titles
    pdf_info = {}
    pdf_info['pdf_num'] = len(pdf_ids)
    pdf_info['pdf_ids'] = pdf_ids
    pdf_info['pdf_describe_links'] = pdf_describe_links
    pdf_info['pdf_titles'] = pdf_titles
    pdf_info['pdf_links'] = pdf_links
    pdf_info['pdf_authors'] = pdf_authors
    pdf_info['pdf_authors_links'] = pdf_authors_links
    pdf_info['pdf_subjects'] = pdf_subjects
    logger.info('extract pdfs links done, begin to download {0} pdfs '.format(len(pdf_links)))
    logger.info('subject: {0}'.format(area))
    pdf_info_write(area, **pdf_info)
    # download the all pdfs


if __name__  == '__main__':
    start = time.time()
    run_all('cs.cv', show_num=8, max_size=1)
    logger.info("took time : {0}".format(time.time() - start))
    # arXiv:1703.00856	Araguaia Medical Vision Lab at ISIC 2017 Skin Lesion Classification  Challenge	https://arxiv.org/pdf/1703.00856.pdf	Rafael Teixeira Sousa, Larissa Vasconcellos de Moraes	https://arxiv.org/find/cs/1/au:+Sousa_R/0/1/0/all/0/1,https://arxiv.org/find/cs/1/au:+Moraes_L/0/1/0/all/0/1	Computer Vision and Pattern Recognition (cs.CV)	https://arxiv.org/abs/1703.00856.pdf

    # test the pdf_info_write
    # pdf_num = 7
    # pdf_ids = ['arXiv:1703.00856']
    # pdf_titles = ['Araguaia Medical Vision Lab at ISIC 2017 Skin Lesion Classification  Challenge']
    # pdf_links = ['https://arxiv.org/pdf/1703.00856.pdf']
    # pdf_authors = ['Rafael Teixeira Sousa, Larissa Vasconcellos de Moraes']
    # pdf_authors_links = ['https://arxiv.org/find/cs/1/au:+Sousa_R/0/1/0/all/0/1,https://arxiv.org/find/cs/1/au:+Moraes_L/0/1/0/all/0/1']
    # pdf_subjects = ['Computer Vision and Pattern Recognition (cs.CV)']
    # pdf_describe_links = ['https://arxiv.org/abs/1703.00856.pdf']
    # pdf_info = {}
    # pdf_info['pdf_num'] = len(pdf_ids)
    # pdf_info['pdf_ids'] = pdf_ids
    # pdf_info['pdf_titles'] = pdf_titles
    # pdf_info['pdf_describe_links'] = pdf_describe_links
    # pdf_info['pdf_links'] = pdf_links
    # pdf_info['pdf_authors'] = pdf_authors
    # pdf_info['pdf_authors_links'] = pdf_authors_links
    # pdf_info['pdf_subjects'] = pdf_subjects
    # pdf_info_write('cs.cv',date='2017-03-05', **pdf_info)
