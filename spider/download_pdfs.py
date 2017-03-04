import requests
import sys
# import re
import urllib2
from lxml import html
import Queue
from threading import Thread
from time import time
import os
import logging

logger = logging.getLogger()

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
        # pdf_links = content.xpath('//span[@class="list-identifier"]//a[@title="Download PDF"]/@href')
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
        print pdf_ids[:2], len(pdf_ids)
        print pdf_links[:2], len(pdf_links)
        print pdf_authors[:2], len(pdf_authors)
        print pdf_authors_links[:2], len(pdf_authors_links)
        print pdf_subjects[:2], len(pdf_subjects)
        print pdf_titles[:2], len(pdf_titles)
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

if __name__  == '__main__':
    a = ArxivPdfs('https://arxiv.org/list/cs.CV/pastweek?skip=0&show=8')
    start = time()
    download_queue = Queue.Queue(maxsize=1)
    for x in range(8):
        worker = DownloadWorker(download_queue)
        worker.daemon = True
        worker.start()
    
    pdf_ids, pdf_titles, pdf_links, pdf_authors, pdf_authors_links, pdf_subjects = a.get_links()
    logger.info('extract pdfs links done, begin to download {0} pdfs '.format(len(pdf_links)))

    for link in pdf_links:
        download_queue.put(link)
    download_queue.join()
    logger.info("the images num is {0}".format(len(pdf_links)))
    logger.info("took time : {0}".format(time() - start))