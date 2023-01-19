import logging
import requests
import time
from urllib.parse import urljoin
import urllib.robotparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.crawled_urls = []
        self.urls_to_visit = urls

    # work
    def download_url(self, url):
        return requests.get(url).text

    # work
    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        path_list = []
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('http'):
                path = urljoin(url, path)
                path_list.append(path)
        return path_list

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def info_crawl(self, url):
        scheme = urlparse(url).scheme
        domain = urlparse(url).netloc
        url_robots = scheme + '://' + domain + '/robots.txt'
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url_robots)
        rp.read()

        infos = {}
        infos['is_crawlable'] = rp.can_fetch("*", url)
        infos['min_delay'] = rp.crawl_delay("*")
        return infos

    def crawl(self, url, min_delay = 1):
        is_crawled = False
        infos = self.info_crawl(url)
        if infos['is_crawlable']:
            if infos['min_delay'] and infos['min_delay'] > min_delay:
                min_delay = infos['min_delay']

            # waiting time here
            logging.info(f'Waiting {min_delay} seconds...')
            time.sleep(min_delay)
            
            logging.info(f'Crawling: {url}')
            html = self.download_url(url)
            for url in self.get_linked_urls(url, html):
                self.add_url_to_visit(url)
            is_crawled = True
        return is_crawled

    def run(self, nb_max_urls = 10):
        while len(self.crawled_urls) < nb_max_urls and self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            try:
                is_crawled = self.crawl(url)
                if is_crawled:
                    self.crawled_urls.append(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    crawler = Crawler(urls=['https://ensai.fr/'])
    crawler.run()
    print(crawler.urls_to_visit, '\n')
    print(crawler.visited_urls, '\n')
    print(crawler.crawled_urls, '\n')


# my_crawler = Crawler(urls=['https://ensai.fr/'])
# html = my_crawler.download_url('https://ensai.fr/')
# urls = my_crawler.get_linked_urls('https://ensai.fr/', html)
# my_crawler.crawl('https://ensai.fr/')
# print(my_crawler.urls_to_visit)
# print(len(my_crawler.urls_to_visit))
# print(my_crawler.info_crawl('https://twitter.com/search/realtime'))
