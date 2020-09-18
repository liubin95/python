# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AliyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 实例名字
    instance_name = scrapy.Field()
    # 主机名
    host_name = scrapy.Field()
    # 操作系统
    os_name = scrapy.Field()
    # 状态
    instance_status = scrapy.Field()
    # 地址
    instance_address = scrapy.Field()
    # ip
    instance_ip = scrapy.Field()
    # cpu使用
    cpu_used = scrapy.Field()
    # 内存使用
    memory_used = scrapy.Field()
    # 磁盘使用（集合）
    disk_list = scrapy.Field()
    pass
