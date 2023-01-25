# tp1-crawler

## Description
This project implements a crawler. With a starting point URL (*https://ensai.fr/*), the crawler retrieves new URL using sitemap files and tags in crawled pages. When an URL is found, the crawler adds it only and only if the URL is not listed and has not been visited (robots.txt file has not been explored). At the end, the number of URL returned is specified by the user. All url are listed in ***crawled_webpages.txt***. These URLs had been crawled exactely once

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

## Launch tests
```shell
python3 -m unittest TESTS/test_crawler.py
```