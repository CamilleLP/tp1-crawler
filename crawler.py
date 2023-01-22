import logging
import requests
import time
from urllib.parse import urljoin
import urllib.robotparser
from urllib.parse import urlparse
from usp.tree import sitemap_tree_for_homepage
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_sitemaps_urls = []
        self.visited_urls = []
        self.crawled_urls = []
        self.urls_to_visit = urls
        self.failed_download = 0
        self.failed_sitemaps = 0
        self.failed_crawled = 0

    def download_url(self, url):
        '''
        download_url: downloads a webpage (specified with url argument)
        return an error if the download has failed
        '''
        try:
            get_url = requests.get(url).text
            return get_url
        except Exception:
            self.failed_download += 1
            logging.exception(f'Failed to get: {url}')

    def get_linked_urls(self, url, html):
        '''
        get_linked_urls extracts urls from the webpage given by url
        html: html content where urls need to be extracted
        '''
        soup = BeautifulSoup(html, 'html.parser')
        path_list = []
        for link in soup.find_all('a'): # extracts all urls with <a> tags
            path = link.get('href')
            if path and path.startswith('http'):
                path = urljoin(url, path)
                path_list.append(path)
        return path_list

    def add_url_to_visit(self, url):
        '''
        add_url_to_visit: add url to visit if it is not already visited or
        listed in self.urls_to_visit
        '''
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def find_domain(self, url):
        '''
        find_domain: extract the domain part of an url to get the homepage url
        '''
        scheme = urlparse(url).scheme # http or https
        domain = urlparse(url).netloc # domain name
        url_domain = scheme + '://' + domain + '/'
        return url_domain
    
    def extract_urls_sitemap(self, url):
        '''
        extract_urls_sitemap: extract all urls of an url webpage using the sitemap files
        '''
        url_domain = self.find_domain(url)
        if url_domain not in self.visited_sitemaps_urls:
            tree = sitemap_tree_for_homepage(url_domain)
            for page in tree.all_pages():
                self.add_url_to_visit(page.url)
            self.visited_sitemaps_urls.append(url_domain)

    def info_crawl(self, url):
        '''
        info_crawl: gives information about a webpage (possibility to crawl 
        and minimum delay to respect between each crawl)
        '''
        url_domain = self.find_domain(url)
        url_robots = url_domain + 'robots.txt'
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url_robots)
        rp.read()

        infos = {}
        infos['is_crawlable'] = rp.can_fetch("*", url)
        infos['min_delay'] = rp.crawl_delay("*")
        return infos

    def crawl(self, url, min_delay = 5):
        '''
        crawl: crawl a webpage and respect a minimum delay between each crawl
        '''
        is_crawled = False
        infos = self.info_crawl(url)
        
        # check that it is allowed to crawl before crawling:
        if infos['is_crawlable']:
            
            # compute minimum delay to respect politeness
            if infos['min_delay'] and infos['min_delay'] > min_delay:
                min_delay = infos['min_delay']

            # politeness (waiting time here)
            logging.info(f'Waiting {min_delay} seconds...')
            time.sleep(min_delay)
            
            # crawling after waiting enough time
            logging.info(f'Crawling: {url}')
            html = self.download_url(url)
            for url in self.get_linked_urls(url, html):
                self.add_url_to_visit(url)

            # confirm that url has been crawled
            is_crawled = True
        return is_crawled

    def run(self, nb_max_urls = 50):
        '''
        run: gives urls obtained by crawling urls (starting points are given in self.urls_to_visit)
        '''
        while len(self.crawled_urls) < nb_max_urls and self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            # use sitemap.xml to find new urls
            try:
                self.extract_urls_sitemap(url)
            except Exception:
                logging.exception(f'Failed to extract url from sitemap: {url}')
                self.failed_sitemaps += 1
            
            # crawl url to find new urls
            try:
                is_crawled = self.crawl(url)
                if is_crawled:
                    self.crawled_urls.append(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
                self.failed_crawled += 1
            finally:
                self.visited_urls.append(url)