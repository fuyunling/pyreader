# -*- coding: utf-8 -*-
import pyttsx3
from os import path
from os import listdir

def preparetext(lines):
    text = ''.join(lines)

    signs = ['。', '！', '？', '”', '：']
    for s in signs:
        text = text.replace(s, s + '\n')
    for s in signs[-2:0:-1]:
        text = text.replace('\n' + s, s)
    text = text.replace('\n\n', '\n')

    return text.splitlines()

def readlog(logf):
    log = ''
    with open(logf, 'r') as f:
        log = f.read()
    return (1, '') if log.find(' -- ') < 0 else log.split(' -- ')

def writelog(log, idx, line):
    with open(log, 'w') as f:
        f.write('%d -- %s' % (idx, line))

def findchapters(lines, ch):
    chapters = {}
    i, ln = 1, 0    # dict key start from 1 while line index start from 0
    for l in lines:
        if l.startswith(ch):
            chapters[i] = [ln, l]
            i = i + 1
        ln = ln + 1
    return chapters

def findcontent(lines, content):
    linefinded = {}
    i, ln = 1, 0    # dict key start from 1 while line index start from 0
    for l in lines:
        if (l.find(content) >= 0):
            linefinded[i] = [ln, l]
            i = i + 1
        ln = ln + 1
    return linefinded

def pickone(linefinded, infotext):
    print ('\n正在定位，请耐心等待…… \n')
    if len(linefinded) > 1:
        print('\n找到以下%s：%s' % 
            (infotext, 
             ''.join(map(lambda k: '\n\n\t%d. [行号：%d][%s]' % 
                         (k, linefinded[k][0], linefinded[k][1].strip()), linefinded))))
        i = int(input('\n选择哪个 > '))
        print('\n已选择：\n\t%s' % linefinded[i][1])
        i = linefinded[i][0]
    elif len(linefinded) == 1:
        print(linefinded)
        i = linefinded[1][0]    # key starts from 1
    else: 
        print('\n找不到指定%s……' % infotext)
        i = -1
    return i

def settingengine(reader, rate):
    print ('\t1. 选择语音角色\n\n' +
           '\t2. 设置语音速度\n')
    s = int(input('其它输入将结束设置 > '))
    if (1 == s):
        print (('可选语音角色：\n%s\n\n' % sign) + 
               '\t1.  HUIHUI   -  中文 女声\n' +
               '\t2.  HONGYU   -  中文 女声\n' +
               '\t3.  YAOYAO   -  中文 女声\n' +
               '\t4. KANGKANG  -  中文 男声\n' +
               '\t5.   ZIRA    -  英语 女声\n\n')
        si = int(input('其它输入将结束操作 > '))
        readers = ['HUIHUI', 'HONGYU', 'YAOYAO', 'KANGKANG', 'ZIRA']
        reader = readers[si - 1]
    elif (2 == s):
        rate = int(input('更改为 > '))
    else:
        exit
    return (reader, rate)

#########################################################################################
sign = '=' * 100
files = listdir('.')
novel = []
for f in files:
    if f.endswith('.txt'):
        novel.append(path.splitext(path.basename(f))[0])
if [] == novel:
    print('没有找到可以朗读的书籍或任何txt文本')
    exit()


recent = 'recent.log'
renn = ''
goon = True
while(goon):
    print('\n找到以下书籍：\n%s\n%s\n%s' % 
        (sign, ''.join(map(lambda n: '\n\t%d. %s\n' % (novel.index(n) + 1, n), novel)), sign))

    select = int(input('想听哪本书？(输入序号即可，输入“0”朗读最近的书籍，其它输入或序号超范围都将终止程序 :-P) > '))
    goon = False
    if 0 == select:
        try:
            idx, renn = readlog(recent)
        except:
            print('\n\n\n！！！找不到上次朗读的书籍，请重新选择！！！\n\n')
            goon = True
    else:
        renn = ''

nn = novel[select - 1] if renn is '' else renn
print('\n已选择：\n%s\n\n\t%s\n\n%s' % (sign, nn, sign))

fn = path.extsep.join([nn, 'txt'])
logfile = path.extsep.join([nn, 'log'])
lines = []
try:
    with open(fn, 'r') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()


sapi_voices = {
    'HUIHUI' : r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0',
    'HONGYU' : r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HONGYU_11.0',
    'YAOYAO' : r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_YAOYAO_11.0]',
    'KANGKANG' : r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_KANGKANG_11.0',
    'ZIRA' : r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
}
reader = 'KANGKANG'
rate = 174
engine = pyttsx3.init()
engine.setProperty('rate', rate)
engine.setProperty('voice', sapi_voices[reader])

idx, sub = 1, ''
if path.exists(logfile):
    idx, sub = readlog(logfile)
else:
    writelog(logfile, idx, sub)
i = int(idx)

goon = True
while (goon):
    goon = False
    print(('已加载书籍，现在你可以：\n%s\n\n' % sign) +
          ('\t1. 继续上次朗读（按行号定位[%s]）\n\n' % idx) + 
          ('\t2. 继续上次朗读（按文本定位）\n\n\t%s\n' % sub) + 
           '\t3. 从指定行号开始朗读\n\n' +
           '\t4. 从指定章节开始朗读\n\n' +
           '\t5. 从指定的文本开始朗读\n\n' +
           '\t6. 从头开始朗读\n\n' +
          ('\t7. 朗读设置\n\n%s\n' % sign) +
           '其它输入将终止程序\n')
    select = eval(input('请选择操作 > ')) if renn is '' else 1
    if (1 == select):
        i = int(idx)
    elif (2 == select):
        i = lines.index(sub)
    elif (3 == select):
        i = int(input('\n请输入行号 > '))
    elif (4 == select):
        i = int(input('\n请输入章节序号 > '))
        chs = findchapters(lines, '第%d章' % i)
        i = pickone(chs, '章节')
    elif (5 == select):
        content = input('\n请输入要定位的文本 > ')
        linefinded = findcontent(lines, content)
        i = pickone(linefinded, '文本')
    elif (6 == select):
        i = 0
    elif (7 == select):
        print ('\n当前语音角色：%s；当前语音速度：%d\n%s\n' % (reader, rate, sign))
        reader, rate = settingengine(reader, rate)
        engine.setProperty('voice', sapi_voices[reader])
        engine.setProperty('rate', rate)
        print ('\n当前语音角色：%s；当前语音速度：%d' % (reader, rate))
        goon = True
    else:
        i = -1

    if (-1 == i):
        exit()
    print(sign)
    print()

for l in lines[i :]:
    if not l.isspace():
        print('[%d]%s' % (i, l))
        engine.say(l)
        engine.runAndWait()
        writelog(logfile, i, l)
        writelog(recent, 0, nn)
    i = i + 1

