# tp1-crawler

## Description
This project implements a crawler. With a starting point URL (*https://ensai.fr/*), the crawler retrieves new URLs using sitemap files and tags in crawled pages. When an URL is found, the crawler adds it only and only if the URL has not been added to the final results and has not been visited (robots.txt file has not been explored). The user can specify the number of URLs to return in ***crawled_webpages.txt***. All the URLs returned in this file have been crawled exactely once.

The code used for the crawler has been inspired by: *https://www.scrapingbee.com/blog/crawling-python/*

## Contributors
Camille Le Potier

## Requirements
Python 3.8

## Installation
```shell
git clone https://github.com/CamilleLP/tp1-crawler.git
cd tp1-crawler
pip3 install -r requirements.txt
```

## Launch the crawler
The user must give a first url (example: *https://ensai.fr/*) and a maximum number of URLs to crawl (50 in the example below):

```shell
python3 main.py https://ensai.fr/ 50
```

To get more information about arguments:
```shell
python3 main.py -h
```

## Launch the tests
```shell
python3 -m unittest TESTS/test_crawler.py
```