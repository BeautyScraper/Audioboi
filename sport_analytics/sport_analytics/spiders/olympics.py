from functools import reduce
import re
import requests
import scrapy
import subprocess
from sport_analytics.utils.file_downloader import download_file
from sport_analytics.utils.decrypt_m3u8 import download_decrypt
from pathlib import Path
from Crypto.Cipher import AES

class OlympicsSpider(scrapy.Spider):
    name = 'olympics'
    # allowed_domains = ['olympics.com']
    start_urls = ['https://olympics.com/en/olympic-games/sochi-2014/videos']

    def parse(self,response):
        urls = response.css('a[href*=video]::attr(href)').getall()
        # breakpoint()
        for url in urls:
            yield response.follow(url=url, callback=self.parse_page)

    def parse_video(self, response):
        # breakpoint()
        durl = response.text.strip('"') 
        meta = response.meta
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://olympics.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Referer": "https://olympics.com/",
            "Connection": "keep-alive"
        }
        yield scrapy.Request(durl, callback=self.parse_video_data,headers=self.headers,meta=meta)
    
    def parse_video_data(self, response):
        # breakpoint()
        # Path(r'c:\temp\1.m3u8').write_text(response.text)
        meta = response.meta
        durl = '/'.join(response.url.split('/')[:6])+'/' 
        url = durl + response.text.split()[-1]
        yield scrapy.Request(url, callback=self.lastone,headers=self.headers,meta=meta)
    
    def lastone(self, response):
        durl = '/'.join(response.url.split('/')[:7])+'/' 
        # filename = r'c:\temp\2.m3u8'
        # breakpoint()
        output_file_path = Path(r'c:\temp') / response.meta['filename']
        # Path(filename).write_text(response.text)
        seg_urls = [durl + x for x in response.text.split() if '.ts' in x] 
        key_file_url = [durl + x for x in response.text.split() if 'serve.key' in x] 
        key_url = re.search('URI="(.*)"', key_file_url[0])[1]
        for vurls in seg_urls:
            download_decrypt(vurls, key_url, None, output_file_path, self.headers)
        # decrypt_m3u8_func(filename, output_file_path)
        # req = requests.get(key_url,headers=self.headers)
        # req.payload = req.text.encode('utf-8')
        # breakpoint()
        # download_file(key_url, r'c:\temp\serve.key','wb', self.headers) # download the key file
        # download_file(seg_urls[0], 'hello.txt','wb',self.headers)

    
    def parse_page(self, response):
        template_url = 'https://olympics.com/tokenGenerator?url=@@&domain=https://vod.olympicchannel.com&_ts=1657182450820'
        vurl = response.css('meta[name="video_url"]::attr(content)').get()
        if vurl is None:
            breakpoint()
        vurl = template_url.replace("@@", vurl)
        meta = {}
        meta['filename'] = re.sub('[^\w\b\s\d]+','',response.css('title::text').get()) + '.mp4'
        yield scrapy.Request(vurl, callback=self.parse_video,meta = meta)

