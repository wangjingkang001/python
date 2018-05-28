#! /usr/bin/python
# -*- coding: UTF-8 -*-

# author : liqiang
# desc : 自动生成辣鸡代码

# 逻辑重理
# 此脚本功能有
# 1.生成文件（lua，c++）
# 2.混入方法（lua）
# 3.混入注释（lua，oc，c++）
# 4.修改打包配置
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
from os.path import join, getsize
s = os.sep #多平台 路径分割符号是'\',在Linux上是‘/’

# 模拟生成文件目录的源目录
cplus_get_dir_path = '/Users/li/mypro/xfront/Resources'
lua_get_dir_path = '/Users/li/mypro/xfront/Resources'
cplus_born_path = '../../../../XnFramework/cocos/quick-3.3/quick/lib/XnGameSrc'
lua_born_path = '../../../../scirptdecode/main/game'
copyfilelist = ['luaFramework','main','package/BuYu/res','package/BuYu/src']
# 生成单个c++文件内的方法数量
cplusFuncConut = 1

context = {
    'key' : 'xiniu',
    'add_func_num' : 10,

    'lua_in_path' : '../../../..',
    'lua_out_path' : '../../../../scirptdecode',

    'lua_get_dir_path':lua_get_dir_path,
    'lua_born_path':lua_born_path,

    'cplus_get_dir_path':cplus_get_dir_path,
    'cplus_born_path':cplus_born_path,

    'oc_in_path':'',
    'oc_out_path':'./',

    'isaddfunc':True,    #加混淆开关
    'isaddfile':True,    #加文件开关
    'isadddesc':True,     #加注释开关   c++添加没有用   会被过滤掉
    'isaddfile_lua':True,

    'wxAppID':"wxacfcf61a237d3658",
    'version':'2.15',
    'config_list':{
        "UnionID": 101,
        "ChildUnionID": 1143,
        "KindID": 404,
        "ChannelID": 0,
        "AppID": "80252127002"
    }
}



add_file_count = 0
add_function_count = 0
add_desc_count = 0

# 配置文件解释
        # "key" : "jiebabuyuxiniubuyu",
        # "add_func_num" :10,
        # "lua_in_path":"../../../../scirptdecode/main/res/client_config",
        # "lua_out_path":"../../../../scirptdecode",
        # "config_list":{
        #     "UnionID": 101,
        #     "ChildUnionID": 1143,
        #     "KindID": 404,
        #     "ChannelID": 0,
        #     "AppID": "80252127002"
        # },
        # "wxAppID":"wxacfcf61a237d3658",
        # "version":"2.15",


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
    m1.update(context['key']+filename.split(s)[-1])   #更新一次 改变一次  filename格式为  文件名 + 方法行号 + 方法当前方法行数
    # print filename.split("/")[-1]
    text =  m1.hexdigest()
    text = text[0:7]
    # return string.join(random.sample(m1.hexdigest(),random.randint(4,10)),"")
    # print text,context['key']+filename.split(s)[-1]
    return str(text)
        # names[asciis] = chr(asciis)
# 得到字段头   为了好查找   暂时先只加一个
def getHeadName():
    return random.choice ( ['get'])
#----------------------------------------------------通用模块end------------------------------------------------



#----------------------------------------------------生成文件信息模块start------------------------------------------------
# 生成一个图形注释 适用于.h .cpp  .mm   .m   .hpp  
def addDescimg():
    text = [
    '\n/**                                                                          佛祖保佑必过包',
    '\n*          .,:,,,                                        .::,,,::.          佛祖保佑必过包',
    '\n*        .::::,,;;,                                  .,;;:,,....:i:         佛祖保佑必过包',
    '\n*        :i,.::::,;i:.      ....,,:::::::::,....   .;i:,.  ......;i.        佛祖保佑必过包',
    '\n*        :;..:::;::::i;,,:::;:,,,,,,,,,,..,.,,:::iri:. .,:irsr:,.;i.        佛祖保佑必过包',
    '\n*        ;;..,::::;;;;ri,,,.                    ..,,:;s1s1ssrr;,.;r,        佛祖保佑必过包',
    '\n*        :;. ,::;ii;:,     . ...................     .;iirri;;;,,;i,        佛祖保佑必过包',
    '\n*        ,i. .;ri:.   ... ............................  .,,:;:,,,;i:        佛祖保佑必过包',
    '\n*        :s,.;r:... ....................................... .::;::s;        佛祖保佑必过包',
    '\n*        ,1r::. .............,,,.,,:,,........................,;iir;        佛祖保佑必过包',
    '\n*        ,s;...........     ..::.,;:,,.          ...............,;1s        佛祖保佑必过包',
    '\n*       :i,..,.              .,:,,::,.          .......... .......;1,       佛祖保佑必过包',
    '\n*      ir,....:rrssr;:,       ,,.,::.     .r5S9989398G95hr;. ....,.:s,      佛祖保佑必过包',
    '\n*     ;r,..,s9855513XHAG3i   .,,,,,,,.  ,S931,.,,.;s;s&BHHA8s.,..,..:r:     佛祖保佑必过包',
    '\n*    :r;..rGGh,  :SAG;;G@BS:.,,,,,,,,,.r83:      hHH1sXMBHHHM3..,,,,.ir.    佛祖保佑必过包',
    '\n*   ,si,.1GS,   sBMAAX&MBMB5,,,,,,:,,.:&8       3@HXHBMBHBBH#X,.,,,,,,rr    佛祖保佑必过包',
    '\n*   ;1:,,SH:   .A@&&B#&8H#BS,,,,,,,,,.,5XS,     3@MHABM&59M#As..,,,,:,is,   佛祖保佑必过包',
    '\n*  .rr,,,;9&1   hBHHBB&8AMGr,,,,,,,,,,,:h&&9s;   r9&BMHBHMB9:  . .,,,,;ri.  佛祖保佑必过包',
    '\n*  :1:....:5&XSi;r8BMBHHA9r:,......,,,,:ii19GG88899XHHH&GSr.      ...,:rs.  佛祖保佑必过包',
    '\n*  ;s.     .:sS8G8GG889hi.        ....,,:;:,.:irssrriii:,.        ...,,i1,  佛祖保佑必过包',
    '\n*  ;1,         ..,....,,isssi;,        .,,.                      ....,.i1,  佛祖保佑必过包',
    '\n*  ;h:               i9HHBMBBHAX9:         .                     ...,,,rs,  佛祖保佑必过包',
    '\n*  ,1i..            :A#MBBBBMHB##s                             ....,,,;si.  佛祖保佑必过包',
    '\n*  .r1,..        ,..;3BMBBBHBB#Bh.     ..                    ....,,,,,i1;   佛祖保佑必过包',
    '\n*   :h;..       .,..;,1XBMMMMBXs,.,, .. :: ,.               ....,,,,,,ss.   佛祖保佑必过包',
    '\n*    ih: ..    .;;;, ;;:s58A3i,..    ,. ,.:,,.             ...,,,,,:,s1,    佛祖保佑必过包',
    '\n*    .s1,....   .,;sh,  ,iSAXs;.    ,.  ,,.i85            ...,,,,,,:i1;     佛祖保佑必过包',
    '\n*     .rh: ...     rXG9XBBM#M#MHAX3hss13&&HHXr         .....,,,,,,,ih;      佛祖保佑必过包',
    '\n*      .s5: .....    i598X&&A&AAAAAA&XG851r:       ........,,,,:,,sh;       佛祖保佑必过包',
    '\n*      . ihr, ...  .         ..                    ........,,,,,;11:.       佛祖保佑必过包',
    '\n*         ,s1i. ...  ..,,,..,,,.,,.,,.,..       ........,,.,,.;s5i.         佛祖保佑必过包',
    '\n*          .:s1r,......................       ..............;shs,           佛祖保佑必过包',
    '\n*          . .:shr:.  ....                 ..............,ishs.             佛祖保佑必过包',
    '\n*              .,issr;,... ...........................,is1s;.               佛祖保佑必过包',
    '\n*                 .,is1si;:,....................,:;ir1sr;,                  佛祖保佑必过包',
    '\n*                    ..:isssssrrii;::::::;;iirsssssr;:..                    佛祖保佑必过包',
    '\n*                         .,::iiirsssssssssrri;;:.                      佛祖保佑必过包',
    '\n*/ //佛祖保佑必过包\n//佛祖保佑必过包\n//佛祖保佑必过包'
    ]
    return text
# 自动生成oc.h文件
def autoTexth(filename):
    global add_file_count
    add_file_count = add_file_count + 1
    text = ['//  '+filename+'.h\n',
    '//  '+filename+'\n',
    '//  \n',
    '//  Created By liqiang on  2017/8/16.\n',
    '//  Copyright (c) 2013 maple. All rights reserved.\n',
    '//  \n',
    '\n',
    '#import <Foundation/Foundation.h>\n',
    ' @interface '+filename+' : NSObject\n',
    ' + (NSString*)UDID;\n',
    ' @end\n'
    ]
    return text

# 自动生成oc.m文件
def autoTextM(filename):
    global add_file_count
    add_file_count = add_file_count + 1
    text = [
        '//  '+filename+'.m\n',
        '//  xiniu\n',
        '//  \n',
        '//  Created by liqiang on  2017/8/16.\n',
        '//  Copyright © 2017年 Li. All rights reserved.\n'
        '//\n',
        '\n',
        '#import \"'+filename+'.h\"\n',
        '@implementation '+filename+'\n',
        '\n',
        '+ (NSString*)UDID\n',
        '{\n',
        '   NSString *udid = @\"'+str(random.randint(10000,10000000))+'\";\n',
        '    return udid;\n',
        '}\n',
        '@end//\n'
    ]
    return text

# 生成一个c++方法  加上获取当前不定的时间  防止被编译器过滤
def autoTextCpluscpp(filename,fn):

    functionname0 = 'xn' + getOneName(filename+'0')
    functionname1 = 'xn' + getOneName(filename+'1')
    functionname2 = 'xn' + getOneName(filename+'2')
    functionname3 = 'xn' + getOneName(filename+'3')
    functionname5 = 'xn' + getOneName(filename+'4')
    functionname4 = getHeadName()+getOneName(filename+'4')
    text = [

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
# 生成一个C++  extern 声明
def autoTextCplusH(filename,fn):
    text = [
        '   extern bool GetIs'+filename+'();\n\n'
    ]
    return text
# 添加lua 辣鸡方法
def autoTextLua(filename):
    # print filename+'1\n'
    global add_function_count
    add_function_count = add_function_count + 1
    functionname1 = 'xn' + getOneName(filename+'1')
    functionname2 = 'xn' + getOneName(filename+'2')
    functionname3 = 'xn' + getOneName(filename+'3')
    functionname4 = getHeadName()+getOneName(filename+'4')
    text = [
        '\nlocal function '+functionname4+'()\n',
        '   local '+functionname1 + '=' + '123'+'\n',
        '   local '+functionname2 + '=' + '456'+'\n',
        '   local '+functionname3+'='+functionname1+'+'+functionname2+'\n',
        '   return '+functionname3+'\n',
        'end\n\n'
    ]
    # print string.join(text)
    return string.join(text)
# 添加lua 辣鸡文件context
def autoTextLuafile(filename,fn):
    # print filename+'1\n'
    global add_file_count
    add_file_count = add_file_count + 1
    functionname0 = 'xn' + getOneName(filename+'0')
    functionname1 = 'xn' + getOneName(filename+'1')
    functionname2 = 'xn' + getOneName(filename+'2')
    functionname3 = 'xn' + getOneName(filename+'3')
    functionname4 = getHeadName()+getOneName(filename+'4')
    text = [
        'local ' + functionname0 + ' = {}\n',
        '\nlocal function '+functionname4+'()\n',
        '   local '+functionname1 + '=' + '123'+'\n',
        '   local '+functionname2 + '=' + '456'+'\n',
        '   local '+functionname3+'='+functionname1+'+'+functionname2+'\n',
        '   return '+functionname3+'\n',
        'end\n\n',
        'return ' + functionname0 + '\n'
    ]
    # print string.join(text)
    return string.join(text)
# 生成OC文件
def addOneOcFile(filenumber):
    #生成文件名
    filename = 'test' + getOneName(filenumber)

    functionname = random.choice ( ['get', 'set', 'xiniu', 'xn', 'BuYu','cc','ccb','ccui'])+filename
    #生成m文件
    # os.mknod(filename+".m")
    fp = open(context['oc_out_path'] + s+filename+".m",'w')
    #生成m文件的内容 并写入
    text = autoTextM(filename)
    for item in text:
        fp.write(item)

    # out.write(i)
    fp.close()

    #生成h文件
    # os.mknod(filename+".h")
    if os.path.exists(context['oc_out_path']) :
        shutil.rmtree(context['oc_out_path'])
    os.mkdir(context['oc_out_path'])
    fp = open(context['oc_out_path'] + s+filename+".h",'w')
    #生成h文件内容并写入
    text = autoTexth(filename)
    for item in text:
        fp.write(item)

    fp.close()

#----------------------------------------------------生成文件信息模块end------------------------------------------------



#----------------------------------------------------main------------------------------------------------
def main():
    # 1.生成文件（lua，c++）
    # 2.混入方法（lua）
    # 3.混入注释（lua，oc，c++）
    # 4.修改打包配置
    print '感谢使用'

if __name__ == "__main__":
    main()