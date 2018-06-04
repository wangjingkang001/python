#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys
import random
import string
import re
import md5
import time
import json
import shutil
import subprocess #调用命令方法
import hashlib 
import time
import datetime #获取当前时间
from os.path import join, getsize
s = os.sep #多平台 路径分割符号是'\',在Linux上是‘/’


#随机生成文件配置类
baseFileNameList_OC = []                   # 文件名存储list_OC
baseFileDic_OC = {}                        # 文件名和类名的字典_OC

baseFileNameList_C = []                    # 文件名和类名的字典_C
baseFileDic_C = {}                         # 文件名和类名的字典_C

ocFileRandomMin = 10
ocFileRandomMax = 30
cFileRandomMin = 5
cFileRandomMax = 20
cppFileRandomMin = 1
cppFileRandomMax = 5

baseFileTitle = ['Auto', 'Make', 'File', 'Del', 'FindMine','KuYi','CFG','WenQi','Done','Feimiao']

baseNowDateTimes = '2016/06/06'         # 注释中日期
baseString = 'china'                    # 注释中图片
baseRadomString = 'ASDFZXC'             # 注释中图片
baseImageTitle = ['佛祖', '老天', '大地', '瑞兽', '小凡', '虚竹', '乔峰','段誉','龙神','TI']   # 注释中图片Title  
baseTitleNameString = 'wangjk'          # 注释中name
baseContext = {                         # 模拟配置项
    'key' : 'wang',
    'add_func_num' : 10,

    'base_in_path' : '',
    'base_out_path' : './newFiles',

    'c_in_path' : '',
    'c_out_path' : './newFiles/codec',

    'oc_in_path':'',
    'oc_out_path':'./newFiles/codeoc',

    'cpp_in_path':'',
    'cpp_out_path':'./newFiles/codec',

    'isaddfunc':True,    #加混淆开关
    'isaddfile':True,    #加文件开关
    'isadddesc':True,     #加注释开关   c++添加没有用   会被过滤掉
    'isaddfile_c':True
}

#----------------------------------------------------通用模块------------------------------------------------
class ProgressBar: # 终端进度条
    def __init__(self, count = 0, total = 0, width = 50):
        self.count = count
        self.total = total
        self.width = width
    def move(self):
        self.count += 1
        return self.count
    def log(self, s = ""): #显示进度
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        # print s
        progress = self.width * self.count / self.total
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()
# 判断文件是否存在key r
def StrIsInFile(filepath,r):
    fp =open(filepath,'r+')
    # print name
    for line in fp.readlines():
        if r in line:
            return True
    fp.close()
    return False
# 得到一个md5加密名字
def getOneName(filename):
    # 随机方法
    # num = random.randint(10, 20) 
    # random.uniform  
    # random.randint   
    # random.randrange(0, 101, 2)   
    # random.choice('abcdefg&#%^*f')  
    # random.sample('abcdefghij',3) 

    # m1 = md5.new()
    m1 = hashlib.md5()
    m1.update(baseContext['key']+filename.split(s)[-1])   #更新一次 改变一次  filename格式为  文件名 + 方法行号 + 方法当前方法行数
    # print filename.split("/")[-1]
    text =  m1.hexdigest()
    text = text[0:7]
    # return string.join(random.sample(m1.hexdigest(),random.randint(4,10)),"")
    # print text,baseContext['key']+filename.split(s)[-1]
    return str(text)
        # names[asciis] = chr(asciis)
# 得到字段头   为了好查找   暂时先只加一个
def getHeadName():
    return random.choice ( ['get'])
#----------------------------------------------------通用模块end------------------------------------------------

#----------------------------------------------------生成一个图形注释start---------------------------------------------

def addDaHuang():
    text = [
    '\n/**                                                                         '+baseString+'保佑必过包',
    '\n*          .,:,,,                                        .::,,,::.          '+baseString+'保佑必过包',
    '\n*        .::::,,;;,                                  .,;;:,,....:i:         '+baseString+'保佑必过包',
    '\n*        :i,.::::,;i:.      ....,,:::::::::,....   .;i:,.  ......;i.        '+baseString+'保佑必过包',
    '\n*        :;..:::;::::i;,,:::;:,,,,,,,,,,..,.,,:::iri:. .,:irsr:,.;i.        '+baseString+'保佑必过包',
    '\n*        ;;..,::::;;;;ri,,,.                    ..,,:;s1s1ssrr;,.;r,        '+baseString+'保佑必过包',
    '\n*        :;. ,::;ii;:,     . ...................     .;iirri;;;,,;i,        '+baseString+'保佑必过包',
    '\n*        ,i. .;ri:.   ... ............................  .,,:;:,,,;i:        '+baseString+'保佑必过包',
    '\n*        :s,.;r:... ....................................... .::;::s;        '+baseString+'保佑必过包',
    '\n*        ,1r::. .............,,,.,,:,,........................,;iir;        '+baseString+'保佑必过包',
    '\n*        ,s;...........     ..::.,;:,,.          ...............,;1s        '+baseString+'保佑必过包',
    '\n*       :i,..,.              .,:,,::,.          .......... .......;1,       '+baseString+'保佑必过包',
    '\n*      ir,....:'+baseRadomString+':,       ,,.,::.     .r5S9989'+baseRadomString+'hr;. ....,.:s,      '+baseString+'保佑必过包',
    '\n*     ;r,..,'+baseRadomString+'13XHAG3i   .,,,,,,,.  ,S931,.,,.;s;s&BHHA8s.,..,..:r:     '+baseString+'保佑必过包',
    '\n*    :r;..rGGh,  :SAG;;G@BS:.,,,,,,,,,.r83:      hHH1sXMBHHHM3..,,,,.ir.    '+baseString+'保佑必过包',
    '\n*   ,si,.1GS,   '+baseRadomString+'&MBMB5,,,,,,:,,.:&8       '+baseRadomString+'MBHBBH#X,.,,,,,,rr    '+baseString+'保佑必过包',
    '\n*   ;1:,,SH:   .'+baseRadomString+'&8H#BS,,,,,,,,,.,5XS,     '+baseRadomString+'&59M#As..,,,,:,is,   '+baseString+'保佑必过包',
    '\n*  .rr,,,;9&1   '+baseRadomString+'&8AMGr,,,,,,,,,,,:h&&9s;   r9&BM'+baseRadomString+':  . .,,,,;ri.  '+baseString+'保佑必过包',
    '\n*  :1:....:5&XSi;'+baseRadomString+'HA9r:,......,,,,:'+baseRadomString+'8899XHHH&GSr.      ...,:rs.  '+baseString+'保佑必过包',
    '\n*  ;s.     .:sS8G8GG889hi.        ....,,:;:,.:irssrriii:,.        ...,,i1,  '+baseString+'保佑必过包',
    '\n*  ;1,         ..,....,,isssi;,        .,,.                      ....,.i1,  '+baseString+'保佑必过包',
    '\n*  ;h:               '+baseRadomString+'BBHAX9:         .                     ...,,,rs,  '+baseString+'保佑必过包',
    '\n*  ,1i..            :'+baseRadomString+'BMHB##s                             ....,,,;si.  '+baseString+'保佑必过包',
    '\n*  .r1,..        ,..;'+baseRadomString+'HBB#Bh.     ..                    ....,,,,,i1;   '+baseString+'保佑必过包',
    '\n*   :h;..       .,..;,'+baseRadomString+'BXs,.,, .. :: ,.               ....,,,,,,ss.   '+baseString+'保佑必过包',
    '\n*    ih: ..    .;;;, ;;:s58A3i,..    ,. ,.:,,.             ...,,,,,:,s1,    '+baseString+'保佑必过包',
    '\n*    .s1,....   .,;sh,  ,iSAXs;.    ,.  ,,.i85            ...,,,,,,:i1;     '+baseString+'保佑必过包',
    '\n*     .rh: ...     rXG9XBBM#M#MHAX3hss13&&HHXr         .....,,,,,,,ih;      '+baseString+'保佑必过包',
    '\n*      .s5: .....    i598X&&A&AAAAAA&XG851r:       ........,,,,:,,sh;       '+baseString+'保佑必过包',
    '\n*      . ihr, ...  .         ..                    ........,,,,,;11:.       '+baseString+'保佑必过包',
    '\n*         ,s1i. ...  ..,,,..,,,.,,.,,.,..       ........,,.,,.;s5i.         '+baseString+'保佑必过包',
    '\n*          .:s1r,......................       ..............;shs,           '+baseString+'保佑必过包',
    '\n*          . .:shr:.  ....                 ..............,ishs.             '+baseString+'保佑必过包',
    '\n*              .,issr;,... ...........................,is1s;.               '+baseString+'保佑必过包',
    '\n*                 .,is1si;:,....................,:;ir1sr;,                  '+baseString+'保佑必过包',
    '\n*                    ..:isssssrrii;::::::;;iirsssssr;:..                    '+baseString+'保佑必过包',
    '\n*                         .,::iiirsssssssssrri;;:.                      '+baseString+'保佑必过包',
    '\n*/ //'+baseString+'保佑必过包\n//'+baseString+'保佑必过包\n//'+baseString+'保佑必过包\n\n'
    ]
    return text

def addCNM():
    text = [
        '//\n',
        '//      ┏┛ ┻━━━━━┛ ┻┓          \n',
        '//      ┃　　　　　　 ┃          \n',
        '//      ┃　　　━　　　┃          \n',
        '//      ┃　┳┛　  ┗┳　┃          \n',
        '//      ┃　　　　　　 ┃          \n',
        '//      ┃　　　┻　　　┃          \n',
        '//      ┃　　　　　　 ┃          \n',
        '//      ┗━┓　　　┏━━━┛          \n',
        '//        ┃　　　┃   神兽保佑        \n',
        '//        ┃　　　┃   代码无BUG！     \n',
        '//        ┃　　　┗━━━━━━━━━┓        \n',
        '//        ┃　　　　　　　    ┣┓      \n',
        '//        ┃　　　　         ┏┛      \n',
        '//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛        \n',
        '//          ┃ ┫ ┫   ┃ ┫ ┫          \n',
        '//          ┗━┻━┛   ┗━┻━┛          \n'
    ]
    return text
def addFZ():
    text = [
        '//                            _ooOoo_          \n',
        '//                           o8888888o         \n',
        '//                           88" . "88         \n',
        '//                           (| -_- |)         \n',
        '//                           O\  =  /O         \n',
        '//                        ____/`---`\____      \n',
        '//                      .`  \\|     |//  `.    \n',
        '//                     /  \\|||  :  |||//  \   \n',
        '//                    /  _||||| -:- |||||-  \  \n',
        '//                    |   | \\\  -  /// |   |  \n',
        '//                    | \_|  ''\---/''  |   |  \n',
        '//                    \  .-\__  `-`  ___/-. /  \n',
        '//                  ___`. .  '+'//"--.--\  `. . __\n',
        '//               .'+'  < '+'  `.___\_<|>_/___.' +'>.'+' \n',
        '//              | | :  `- \`.;`\ _ /`;.`/ - ` : | |\n',
        '//              \  \ `-.   \_ __\ /__ _/   .-` /  /\n',
        '//         ======`-.____`-.___\_____/___.-`____.-''======\n',
        '//                            `=---=''                    \n',
        '//        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n',
        '//                      Buddha Bless, No Bug !            \n'
    ]
    return text

def addCNM2():
    text = [
    '/**\n',
    '*　　　　　　　 ┏┓       ┏┓+ +\n',
    '*　　　　　　　┏┛┻━━━━━━━┛┻┓ + +\n',
    '*　　　　　　　┃　　　　　　 ┃\n',
    '*　　　　　　　┃　　　━　　　┃ ++ + + +\n',
    '*　　　　　　 █████━█████  ┃+\n',
    '*　　　　　　　┃　　　　　　 ┃ +\n',
    '*　　　　　　　┃　　　┻　　　┃\n',
    '*　　　　　　　┃　　　　　　 ┃ + +\n',
    '*　　　　　　　┗━━┓　　　 ┏━┛\n',
    '*               ┃　　  ┃\n',
    '*　　　　　　　　　┃　　  ┃ + + + +\n',
    '*　　　　　　　　　┃　　　┃　Code is far away from     bug with the animal protecting\n',
    '*　　　　　　　　　┃　　　┃ + 　　　　         神兽保佑,代码无bug\n',
    '*　　　　　　　　　┃　　　┃\n',
    '*　　　　　　　　　┃　　　┃　　+\n',
    '*　　　　　　　　　┃　 　 ┗━━━┓ + +\n',
    '*　　　　　　　　　┃ 　　　　　┣┓\n',
    '*　　　　　　　　　┃ 　　　　　┏┛\n',
    '*　　　　　　　　　┗┓┓┏━━━┳┓┏┛ + + + +\n',
    '*　　　　　　　　　 ┃┫┫　 ┃┫┫\n',
    '*　　　　　　　　　 ┗┻┛　 ┗┻┛+ + + +\n',
    '*/\n'
    ]
    return text
#----------------------------------------------------生成一个图形注释end---------------------------------------------


#----------------------------------------------------生成文件信息模块start------------------------------------------------

# 自动生成oc.h文件
def autoTexth(filename):
    global baseFileDic_OC

    text = ['//  '+filename+'.h\n',
    '//  '+filename+'\n',
    '//  \n',
    '//  Created by '+baseTitleNameString+' on  '+baseNowDateTimes+'.\n',
    '//  Copyright (c) 2013 maple. All rights reserved.\n',
    '//  \n',
    '\n',
    '#import <Foundation/Foundation.h>\n',
    ' @interface '+filename+' : NSObject\n\n']

    endText = [
    '\n @end\n']

    codeNameList = []
    for a in range(random.randint(2,12)):
        codeRadomTitle = random.choice ( ['get', 'set', 'make', 'done', 'take','find','add','del','let'])   #随机标题
        codeRadomString =  codeRadomTitle +''.join(random.sample(string.ascii_letters + string.digits, 10)) #随机字符串
        addText = [' + (NSString*)'+codeRadomString+';\n']
        text = text + addText
        codeNameList.append(codeRadomString)

        pass
    
    text = text + endText
    baseFileDic_OC[filename] = codeNameList
    return text

# 自动生成oc.m文件
def autoTextM(filename):
    global baseFileDic_OC

    codeNameList = baseFileDic_OC[filename]
    text = [
        '//  '+filename+'.m\n',
        '//  '+baseTitleNameString+'\n',
        '//  \n',
        '//  Created by '+baseTitleNameString+' on  '+baseNowDateTimes+'.\n',
        '//  Copyright © 2018年 Wang. All rights reserved.\n',
        '//\n',
        '\n',
        '#import \"'+filename+'.h\"\n',
        '@implementation '+filename+'\n',
        '\n\n']
    endText = [
        '@end//\n']

    for code in codeNameList:
        addText = ['// '+code+'\n',
        ' + (NSString*)'+code+';\n',
        '{\n',
        '   NSString *ud'+code+' = @\"'+str(random.randint(100,10000000))+'\";\n',
        '   NSString *str'+code+' = [NSString stringWithFormat:@"%@+%@",ud'+code+',@\"'+code+'\"];\n',
        '   NSLog(@"%@",str'+code+');\n',
        '   return str'+code+';\n',
        '}\n\n']
        text = text + addText
        pass
    
    text = text + endText

    return text

# 自动生成cpp.cpp文件
def autoTextCpluscpp(filename):

    functionname0 = 'xn' + getOneName(filename+'0')
    functionname1 = 'xn' + getOneName(filename+'1')
    functionname2 = 'xn' + getOneName(filename+'2')
    functionname3 = 'xn' + getOneName(filename+'3')
    functionname5 = 'xn' + getOneName(filename+'4')
    functionname4 = getHeadName()+getOneName(filename+'4')
    text = [
        '#include <time.h>\n'
        'bool GetIs'+filename+'(){\n',

        '   int '+functionname1 + '=' + '12312312'+';\n',
        '   int '+functionname2 + '=' + '45645645'+';\n',
        '   int '+functionname3+'='+functionname1+'+'+functionname2+';\n',
        '   bool '+functionname5+' = '+functionname3+'> 0; \n',
        '   time_t tt = time(NULL);\n\n',
        '   tm* t = localtime(&tt);\n\n',
        '   bool Is'+filename+' = false;\n',
        '   if (t->tm_year > 0){\n',
        '       Is'+filename+' = true;\n\n',
        '   }\n',
        '    return Is'+filename+' and '+functionname5+';\n\n',
        '}\n'
    ]
    return text
# 生成一个C++  extern 声明 .h
def autoTextCplusH(filename):
    text = [
        '   extern bool GetIs'+filename+'();\n\n'
    ]
    return text

# 自动生成c mm文件
def autoTextCMM(filename):
    functionname1 = 'xn' + getOneName(filename+'1')
    functionname2 = 'xn' + getOneName(filename+'2')
    functionname3 = 'xn' + getOneName(filename+'3')
    text = [
        'int '+filename+'(int num1, int num2){\n',
        '   int '+functionname1 + '=' + str(random.randint(1000,100000))+';\n',
        '   int '+functionname2 + '=' + str(random.randint(2200,200000))+';\n',
        '   int '+functionname3+'='+functionname1+'+'+functionname2+';\n',
        '   int result;'
        '   if (num1 > num2){\n',
        '       result = num1;\n',
        '   }\n',
        '   else{\n'
        '       result = num2;\n',
        '   }\n',
        '}\n']
    return text
# 生成一个C 声明 .h
def autoTextCH(filename):
    text = [
        '   int '+filename+'(int num1, int num2);\n\n'
    ]
    return text

# 生成OC文件
def addOneOcFile(filename):
    #把文件名加入list
    baseFileNameList_OC.append(filename)

    #生成h文件
    fp = open(baseContext['oc_out_path'] + s+filename+".h",'w')
    #生成h文件内容并写入
    text = autoTexth(filename)
    for item in text:
        fp.write(item)
    fp.close()

    #生成m文件
    fp = open(baseContext['oc_out_path'] + s+filename+".m",'w')
    #生成m文件的内容 并写入
    text = autoTextM(filename)
    # text = text + autoTextCpluscpp(filename,"fn")
    for item in text:
        fp.write(item)
    fp.close()

# 生成CPP文件
def addOneCppFile(filename):
    #生成h文件
    fp = open(baseContext['cpp_out_path'] + s+filename+".h",'w')
    text = autoTextCplusH(filename)
    for item in text:
        fp.write(item)
    fp.close()

    #生成cpp文件
    fp = open(baseContext['cpp_out_path'] + s+filename+".cpp",'w')
    text = autoTextCpluscpp(filename)
    for item in text:
        fp.write(item)
    fp.close()

# 生成C文件 这里指生成混合文件 .mm包含c cpp oc
def addOneCFile(filename):
    #把文件名加入list
    baseFileNameList_C.append(filename)
    #生成h文件
    fp = open(baseContext['c_out_path'] + s+filename+".h",'w')
    text = autoTextCH(filename)
    for item in text:
        fp.write(item)
    fp.close()

    #生成cpp文件
    fp = open(baseContext['c_out_path'] + s+filename+".mm",'w')
    text = autoTextCMM(filename)
    for item in text:
        fp.write(item)
    fp.close()
    
def delAllFiles():

    #删除目录
    if os.path.exists(baseContext['base_out_path']) :
        shutil.rmtree(baseContext['base_out_path'])
    #创建目录
    os.mkdir(baseContext['base_out_path'])
    os.mkdir(baseContext['oc_out_path'])
    os.mkdir(baseContext['cpp_out_path'])
    os.mkdir(baseContext['c_out_path'])

#----------------------------------------------------生成文件信息模块end------------------------------------------------


#----------------------------------------------------生成文件总调用模块start----------------------------------------------

#生成base
def createBaseFile():
    randomName = random.choice ( ['get', 'set', 'xiniu', 'xn', 'BuYu','cc','ccb','ccui'])
    fileName = 'Base' +randomName+datetime.datetime.now().strftime('%M%S')
    #生成m文件
    # os.mknod(filename+".m")
    fp = open(baseContext['base_out_path'] + s+fileName+".m",'w')
    #生成m文件的内容 并写入
    text = autoBaseM(fileName)
    for item in text:
        fp.write(item)
    # out.write(i)
    fp.close()
    #生成h文件
    # os.mknod(filename+".h")
    fp = open(baseContext['base_out_path'] + s+fileName+".h",'w')
    #生成h文件内容并写入

    #标志logo
    logoNumber = random.randint(1,4)
    print(logoNumber)
    if logoNumber == 1:
        text = addDaHuang()
    elif logoNumber == 2:
        text = addCNM()
    elif logoNumber == 3:
        text = addCNM2()
    elif logoNumber == 4:
        text = addFZ()
    
    text = text + autoBaseH(fileName)
    for item in text:
        fp.write(item)
    fp.close()

# 自动生成base.h text
def autoBaseH(filename):

    text = ['//  '+filename+'.h\n',
    '//  '+filename+'\n',
    '//  \n',
    '//  Created by '+baseTitleNameString+' on  '+baseNowDateTimes+'.\n',
    '//  Copyright (c) 2017 maple. All rights reserved.\n',
    '//  \n',
    '\n',
    '#import <Foundation/Foundation.h>\n',
    ' @interface '+filename+' : NSObject\n',
    ' + (NSString*)find'+filename+';\n',
    ' @end\n'
    ]
    return text

# 自动生成base.m text
def autoBaseM(filename):
    global baseFileDic_OC

    text = ['//  '+filename+'.mm\n',
        '//  '+baseTitleNameString+'\n',
        '//  \n',
        '//  Created by '+baseTitleNameString+' on  '+baseNowDateTimes+'.\n',
        '//  Copyright © 2017年 Wang. All rights reserved.\n'
        '//\n',
        '\n',
        '#import \"'+filename+'.h\"\n']
    #加入 import
    for oc in baseFileNameList_OC:
        addTest = ['#import \"'+oc+'.h\"\n']
        text = text + addTest
        pass

    for c in baseFileNameList_C:
        addTest = ['#import \"'+ c + '.h\"\n']
        text = text + addTest
        pass
    
    midText = ['@implementation '+filename+'\n',
            '\n',
            '+ (NSString*)find'+filename+'\n',
            '{\n']
    text = text + midText
    #加入方法
    for oc in baseFileNameList_OC:
        codeNameList = baseFileDic_OC[oc]
        for code in codeNameList:
            addTest = ['    //title '+ oc +' '+ code +'\n',
                    '   ['+ oc +' '+code+'];\n']
            text = text + addTest
            pass
        
        pass
    for c in baseFileNameList_C:
        x = str(random.randint(1,100))
        y = str(random.randint(1,200))
        addTest = ['   '+c +'( '+x+','+y+' )'+';\n']
        text = text + addTest
        pass

    lastext = ['\n   NSString *find = @\"'+str(random.randint(10000,100000))+'\";\n',
        '   NSLog(@"%@",find);\n'
        '    return find;\n',
        '}\n',
        '@end//\n']
    text = text + lastext

    print(u'再把如下代码拷贝到项目调用的地方:')
    print('----------------------------')
    # print('#import \".'+baseContext['base_out_path']+'/'+filename+'.h\"')
    print('#import \"'+filename+'.h\"')
    print('['+filename+' find'+filename+'];')
    print('----------------------------')

    return text

#----------------------------------------------------生成文件总调用模块end------------------------------------------------


#----------------------------------------------------main------------------------------------------------
def main():

    #0.初始化 全局变量

    global ocFileRandomMin
    global ocFileRandomMax
    global cFileRandomMin
    global cFileRandomMax
    global cppFileRandomMin
    global cppFileRandomMax

    global baseFileTitle
    global baseImageTitle
    global baseNowDateTimes
    global baseFileNameList_OC
    global baseFileNameList_C
    global baseString
    global baseRadomString
    global baseContext
    global baseTitleNameString

    baseTitleNameString = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    baseString = random.choice (baseImageTitle)
    baseRadomString = ''.join(random.sample(string.ascii_letters + string.digits, 6)) #随机字符串
    baseNowDateTimes = datetime.datetime.now().strftime('%Y/%m/%d/%H/%M/%S')

    # randomFile = './File_' + ''.join(random.sample(string.ascii_letters + string.digits, 4))
    randomFile = '.'+ s +'File_' + 'newFiles' #方便测试这里写死
    randomFileOC = randomFile + s +'OC_' + ''.join(random.sample(string.ascii_letters + string.digits, 3))
    randomFileC = randomFile + s +'C_' + ''.join(random.sample(string.ascii_letters + string.digits, 3))
    randomFileCPP = randomFile + s +'CPP_' + ''.join(random.sample(string.ascii_letters + string.digits, 3))
    baseContext['base_out_path'] = randomFile
    baseContext['oc_out_path'] = randomFileOC
    baseContext['cpp_out_path'] = randomFileCPP
    baseContext['c_out_path'] = randomFileC

    #1.初始化 删除创建文件夹
    delAllFiles()

    #2.生成 oc随机文件
    for a in range(random.randint(ocFileRandomMin,ocFileRandomMax)):
        filenumber = random.choice('abcdefghrjklmnopqrstu')
        randomName = random.choice (baseFileTitle)
        filename = randomName + getOneName(filenumber + str(a))
        #生成文件.h.m
        addOneOcFile(filename)
        pass
    #3.生成 cpp随机文件
    for a in range(random.randint(cppFileRandomMin,cppFileRandomMax)):
        filenumber = random.choice('vwxyz')
        randomName = random.choice (baseFileTitle)
        filename = randomName + getOneName(filenumber + str(a))
        addOneCppFile(filename)
        pass
    
    #4.生成 c随机文件
    for a in range(random.randint(cFileRandomMin,cFileRandomMax)):
        filenumber = random.choice('qwertryu')
        randomName = random.choice (baseFileTitle)
        filename = randomName + getOneName(filenumber + str(a))
        addOneCFile(filename)
        pass

    #5.生成 Base调用文件
    createBaseFile()

    #最后
    print 'Done~~~'

if __name__ == "__main__":
    main()