#encoding:utf-8
'''
Created on 2016年9月21日

@author: liuyu
'''
import baidu_spider



def getPreXiepeiyiVer(ALFA):
    '''
    #AlFA：预扩充协陪义动词的相似度阈值
    #得到所有相似度比较动词
    #删除重复动词，保证动词的唯一性
    #从相似度比较动词中删除种子协陪义动词
    #返回不包含种子协陪义动词的预扩充的协陪义动词列表
    #返回出现在比较动词中且满足ALFA阈值的种子协陪义动词
    '''
    #得到相似度文件中的所有比较动词
    rlist = []
    infile1 = './source_hownet-similarity/cooperate合作.txt'
    r1list = baidu_spider.getPreVerbdic(ALFA,infile1)
    
    infile2 = './source_hownet-similarity/follow跟随.txt'
    r2list = baidu_spider.getPreVerbdic(ALFA, infile2)
    
    infile3 = './source_hownet-similarity/guide引导.txt'
    r3list = baidu_spider.getPreVerbdic(ALFA, infile3)
    
    infile4 = './source_hownet-similarity/help帮助.txt'
    r4list = baidu_spider.getPreVerbdic(ALFA, infile4)
    
    infile5 = './source_hownet-similarity/HoldWithHand搀扶.txt'
    r5list = baidu_spider.getPreVerbdic(ALFA, infile5)   

    infile6 = './source_hownet-similarity/protect保护.txt'
    r6list = baidu_spider.getPreVerbdic(ALFA, infile6)
    rlist = r1list + r2list + r3list + r4list + r5list + r6list
    
    #删除重复动词
    rlist = list(set(rlist))
    
    #得到种子协陪义动词
    bt_file = './source_btxiepeiyi/bt_xiepeiyiVerb.dic'
    btlist = baidu_spider.getBtVerDic(bt_file)
    
    #从相似度比较动词中删除种子协陪义动词
    delbtlist = set()
    rlist_ = list(rlist)
    for r in rlist_:
        print(r)
        if r in btlist:
            rlist.remove(r)
            delbtlist.add(r)
    
    delbtlist = list(delbtlist)
    
    return rlist,delbtlist  

    
if __name__ == '__main__':
    ALFA = 1.0
    rlist,delbtlist = getPreXiepeiyiVer(ALFA)
    outfile1 = './result_hownet-similarity/pre_xiepeiyiVerb.dic'
    outfile2 = './result_hownet-similarity/del_bt_xiepeiyiVerb.dic'
    with open(outfile1,'wt',encoding='utf-8') as writer1,open(outfile2,'wt',encoding='utf-8') as writer2:
        for r1 in rlist:
            writer1.write(r1+'\n')
        for r2 in delbtlist:
            writer2.write(r2+'\n')            
