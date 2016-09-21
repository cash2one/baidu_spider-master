#coding:utf-8
import bs4
from bs4 import BeautifulSoup as bs
import urllib.parse
import urllib.request

import functools
import re
import time

import PreXiepeiyi

from time import sleep

#import socket
#socket.setdefaulttimeout(3)

class BaiduSpider(object):
    def __init__(self,word,max_link):
        self._word = word
        self._max_link = max_link
        p = {"word":word}
        self._start_url = "http://www.news.baidu.com/ns?" + urllib.parse.urlencode(p)

    def _get_links(self):
        links = []
        links.append(self._start_url)
        try:
            soup = bs(self._get_html(self._start_url),"lxml")
            links_tag = soup.select("#page")
            if 0 != len(links_tag):
                links_tag = links_tag[0]
            #get the second page link
            for child in links_tag.children:
                attr = child.attrs
                if attr:
                    links.append("http://www.news.baidu.com" + attr["href"])
                    break
            #get 20~800 news links
            for i in range(20,810,10):  
                link_temp = links[1].__str__()
                PatternObj = re.compile('&pn=(\\d)+?&')
                newLink = PatternObj.subn('&pn='+str(i)+'&', link_temp )
                links.append(str(newLink[0]))
            end = self._max_link if self._max_link < len(links) else len(links)
        except AttributeError as e_Att:
            print(e_Att)
            time.sleep(10)
            return self._get_links()
        return links[:end]
    
    def _rightTime(self,summary):
        '''
        对于种子协陪义动词判断summary中的时间是否在2016年6月1日至2016年8月17日
        对于预扩展协陪义动词，判断summary中的时间是否在2016年8月20日至2016年9月21日   
        中国基金网  14小时前
        网易新闻  2016年08月12日 16:35
        '''
        #2016-06-01转化为datetime
        try:
            startDate_str = '2016-06-01'
            startTime =  time.mktime(time.strptime(startDate_str, '%Y-%m-%d'))
            a = summary.split()
            time_in_text = a[1]
            if '年' in time_in_text:
                time_in_text = time_in_text.split(" ")[0]
                time_in_text = time_in_text.replace("年",'-').replace("月",'-').replace("日",'')
                textTime = time.mktime(time.strptime(time_in_text, '%Y-%m-%d'))
                if (float(textTime))<=(float(startTime)):
                    return False
            return True
        except Exception:
            return False
    
    
    def _get_html(self,link):
        try:
            request = urllib.request.Request(link)
            res =urllib.request.urlopen(request,timeout=10)
        except Exception as e:       #爬虫卡住或其他异常，则再次尝试，尝试用post方式打开
            print(link+'\n')
            print(e)
            return self._get_html(link)            
        return res.read().decode("utf-8")
    
    def _get_html_Content_post(self,link,f_error,retries):
        print (link,'open the link using the post method:',time.time())
        html_content = ''
        try:
            request = urllib.request.Request(link)
            res =urllib.request.urlopen(request,timeout=3)
            html_content = res.read()
        except Exception as e:       #爬虫卡住或其他异常，则再次尝试，尝试机会有3次
            print(link+'\n')
            print(e)
            f_error.write(link+'\n')
            if retries:
               return self._get_html_Content_post(link, f_error,retries-1)
        print ('close:',time.time())
        return html_content
    
        
    def _get_html_Content(self,link, f_error,retries=2):
        print (link,'\n','open the link:',time.time())
        html_content = ''
        try:
            user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
            headers={'User-Agent':user_agent}
            request = urllib.request.Request(link)
            request.add_header('User-Agent', user_agent)
            #timeout=2
            res =urllib.request.urlopen(request,timeout=3)
            html_content = res.read()
        except Exception as e:       #爬虫卡住或其他异常，则再次尝试，尝试用post方式打开
            print(link+'\n')
            print(e)
            f_error.write(link+'\n')
            if retries:
                return self._get_html_Content_post(link, f_error,retries=3)
        print ('close:',time.time())
        return html_content

    def _get_content(self,content):
        # 先要把bs4.element.NavigableString类型转化为string类型
        return functools.reduce(lambda x,y:x+y,map(lambda x:x.replace("<em>","").replace("</em>",""),
                                     map(lambda x:x.string,content)))
    def _spiderDetail(self, link,f_error,Verbdic):
        '''
        input:link,f_error
        output:contents contained xiepeiyiverb
        通过第一步获取的URL，得到新闻所在的内容页面URL，由于百度新闻列表页面上的新闻来自不同的站，
        所以很难找到一个通用的结构，大多数的新闻类网站，内容都是放在p标签内，所以就采用了如下的方式获取新闻的内容
        '''
        html_content = self._get_html_Content(link, f_error,retries=2)
        contents =''
        if html_content != '':
            soup = bs(html_content,"lxml")
            #reg=u".+?带领"
            #Res = re.compile(reg)
            #contents = soup.findAll(name="p", text=Res)
            contents = '<p>'
            iter = []
            nodes_p = soup.find_all(name='p')
            for n in nodes_p:
                p_cont = n.get_text(strip=True)
                p_cont = re.sub(r'\s','',p_cont)               #去除段落中的换行符
                p_cont = re.sub(r'\r','',p_cont)
                for ver in Verbdic:
                    if ver in p_cont:
                        iter.append(p_cont)
                        break
            contents = contents.join(iter)
        return contents
        
    
    def _spider(self,f, f_error,Verbdic):
        '''
            百度新闻列表页面，
            根据关键词检索新闻，
            获取新闻标题、来源及时间、链接、链接页面文字
        '''
        try:
            total_links = self._get_links()
            print (total_links)
            for i,l in enumerate(total_links):
                print ("Page {0}".format(i+1))
                soup = bs(self._get_html(l),"lxml")
                # 找到左边内容到的跟节点
                left_div = soup.select("#content_left")[0] 
                # base_div_list是一个新闻列表
                for child_div in left_div.children:
                    if isinstance(child_div,bs4.element.Tag) and child_div.div and child_div.div.get('class') and'result' in child_div.div['class']:
                        base_div = child_div
      
                childs = base_div.children
                for child in childs:
                    title = child.select(".c-title")[0]
                    summary = ""
                    summary = summary.join(self._get_content(child.select(".c-summary")[0].p.contents))
                    a_link = title.a["href"]
                    titlename = ""
                    titlename = titlename.join(self._get_content(title.a.contents))
                    #爬取新闻内容网页
                    content = ''
                    if self._rightTime(summary):
                        content = self._spiderDetail(a_link, f_error,Verbdic)
                        
                        titlename = re.sub(r'\r','',titlename)
                        titlename = re.sub(r'\s+?','，',titlename)
                        titlename = titlename+'。'
                        if content != '':
                            f.write ('<title>标题:'+titlename+'\t<resource>来源及时间:'+summary+
                                     '\t<link>链接:'+a_link
                                     +'\t<content>新闻内容:'+content+"\n")
        except UnboundLocalError:
            return self._spider(f, f_error,Verbdic)
                        
                   
    def start(self,f, f_error,Verbdic):
        try:
            self._spider(f,f_error,Verbdic)
        except Exception as e:
            print(e)
        
    def __del__(self):
        print ("__del__")


def getPreVerbdic(ALFA,infile):
    '''
    #infile；每一行包含“协陪义种子次\t比较动词\t相似度  ”
    #提取出相似度大于ALFA的比较动词，并以列表的形式返回
    '''
    verlist = []
    with open(infile,'rt',encoding='utf-8') as reader:
        lines = reader.readlines()
        for line in lines:
            ls = line.split()
            if float(ls[2])>=ALFA:
                verlist.append(ls[1])
    return verlist

def getBtVerDic(bt_file):
    btlist = []
    with open(bt_file,'rt',encoding='utf-8') as bt_r:
        lines = bt_r.readlines()
        for l in lines:
            btlist.append(l[:len(l)-1])
    return btlist

if '__main__' == __name__:
    '''
    #ALFA：预扩充的协陪义动词的相似度阈值
    #Verbdic：ALFA条件下的所有预扩充的协陪义动词，为所有动词生成一个f_over对象
    #为每个预扩充协陪义动词，生成一个f对象、一个f_error对象
    #f：存储一个预扩充协陪义动词的爬取结果
    #f_error：存储读取新闻内容错误的链接
    #f_over：存储已经下载所有句子的协陪义动词
    '''
    ALFA = 1.0
    Verbdic,delbtlist = PreXiepeiyi.getPreXiepeiyiVer(ALFA)
    btVwebdic = []
    
    name_over = "./result_hownet-similarity/overVerb.txt"
    with open(name_over,'wt',encoding='utf-8') as f_over:
        for keyword in Verbdic:
            name = "./result_hownet-similarity/links_"+keyword+".txt"
            name_error = "./result_hownet-similarity/logError_"+keyword+".txt"
            
            with open(name,'wt',encoding='utf-8') as f, open(name_error,'wt',encoding='utf-8') as  f_error:
                baidu_spider = BaiduSpider(keyword,800)
                baidu_spider.start( f, f_error,Verbdic)
                del baidu_spider  #删除对象
                
                f_over.write(keyword+'\n')  
        
    '''
    with open("links1.txt",'wt',encoding='utf-8') as f, open("logError1.txt",'wt',encoding='utf-8') as  f_error, open("overVerb1.txt",'wt',encoding='utf-8') as f_over:
        for keyword in Verbdic:
            baidu_spider = BaiduSpider(keyword,800)
            baidu_spider.start( f, f_error,Verbdic)
            f_over.write(keyword+'\n')
    '''