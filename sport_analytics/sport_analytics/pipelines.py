# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import subprocess
import re

class SportAnalyticsPipeline:
    def process_item(self, item, spider):
        # breakpoint()

        filename =  re.sub('[^\w\b\s\d]+','',item['name']) + '.mp4'
        # breakpoint()
        # subprocess.call(['downloadm3u8','-o',filename,item['video_url']])
        # subprocess.call(['aria2c', '--dir', r'C:\temp4', '-o', filename, item['video_url']])
        return item
