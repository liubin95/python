# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector

from items import AliyunItem


class CloudmonitorSpider(scrapy.Spider):
    name = 'cloudmonitor'
    allowed_domains = ['aliyun.com']
    start_urls = [
        'https://cloudmonitor.console.aliyun.com/#/hostmonitor/host',
        'https://signin.aliyun.com/login.htm?callback=https%3A%2F%2Fcloudmonitor.console.aliyun.com%2F%23%2Fhostmonitor%2Fhost'
    ]
    headers = {
        'referer': 'https://cloudmonitor.console.aliyun.com/'
    }
    driver = None

    def start_requests(self):
        """
        可以重写 Spider 类的 start_requests 方法
        """
        yield scrapy.Request(url=self.start_urls[1], callback=self.parse)

    def parse(self, response):
        """
        默认的解析方法
        :param response: 响应对象
        """
        # 创建选择器
        selector = Selector(response)
        # 选择表格
        tables = selector.xpath('//tr')
        # 删除表头
        del (tables[0])
        # 删除表格脚
        del (tables[-1])

        for each in tables:
            self.logger.info(each)
            # 实例化一个Item对象
            item = AliyunItem()

            # 解析行中的单元格
            item['instance_name'] = each.xpath('td')[1].xpath('a')[0].xpath('text()')[0].extract()
            item['host_name'] = each.xpath('td')[1].xpath('div')[0].xpath('text()')[0].extract()
            item['os_name'] = each.xpath('td')[2].xpath('div')[0].xpath('@aliyun-popover2')[0].extract()
            item['instance_status'] = each.xpath('td')[3].xpath('div/div/span/span')[0].xpath('text()')[0].extract()
            item['instance_address'] = each.xpath('td')[5].xpath('text()')[0].extract()
            ip_list = each.xpath('td')[6].xpath('div').xpath('text()').extract()
            item['instance_ip'] = ','.join(ip_list)
            item['cpu_used'] = each.xpath('td')[7].xpath('div')[0].xpath('div')[0].xpath('text()')[0].extract()
            item['memory_used'] = each.xpath('td')[7].xpath('div')[1].xpath('div')[0].xpath('text()')[0].extract()
            item['disk_list'] = each.xpath('td')[8].xpath('div')[0].xpath('div/span[@aliyun-popover2]').xpath(
                'text()').extract()

            # 返回数据
            yield item

        # 是否有下一页
        # /html/body/div[3]/div/div/div[3]/div[2]/div/div/div/div[3]/table[2]/tfoot/tr/td[2]/div[2]/div/ul/li[4]/a
