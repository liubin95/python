# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options


class AliyunSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AliyunDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        options = Options()
        setting = get_project_settings()

        # 该属性不显示浏览器
        # options.add_argument('-headless')

        # selenium.webdriver.chrome需要手动下载
        driver = webdriver.WebDriver(chrome_options=options)
        driver.maximize_window()
        # 隐性等待，最长等10秒
        driver.implicitly_wait(10)
        driver.get(request.url)
        # 操作对象
        actions = ActionChains(driver)
        # 用户名
        input = driver.find_elements_by_xpath('//*[@id="user_principal_name"]')[0]
        actions.click(input).perform()
        input.send_keys(setting.get('USER_NAME'))
        # 点击下一步
        next_btn = driver.find_elements_by_xpath('//*[@id="J_FormNext"]/span')[0]
        actions.click(next_btn).perform()
        # 密码
        pass_word = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/form/div[4]/div[1]/p/input')[0]
        driver.execute_script("arguments[0].focus();", pass_word)
        pass_word.send_keys(setting.get('PASS_WORD'))
        # 登录按钮 //*[@id="u22"]/input
        login_btn = driver.find_elements_by_xpath('//*[@id="u22"]/input')[0]
        driver.execute_script("arguments[0].click();", login_btn)

        # 头像
        login_avatar = driver.find_elements_by_xpath('//*[@id="J_console_base_top_nav"]/div[2]/div[9]/button/img')[0]
        # 鼠标悬浮头像
        ActionChains(driver).move_to_element(login_avatar).perform()
        # 登录名
        login_name = driver.find_elements_by_xpath(
            '//*[@id="J_console_base_top_nav"]/div[2]/div[9]/div/header/header/div/div/div')[0]
        spider.logger.info('login_name:%s', login_name.text)
        html = driver.page_source

        driver.quit()
        # self.driver = driver

        # 构建response, 将它发送给spider引擎
        return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
