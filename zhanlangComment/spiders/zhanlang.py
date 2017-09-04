# -*- coding: utf-8 -*-
import json

import scrapy
import re

from scrapy import FormRequest
from scrapy.http import Request
from urllib import parse
import requests
from PIL import Image
from zhanlangComment.items import ZhanlangcommentItem
class ZhanlangSpider(scrapy.Spider):
    name = 'zhanlang'
    allowed_domains = ['https://movie.douban.com/subject/26363254/comments/']
    # start_urls = ['https://movie.douban.com/subject/26363254/comments']

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",

    }

    def start_requests(self):
        post_url = "https://accounts.douban.com/login"
        return [Request(url=post_url,  callback=self.login)]

    def login(self, response):
        session = requests.session()
        post_url = "https://accounts.douban.com/login"
        captcha_url = response.xpath('//*[@id="captcha_image"]/@src').extract()[0].strip()
        print(captcha_url)
        captcha_id = captcha_url.replace("https://www.douban.com/misc/captcha?id=","").replace("&size=s","")
        print(captcha_id)
        t = session.get(captcha_url, headers=self.header)
        print(t)
        with open("captcha.jpg","wb") as f:
            f.write(t.content)
            f.close()
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass
        captcha = input("请输入验证码：\n")
        post_data = {
            "form_email": "1226710837@qq.com",
            "form_password": "Z9l5kdceR,2NGp",
            "captcha-solution":captcha,
            "captcha-id": captcha_id,
            "redir": "https://movie.douban.com/subject/26363254/comments"
        }
        return [scrapy.FormRequest(url='https://accounts.douban.com/login', formdata=post_data, callback=self.check_login, dont_filter=True)]

    def check_login(self,response):
        yield Request('https://movie.douban.com/subject/26363254/comments', callback = self.parse, dont_filter=True)


    def parse(self, response):
        username = response.css("#comments div div.comment h3 span.comment-info a::text").extract()
        time = response.css("#comments div div.comment h3 span.comment-info span.comment-time::text").extract()
        comment = response.css("#comments div div.comment p::text").extract()
        print(username)
        print(time)
        print(comment)
        for i in range(0, len(username)-1):
            # print()
            item = ZhanlangcommentItem()
            item["username"] = username[i].strip()
            item["time"] = time[i].strip()
            item["comment"] = comment[i].strip()
            yield item
        next_page = response.css("#paginator a.next::attr(href)")
        # next_page_url = ""
        if next_page:
            next_page_url_part = next_page.extract_first("")
            next_page_url = parse.urljoin(response.url, next_page_url_part)
            print(next_page_url)
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        else:
            pass





