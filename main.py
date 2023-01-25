from CRAWLER.crawler import Crawler
from export_url import export_url_to_txt

if __name__ == '__main__':
    crawler = Crawler(urls=['https://ensai.fr/'])
    crawler.run()
    print('urls to visit \n', crawler.urls_to_visit, len(crawler.urls_to_visit), '\n')
    print('visited urls \n', crawler.visited_urls, len(crawler.visited_urls), '\n')
    print('visited sitemap urls \n', crawler.visited_sitemaps_urls, len(crawler.visited_sitemaps_urls), '\n')
    print('crawled urls \n', crawler.crawled_urls, len(crawler.crawled_urls), '\n')

    print('number of failed downloads', crawler.failed_download, '\n')
    print('number of failed sitemaps', crawler.failed_sitemaps, '\n')
    print('number of failed crawl', crawler.failed_download, '\n')

    export_url_to_txt(crawler.crawled_urls, "crawled_webpages.txt")