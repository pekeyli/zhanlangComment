import requests
from scrapy.selector import Selector
import pymongo
import random
connection = pymongo.MongoClient('localhost', 27017)
db = connection['ip_proxy']
collection = db['ip_proxy']

def crawl_ips():
    # 爬取西刺免费代理IP
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    count = 0
    for i in range(2370):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i+1), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]
            print(all_texts)
            ip_list.append((ip,port,proxy_type,speed))

        # print(re.text)
        item = {}
        for i in ip_list:
            item = {
                '_id':count,
                'ip':i[0],
                'port':i[1],
                'proxy':'HTTP',
                'speed':i[3],
                'is_del':0,
            }
            collection.insert(item)
            count += 1
class GetIp(object):
    all_ip_count = collection.count()
    print(all_ip_count)
    def get_random_ip(self):
        # 从数据库这哦你随机获取一个ip
        get_id = random.randint(0, self.all_ip_count-1)
        while not collection.find({"_id":get_id,"is_del":0}):
            get_id = random.randint(0, self.all_ip_count - 1)
        print(get_id)
        ip_str = collection.find({"_id":get_id})
        print(ip_str)
    # def judge_ip(self, ip, port):
    #     http_url = "https://www.baidu.com"
    #     proxy_url = "http://{0}:{1}".format(ip,port)
    #     proxy_dict = {
    #
    #     }
if __name__ == '__main__':
    get_ip = GetIp()
    get_ip.get_random_ip()
    # print(crawl_ips())

