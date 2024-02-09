from CRAWLER.crawler import Crawler
from CRAWLER.export_url import export_url_to_txt
import argparse

if __name__ == '__main__':
    # configure argument
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help = "first url to crawl")
    parser.add_argument("nb_url_to_crawl", help = "give the number of URLs to crawl")
    
    # extract argument given by user
    args = parser.parse_args()
    url = args.url
    nb = int(args.nb_url_to_crawl)
    
    # launch the crawler
    crawler = Crawler(urls=[url])
    crawler.run(nb_max_urls=nb)

    # print results and save crawled URLs in a txt file
    print('urls to visit \n', crawler.urls_to_visit, len(crawler.urls_to_visit), '\n')
    print('visited urls \n', crawler.visited_urls, len(crawler.visited_urls), '\n')
    print('visited sitemap urls \n', crawler.visited_sitemaps_urls, len(crawler.visited_sitemaps_urls), '\n')
    print('crawled urls \n', crawler.crawled_urls, len(crawler.crawled_urls), '\n')

    print("ADDITIONAL INFO CRAWLER: \n")
    print('nb of failed downloads', crawler.failed_download, '\n')
    print('number of failed sitemaps', crawler.failed_sitemaps, '\n')
    print('nb of failed crawl', crawler.failed_download, '\n')

    export_url_to_txt(crawler.crawled_urls, "crawled_webpages.txt")
    print("The " + str(nb) + " urls crawled have been saved in 'crawled_webpages.txt' file")