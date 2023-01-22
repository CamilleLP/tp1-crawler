# tp1-crawler

## Description
This project implements a crawler. With a starting point URL (*https://ensai.fr/*), the crawler retrieves new URL using sitemap files and tags in crawled pages. When an URL is found, the crawler adds it only and only if the URL is not listed and has not been visited (robots.txt file has not been explored). At the end, the number of URL returned is specified by the user. All url are listed in <br> *crawled_webpages.txt* <br/> These URLs had been crawled exactely once

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
```shell
python3 main.py
```

## Launch tests
```shell
python3 -m unittest test_crawler.py
```