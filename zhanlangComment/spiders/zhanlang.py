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

import random
class ZhanlangSpider(scrapy.Spider):
    name = 'zhanlang'
    allowed_domains = ['https://movie.douban.com/subject/26363254/comments/']
    # start_urls = ['https://movie.douban.com/subject/26363254/comments']
    # header = {
    #     # "User-Agent":
    # }
    #请求登录页面
    def start_requests(self):
        post_url = "https://accounts.douban.com/login"
        return [Request(url=post_url,  callback=self.login)]
    #通过验证码登录
    def login(self, response):
        #创建session会话
        session = requests.session()
        post_url = "https://accounts.douban.com/login"
        #获取验证码图片的url
        captcha_url = response.xpath('//*[@id="captcha_image"]/@src').extract()[0].strip()
        print(captcha_url)
        #获取验证码图片的id，用于填写登录formdata
        captcha_id = captcha_url.replace("https://www.douban.com/misc/captcha?id=","").replace("&size=s","")
        print(captcha_id)
        #获取验证码图片并将其打开
        t = session.get(captcha_url)
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
        #输入验证码
        captcha = input("请输入验证码：\n")
        #定义formdata，个参数。。。
        post_data = {
            "form_email": "用户名",
            "form_password": "用户密码",
            "captcha-solution":captcha,
            "captcha-id": captcha_id,
            "redir": "https://movie.douban.com/subject/26363254/comments"
        }
        #使用scrapy内置的FormRequest提交登录表单
        return [scrapy.FormRequest(url='https://accounts.douban.com/login', formdata=post_data, callback=self.check_login, dont_filter=True)]
    #可以在这个方法中定义验证登录
    def check_login(self,response):
        #如果登陆成功则跳转到parser
        yield Request('https://movie.douban.com/subject/26363254/comments', callback = self.parse, dont_filter=True)


    def parse(self, response):
        #获取一页的评论的用户名，评论时间，评论内容
        username = response.css("#comments div div.comment h3 span.comment-info a::text").extract()
        time = response.css("#comments div div.comment h3 span.comment-info span.comment-time::text").extract()
        comment = response.css("#comments div div.comment p::text").extract()
        print(username)
        print(time)
        print(comment)
        #将这页爬取的内容保存在item中，其中item为数据库insert的对象，在item中定义
        for i in range(0, len(username)-1):
            # print()
            item = ZhanlangcommentItem()
            item["username"] = username[i].strip()
            item["time"] = time[i].strip()
            item["comment"] = comment[i].strip()
            yield item
        #查看页面中是否有下一页按钮，如果有则访问下一页的网址，否则退出
        next_page = response.css("#paginator a.next::attr(href)")
        # next_page_url = ""
        if next_page:
            next_page_url_part = next_page.extract_first("")
            next_page_url = parse.urljoin(response.url, next_page_url_part)
            print(next_page_url)
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        else:
            pass





