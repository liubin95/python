# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class AliyunDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        """
        初始化中间件，打开浏览器登录
        """
        options = Options()
        setting = get_project_settings()

        # 该属性不显示浏览器
        # options.add_argument('-headless')

        # selenium.webdriver.chrome需要手动下载
        driver = webdriver.WebDriver(chrome_options=options)
        driver.maximize_window()
        # 隐性等待，最长等10秒
        driver.implicitly_wait(10)
        driver.get(
            'https://signin.aliyun.com/login.htm?callback=https%3A%2F%2Fcloudmonitor.console.aliyun.com%2F%23%2Fhostmonitor%2Fhost'
        )
        # 操作对象
        actions = ActionChains(driver)
        # 用户名
        input = driver.find_elements_by_xpath(
            '//*[@id="--aliyun-xconsole-app"]/div/div[1]/div[2]/div[3]/div/form/div[1]/div[2]/span/input')[0]
        actions.click(input).perform()
        input.send_keys(setting.get('USER_NAME'))
        # 点击下一步
        next_btn = driver.find_elements_by_xpath(
            '//*[@id="--aliyun-xconsole-app"]/div/div[1]/div[2]/div[3]/div/form/div[3]/div/button')[0]
        actions.click(next_btn).perform()
        # 密码
        pass_word = driver.find_elements_by_xpath(
            '//*[@id="--aliyun-xconsole-app"]/div/div[1]/div[2]/div[3]/div/form/div[2]/div[2]/span/input')[0]
        driver.execute_script("arguments[0].focus();", pass_word)
        pass_word.send_keys(setting.get('PASS_WORD'))
        # 登录按钮 //*[@id="u22"]/input
        login_btn = driver.find_elements_by_xpath(
            '//*[@id="--aliyun-xconsole-app"]/div/div[1]/div[2]/div[3]/div/form/div[3]/div/button')[0]
        driver.execute_script("arguments[0].click();", login_btn)

        # 调整每页条数为50
        page_size = driver.find_elements_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/div/div/div/div[3]/table[2]/tfoot/tr/td[2]/div[2]/div/div[2]/span/select')[
            0]
        select = Select(page_size)
        # 选择
        select.select_by_index(3)
        # 最后一页
        last_page = driver.find_elements_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/div/div/div/div[3]/table[2]/tfoot/tr/td[2]/div[2]/div/ul/li[9]/a')[
            0]
        driver.execute_script("arguments[0].click();", last_page)

        # 头像
        login_avatar = driver.find_elements_by_xpath('//*[@id="J_console_base_top_nav"]/div[2]/div[9]/button/img')[0]
        # 鼠标悬浮头像
        ActionChains(driver).move_to_element(login_avatar).perform()
        # 登录名
        login_name = driver.find_elements_by_xpath(
            '//*[@id="J_console_base_top_nav"]/div[2]/div[9]/div/header/header/div/div/div')[0]
        print(login_name.text)
        self.driver = driver

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 休眠两秒，等待数据加载
        time.sleep(3)
        driver = self.driver
        html = driver.page_source
        # 上一页标签
        last_xpath = '/html/body/div[3]/div/div/div[3]/div[2]/div/div/div/div[3]/table[2]/tfoot/tr/td[2]/div[2]/div/ul/li[2]/a'
        last_page = driver.find_elements_by_xpath(last_xpath)[0]
        # 当前页码
        page = driver.find_element_by_css_selector('.pagination li.active a').text
        # 灰色禁用
        spider.logger.info('当前页码' + page)
        if page != '1':
            ActionChains(driver).click(last_page).perform()
        else:
            driver.quit()
            spider.crawler.engine.close_spider(spider, '全文结束关闭爬虫')
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
