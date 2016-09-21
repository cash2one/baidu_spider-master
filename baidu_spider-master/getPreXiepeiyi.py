#encoding:utf-8
'''
Created on 2016年9月21日

@author: liuyu
'''
import baidu_spider

def getPreXiepeiyiVer(ALFA):
    
    rlist = []
    infile1 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA,infile1)
    
    infile2 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA, infile2)
    
    infile3 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA, infile3)
    
    infile4 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA, infile4)
    
    infile5 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA, infile5)   

    infile6 = '../source_hownet-similarity/cooperate合作.txt'
    rlist = rlist + baidu_spider.getVerbdic(ALFA, infile6)
    
    return rlist   
    
if __name__ == '__main__':
    ALFA = 1.0
    rlist = getPreXiepeiyiVer(ALFA)
    outfile = '../result_hownet-similarity/pre_xiepeiyiVerb.dic'
    with open(outfile,'wt',encoding='utf-8') as writer:
        for r in rlist:
            writer.write(r+'\n')
