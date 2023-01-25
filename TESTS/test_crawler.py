from unittest import TestCase
from CRAWLER.crawler import Crawler
import validators

class TestCrawler(TestCase):
    def test_download_url_valid(self):
        '''
        check for a valid url that download_url function work
        '''
        # GIVEN
        valid_url = 'https://ensai.fr/'
        # WHEN
        crawler = Crawler()
        res_valid_url = crawler.download_url(valid_url)
        # THEN
        self.assertIsNotNone(res_valid_url)
        self.assertIn('<!DOCTYPE html>', res_valid_url)
        self.assertIn('</html>', res_valid_url)
    
    def test_download_url_non_valid(self):
        '''
        check for a non-valid url that download_url function returns an error
        '''
        # GIVEN
        nonvalid_url = 'https://ensaiiii.fr/'
        # WHEN
        crawler = Crawler()
        res_non_valid_url = crawler.download_url(nonvalid_url)
        # THEN
        self.assertEqual(crawler.failed_download, 1)

    def test_get_linked_urls_links(self):
        '''
        check that get_linked_urls extracts properly url from a html file
        when there is a link in the page
        '''
        # GIVEN
        links_url = 'https://exemple.com/'
        html = """<!DOCTYPE html>
        <html>   
        <head>
            <title>Hyperlink Example</title>
        </head>
            
        <body>
            <a href = "https://exemple.com/test.html" </a>
        </body>	
        </html>"""
        # WHEN
        crawler = Crawler()
        links = crawler.get_linked_urls(links_url, html)
        # THEN
        self.assertEqual(links, ['https://exemple.com/test.html'])

    def test_get_linked_urls_nolinks(self):
        '''
        check that get_linked_urls extracts properly url from a html file
        when there is no link in the page
        '''
        # GIVEN
        links_url = 'https://exemple.com/'
        html = """<!DOCTYPE html>
        <html>   
        <head>
            <title>Hyperlink Example</title>
        </head>
            
        <body>
        </body>	
        </html>"""
        # WHEN
        crawler = Crawler()
        links = crawler.get_linked_urls(links_url, html)
        # THEN
        self.assertEqual(len(links), 0)

    def test_add_url_to_visit_add(self):
        '''
        check that add_url_to_visit adds url to visit (only when it is necessary)
        '''
        # GIVEN
        visited_urls = []
        urls_to_visit = []
        url = 'https://monurl.com'
        # WHEN
        crawler = Crawler()
        crawler.visited_urls = visited_urls
        crawler.urls_to_visit = urls_to_visit
        crawler.add_url_to_visit(url)
        # THEN
        self.assertEqual(crawler.urls_to_visit, [url])

    def test_add_url_to_visit_not_add(self):
        '''
        check that add_url_to_visit adds url to visit (only when it is necessary)
        '''
        # GIVEN
        visited_urls = ['https://monurl.com']
        urls_to_visit = []
        url = 'https://monurl.com'
        # WHEN
        crawler = Crawler()
        crawler.visited_urls = visited_urls
        crawler.urls_to_visit = urls_to_visit
        crawler.add_url_to_visit(url)
        # THEN
        self.assertEqual(crawler.urls_to_visit, [])

    def test_find_domain(self):
        '''
        check that add_url_to_visit adds url to visit (only when it is necessary)
        '''
        # GIVEN
        url = 'https://monurl.com/test/test2'
        # WHEN
        crawler = Crawler()
        url_domain = crawler.find_domain(url)
        # THEN
        self.assertEqual(url_domain, 'https://monurl.com/')

    def test_extract_urls_sitemap(self):
        '''
        check that extract_urls_sitemap results are correct urls
        '''
        # GIVEN
        url = 'https://ensai.fr/'
        # WHEN
        crawler = Crawler()
        crawler.extract_urls_sitemap(url)
        print(crawler.urls_to_visit)
        # THEN
        self.assertGreater(len(crawler.urls_to_visit), 0)
        for url in crawler.urls_to_visit:
            self.assertTrue(validators.url(url))

    def test_info_crawl1(self):
        '''
        check that information given by info_crawl are correct
        '''
        # GIVEN
        # according to robots.txt, possible to crawl but must wait 10 seconds between each crawl
        url = 'https://www.banque-france.fr/'
        # WHEN
        crawler = Crawler()
        infos = crawler.info_crawl(url)
        # THEN
        self.assertTrue(infos['is_crawlable'])
        self.assertEqual(infos['min_delay'], 10)

    def test_info_crawl2(self):
        '''
        check that information given by info_crawl are correct
        '''
        # GIVEN
        # according to robots.txt, possible to crawl, no delay required bewteen each crawl
        url = 'https://ensai.fr/'
        # WHEN
        crawler = Crawler()
        infos = crawler.info_crawl(url)
        # THEN
        self.assertTrue(infos['is_crawlable'])
        self.assertIsNone(infos['min_delay'])


    def test_info_crawl3(self):
        '''
        check that information given by info_crawl are correct
        '''
        # GIVEN
        # crawl not allowed
        url = 'https://www.facebook.com/'
        # WHEN
        crawler = Crawler()
        infos = crawler.info_crawl(url)
        # THEN
        self.assertFalse(infos['is_crawlable'])

    def test_crawl1(self):
        '''
        check that crawler work properly
        '''
        # GIVEN
        url = 'https://ensai.fr/'
        # WHEN
        crawler = Crawler()
        is_crawled = crawler.crawl(url)
        # THEN
        self.assertTrue(is_crawled)
        self.assertGreater(len(crawler.urls_to_visit),0)

    def test_crawl2(self):
        '''
        check that crawler work properly
        '''
        # GIVEN
        url = 'https://www.facebook.com/'
        # WHEN
        crawler = Crawler()
        is_crawled = crawler.crawl(url)
        # THEN
        self.assertFalse(is_crawled)

    def test_run(self):
        '''
        check that run crawls exactely nb_max_urls urls
        '''
        # GIVEN
        url = 'https://ensai.fr/'
        nb_max_urls = 10
        # WHEN
        crawler = Crawler()
        crawler.run(nb_max_urls)
        # THEN
        self.assertEqual(len(crawler.crawled_urls), nb_max_urls)

