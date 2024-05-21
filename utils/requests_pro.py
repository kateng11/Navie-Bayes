import random
import re
import joblib
from snownlp import SnowNLP
import requests
from lxml import etree
from model.TrainModel import tokenize
from api.predicteds import sentiment_predicted
from utils.mysql_pro import orm_standby


naive_bayes = joblib.load('file/naive_bayes_model.pkl')
tfidf_vectorizer = joblib.load('file/tfidf_vectorizer.pkl')


class Tieba(object):

    def __init__(self, name,page):
        self.page = page + 1
        self.url = f'https://tieba.baidu.com/f?kw={name}'
        self.headers = {
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
            'User-Agent': '/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) '     #  低端浏览器没有被<!--  -->注释掉
        }
        # self.f = open('关键词.csv', 'w', encoding='utf-8-sig', newline="")
        # self.csv_write = csv.writer(self.f)

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        #  把浏览器响应的内容保存到本地，以便查看响应的源码
        # with open('tieba.html', 'wb') as f:
        #     f.write(response.content)
        return response.content

    def parse_data(self, data):
        #  创建element对象
        data = data.decode().replace("<!--", "").replace("-->", "")  # 高端浏览器会把一些内容给注释掉的
        el_html = etree.HTML(data)
        # el_list = el_html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')  #  此处输出的是对象
        el_list = el_html.xpath('//*[@id="thread_list"]/li/div')  # 此处输出的是对象
        # print(len(el_list))
        # exit()
        data_list = []
        for el in el_list:
            tmp = {}
            tmp['title'] = el.xpath('./div[2]/div[1]/div[1]/a/text()')[0]  # 此处xpath取出的数据是列表，所以加上索引[0]
            tmp['href'] = 'http://tieba.com' + el.xpath('./div[2]/div[1]/div[1]/a/@href')[0]  # 此处取出的索引是相对路径，所以前面还要拼接字符串
            try:
                tmp['author'] = el.xpath('./div[2]/div[1]/div[2]/span[1]/span[1]/a/text()')[0]
            except:
                tmp['author'] = el.xpath('./div[2]/div[1]/div[2]/span[1]/span[1]/a/text()')
            try:
                tmp['reviewer'] = el.xpath('./div[2]/div[2]/div[2]/span[1]/a/text()')[0]
            except:
                tmp['reviewer'] = el.xpath('./div[2]/div[2]/div[2]/span[1]/a/text()')
            try:
                tmp['last_comment_time'] = el.xpath('./div[2]/div[2]/div[2]/span[2]/text()')[0]
            except:
                tmp['last_comment_time'] = el.xpath('./div[2]/div[2]/div[2]/span[2]/text()')
            try:
                tmp['comment'] = el.xpath('./div[2]/div[2]/div[1]/div/text()')[0]
            except:
                tmp['comment'] = el.xpath('./div[2]/div[2]/div[1]/div/text()')
            data_list.append(tmp)
        # print(data_list)

        #  获取csv他属性值
        a = []
        dict = data_list[0]
        for headers in sorted(dict.keys()):  # 把字典的键取出来
            a.append(headers)
        header = a  # 把列名给提取出来，用列表形式呈现
        # print(a)
        # self.csv_write.writerow(['title', 'href', 'author', 'reviewer', 'last_comment_time', 'comment'])
        # self.csv_write.writerow(a)

        try:
            # next_url = 'https' + el_html.xpath('//a[@class="next pagination-item "]/@href')
            next_url = 'https:' + el_html.xpath('//a[contains(text(),"下一页")]/@href')[0]
        except:
            next_url = None
        return data_list, next_url, header

    def save_data(self, data_list, header,sentencesL,labelsL):
        orm_standby()
        from database import models
        for data in data_list:
            try:
                # print(data)
                try:
                    data['last_comment_time'] = data['last_comment_time'].replace('\r', '').replace('\n', '').strip()
                    data['comment'] = data['comment'].strip().replace('\r', '').replace('\n', '')
                except:
                    print('爬取异常，请联系管理员QQ 995405033 处理')
                # self.csv_write.writerow([data['title'], data['href'], data['author'], data['reviewer'], data['last_comment_time'],data['comment']])
                # print("每行数据",data['title'], data['href'], data['author'], data['reviewer'], data['last_comment_time'],data['comment'])
                print("{} -- {} --    入库成功".format(data['title'],data['href']))
                if models.ReqeustsData.objects.filter(name=data['title']).exists() == False:
                    comment_text = data['comment']
                    sentiment= predict_sentiment(comment_text)
                    models.ReqeustsData.objects.create(name=data['title'], url=data['href'],
                                                       author=data['author'], reviewer=data['reviewer'],
                                                last_comment_time=data['last_comment_time'], comment=comment_text,labels=sentiment)
            except:
                pass

    def run(self):
        orm_standby()
        from database import models

        # 整理训练集
        R = models.List.objects.all()
        sentencesL = []
        labelsL = []
        for obj in R:
            sentencesL.append(obj.sentences)
            labelsL.append(obj.labels)

        #  url
        #  headers
        next_url = self.url
        for _ in range(1,self.page + 1):
            #  发送请求，获取响应
            data = self.get_data(next_url)
            #  从响应中提取数据（数据和翻页用的url）
            data_list, next_url, a = self.parse_data(data)
            self.save_data(data_list, a ,sentencesL,labelsL)
            #  判断是否终结
            if next_url == None:
                break




# 随机UA的请求头
def head():
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                  'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                  'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                  'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                  ]
    user_agent = random.choice(user_agent)
    headers = {

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': user_agent,  # 设置随机请求头
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',

    }
    return headers

def user_agent():
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                  'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                  'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                  'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                  ]
    return random.choice(user_agent)

# 配置请求头
def session_requests_b():
    session = requests.Session()  # 设置session
    headers = head()
    session.headers.update(headers)  # 配置请求头
    # print(session.cookies)
    return session

def predict_sentiment(text):
    # 分词处理
    tokenized_text = tokenize(text)
    # 转换为TF-IDF向量
    text_tfidf = tfidf_vectorizer.transform([tokenized_text])
    # 进行情感预测
    prediction = naive_bayes.predict(text_tfidf)[0]
    # 将预测结果转换为积极或消极的字符串
    sentiment = "正面情绪" if prediction == 1 else "负面情绪"
    return sentiment

if __name__ == '__main__':
    list = [data for data in range(1,15)]
    print(list)


