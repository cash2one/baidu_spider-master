#encoding:utf-8
'''
Created on 2016年8月17日

@author: liuyu
'''
import re
import os
    
    
if '__main__' == __name__:
    inFile = 'C:\\Users\\liuyu\\Desktop\\爬虫\\baidu_spider-master\\result\\baidu news\\links.txt'
    outFile = 'C:\\Users\\liuyu\\Desktop\\爬虫\\baidu_spider-master\\result\\baidu news\\linksFixed.txt'
    with open(inFile,'rt', encoding='utf-8') as reader,open(outFile,'wt',encoding='utf-8') as writer:
        lines = reader.readlines()
        lines = ''.join(lines)
        lines = re.sub('\n', '', lines)
        lines = re.split('标题:', lines)
        for line in lines:
            writer.write('标题:'+line+'\n')
            
