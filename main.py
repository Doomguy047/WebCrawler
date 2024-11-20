import threading
from queue import Queue
from crawler import Crawler
from domain import *
from general import *

print("Enter Project Name here:")
PROJECT_NAME = input()
print("Enter Homepage url here:")
HOMEPAGE = input()
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
print("Enter number of threads here:")
NUMBER_OF_THREADS = input()
queue = Queue()
Crawler(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


def create_crawlers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_crawlers()
crawl()
