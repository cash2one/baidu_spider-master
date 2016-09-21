#encoding:utf-8
'''
Created on 2016年8月16日

@author: liuyu
'''
import re
import time

class preprocessor:
    def __init__(self,titles,contents):
        self._titles = titles
        self._contents = contents
    
    def _sepContent(self):
        paragraphs = []
        sentences = []
        i=0
        for content in self._contents:
            print(i)
            i=i+1
            print(content)
            paragraphs.extend(re.split('<p>', content))
            for para in paragraphs:
                sentences.extend( re.split('。|？', para))
        return sentences
    
    def _duplicate_removal(self):
        
        titlesCount = len(self._titles)
        titlesDic = dict(zip(self._titles, ['']*titlesCount))
        
        sentences = self._sepContent()
        sentencesCount = len(sentences)
        sentencesDic = dict(zip(sentences, ['']*sentencesCount))
        
        titles = list(titlesDic.keys())
        sentences = list(sentencesDic.keys())
        return titles, sentences
    
    
if '__main__' == __name__:

    inFile = 'H:\\协陪义动词实验20150326\\baidu_spider-master2\\result\\baidu news\\linksFixed.txt'
    titleFile = 'H:\\协陪义动词实验20150326\\baidu_spider-master2\\result\\baidu news\\titles.txt'
    sentenceFile = 'H:\\协陪义动词实验20150326\\baidu_spider-master2\\result\\baidu news\\sentences.txt'
    t_titles = []
    t_contents = []
    with open(inFile,'rt',encoding='utf-8') as reader:
        lines = reader.readlines()
        for line in lines:
            if '标题:' in line and '来源及时间:' in line and '链接:' in line and '新闻内容:' in line:
                title = re.split('\t来源及时间:',re.split('标题:',line)[1])[0]
                try :
                    content = re.split('\t新闻内容:',line)[1]
                except IndexError as e:
                        print (line)
                t_titles.append(title)
                t_contents.append(content)
    pre_processor = preprocessor(t_titles,t_contents)
    titles,sentences = pre_processor._duplicate_removal()
    sentences.remove('')
    #del sentences elements if it in titles
    sentences.extend(titles)
    sentences = list(set(sentences))
    sentences = [x for x in sentences if x not in titles]
    with open(titleFile,'wt',encoding='utf-8') as t, open(sentenceFile,'wt',encoding='utf-8') as s:
        for i in iter(range(len(titles))):
            titles[i] = re.sub('\.\.\.','',titles[i])
            t.write('td-'+str(i+1)+'\t'+titles[i]+'\n')
        for j in iter(range(len(sentences))):
            sentences[j] = re.sub('\n','',sentences[j])
            sentences[j] = re.sub('&nbsp',"",sentences[j])
            sentences[j] = re.sub('(.+?)',"",sentences[j])
            sentences[j] = re.sub('（.+?）',"",sentences[j])
            if '|' not in sentences[j] and 'padding-right' not in sentences[j] and 'span' not in sentences[j]:
                s.write('sd-'+str(j+1)+'\t'+sentences[j]+'。\n')
            
            
        
