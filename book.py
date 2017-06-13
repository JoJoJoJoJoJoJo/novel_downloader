#-*-coding:utf-8-*-
import re
import requests
from bs4 import BeautifulSoup
import codecs
import sys

class DownloadBook(object):

    def __init__(self,url,path=None):
        
        '''
            params:
                url:包含所有章节目录的页面
                path:最后生成的txt的路径
        '''
        
        self.path = path
        self.url = url
        self.contents = {}

    def get_dirs(self):
        r_dir = requests.get(self.url)
        #正则匹配/book/8017/849147.html这样的地址
        reg = r'/[a-z0-9A-Z_]+/[0-9]{0,5}/([0-9]{0,10}).html'
        chapters = re.findall(reg,r_dir.text)
        self.chapters = map(int,chapters)
        self.chapters.sort()

    def get_content(self):
        for chapter in self.chapters:
            #生成每章地址
            chapter_url = self.url+str(chapter)+'.html'
            r_content = requests.get(chapter_url)
            #显示进程
            print 'processing %s,%s'%(chapter_url,r_content)
            #使用BS获取content和title
            soup = BeautifulSoup(r_content.content,'lxml')
            content = soup.find('div',id='content')
            chapter_title = soup.find('h1')
            #转为str并用正则匹配去掉html标签
            book = re.findall(r'<div id="content">(.*?)</div>',str(content),re.S)[0]
            title = re.findall(r'<h1>(.*?)</h1>',str(chapter_title),re.S)[0]
     
            if self.path is None:
                with codecs.open('book1.txt','a+',encoding='gbk',errors='ignore') as f:
                    f.write(title+'\r\n')
                    f.write(book.replace('<br/>','\r\n')+'\r\n')
            else:
                with codecs.open(path,'a+',encoding='gbk',errors='ignore') as f:
                    f.write(title+'\r\n')
                    f.write(book.replace('<br/>','\r\n')+'\r\n')
        f.close()

if __name__ == '__main__':
    #Windows环境，设置编码为utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    url = 'http://www.zwdu.com/book/8017/'
    app = DownloadBook(url)
    app.get_dirs()
    app.get_content()
    print 'Success!'
            
