from functools import reduce
import re
import requests
import scrapy
import subprocess
from sport_analytics.utils.file_downloader import download_file
from sport_analytics.utils.decrypt_m3u8 import download_decrypt
from pathlib import Path

gallery_links_file = 'gallery_links.txt'
file_save_dir = ''

class AudiboiSpider(scrapy.Spider):
    name = 'audiboi'
    # allowed_domains = ['audiboi.com']
    # start_urls = ['http://audiboi.com/']
    def start_requests(self):
        #open the file and crawl the urls
        with open(gallery_links_file) as f:
            for url in f:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # breakpoint()
        file_url = response.css('[data-source]::attr(data-source)').get()
        file_name = response.css('[data-source]::attr(data-source)').get().split('/')[-1]
        file_full_path = Path(file_save_dir) / Path(file_name).stem / file_name
        
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
    "Accept-Language": "en-US,en;q=0.5",
    "Range": "bytes=425658-",
    "Connection": "keep-alive",
    "Referer": "https://audiboi.com/",
    "Sec-Fetch-Dest": "audio",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site"
                }

        download_file(file_url, file_full_path,'wb',headers)
        pass
