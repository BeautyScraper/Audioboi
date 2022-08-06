from ast import parse
import scrapy
from ..items import SportAnalyticsItem
import subprocess 

class WweSpiderSpider(scrapy.Spider):
    name = 'wwe_spider'
    allowed_domains = ['wwe.com']
    # start_urls = ['https://www.wwe.com/videos/brock-lesnar-paul-heymans-best-moments-wwe-top-10-jan-9-2022']
    def start_requests(self):
        with open('wwe.opml','r') as fp:
            start_urls = fp.readlines()

        # start_urls = ['https://www.wwe.com/videos/']
        for url in start_urls:
            yield scrapy.Request(url=url.strip(), callback=self.parse_video)

    def start_page(self, response):
        video_page_urls = response.css('a[href*=video]::attr(href)').getall()
        for urls in video_page_urls:
            # breakpoint()
            yield response.follow(url=urls,callback=self.parse_video)



    def parse_video(self, response):
        item = SportAnalyticsItem()
        try:
            ur = response.css('script::text').re('"file"\b*:\b*\"[^"]*')[0] 
        except:

            yield response.follow(url=response.url,callback=self.start_page,dont_filter=True)
            return

        url = ur.split(':')[1].strip('"')
        # breakpoint()
        video_url = 'https:' + url.replace('\\/','/')
        item['name'] = response.css('title::text').get()
        # video_url = response.css('meta[name=\"twitter\:player\:stream\"]::attr(content)').get()
        item['video_url'] = video_url
        item['source_website'] = response.url.split('/')[2]
        # subprocess.call(['aria2c', '--dir', r'C:\temp4', '-o', 'Brock10.mp4', video_url])
        # breakpoint()
        yield item
