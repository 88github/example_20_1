#coding=utf-8

'''
    20170705
    why
'''

import cgi, os, sys
from urllib import quote_plus
from string import capwords

headerhtml = 'Content-Type:text/html\n\n'
url = 'example_20_1.py'

errorhtml = '''
    <html>
    <head><title>Friend CGI Demo</title></head>
    <body>
    <h3>Error:<i>%s</i></h3>
    <form><input type="button" value="Back" onclick="window.history.back()"></form>
    </body>
    </html>
'''

def showError(error_str):
    print headerhtml + errorhtml % (error_str)

formhtml = '''<html><head><title>Title</title>
</head>
<body>
<H3>Friends list for:<I>%s</I></H3>
<form ACTION="%s">
    <B>Enter your Name:</B>
    <INPUT type="hidden" name="action" value="edit">
    <INPUT type="text" name="person" value="%s" size="15">
    <B>how many friends do you have?</B>
    %s
    <input type="submit">
</form>
</body>
</html>
'''

radiohtml = '<input type="radio" name="howmany" value="%s" %s> %s\n'

def showForm(who, howmany):
    friends = ''
    for i in [0, 10, 25, 50, 100]:
        checked = ''
        if str(i)== howmany:
            checked = 'CHECKED'
        friends = friends + radiohtml % (str(i), checked, str(i))
    print headerhtml + formhtml % (who, url, who, friends)

resulthtml = '''
    <html>
    <head><title>Friend CGI Demo</title></head>
    <body>
    <h3>friends list for:<i>%s</i></h3>
    your name is:<b>%s</b><p>
    your have <b>%s</b> friends.
    <p>Click<a href="%s">here</a>To edit your data again.
    <p>Click<a href="%s">Look</a>Look Other.
    </body>
    </html>
'''

def showResult(who, howmany):
    newUrl = url + '?action=reedit&person=%s&howmany=%s'  % (quote_plus(who), howmany) #quote_plus编码
    LookUrl = url + '?action=look' # quote_plus编码
    print headerhtml + resulthtml % (who, who, howmany, newUrl, LookUrl)

hisHtml = '''
    <html>
    <head><title>History information</title></head>
    <body>
    <form><input type="button" value="Back" onclick="window.history.back()"></form>
    <input type=button value=刷新 onclick="window.location.reload()">
    <p>Click<a href="%s">Clear</a>Clear the info.
    <h3>info:</h3>
    <b>%s</b>
    </body>
    </html>
'''

def showHisHtml(data):
    clearUrl = url + '?action=clear'
    print headerhtml + hisHtml % (clearUrl, data)

def SaveInfo(who, howmany):
    bookData = ""
    bookDataList = (u"name:%s" % who, u" has %s " % howmany + u"friend.\n")
    bookData = bookData.join(bookDataList)
    file_object = open('D:/it/Python/HTTP_Client/cgi-bin/book.txt', 'a')
    file_object.write(bookData.decode("gb2312").encode("utf-8"))
    file_object.close()

def ReadInfo():
    bookDataN = ""
    file_object = open('D:/it/Python/HTTP_Client/cgi-bin/book.txt', 'r')
    Flag = True
    while Flag:
        bookData = file_object.readline()
        if not bookData:
            Flag = False
        else:
            bookDataN += bookData + '<br>'
    file_object.close()
    return bookDataN

clearHtml = '''
    <html>
    <head><title>Clear History information</title></head>
    <body>
    <form><input type="button" value="Back" onclick="window.history.back()"></form>
    <h3>历史记录清空完成！请返回</h3>
    </body>
    </html>
'''

def clearHisInfo():
    file_object = open('D:/it/Python/HTTP_Client/cgi-bin/book.txt', 'w+')
    file_object.truncate()
    file_object.close()
    print headerhtml + clearHtml

def process():
    error = ''
    form = cgi.FieldStorage()

    if form.has_key('person'):  #has_key() 函数用于判断键是否存在于字典中，如果键在字典dict里返回true，否则返回false.
        who = capwords(form['person'].value)    #将传进来的字符串的首字母自动大写
    else:
        who = 'NEW USER'

    if form.has_key('howmany'):
        howmany = form['howmany'].value
    else:
        if form.has_key('action') and form['action'].value == 'edit':
            error = 'please select number of friends.'
        else:
            howmany = 0

    if not error:
        if form.has_key('action') and form['action'].value == 'edit':
            SaveInfo(who, howmany)
            showResult(who, howmany)
        if form.has_key('action') and form['action'].value == 'look':
            ReadData = ReadInfo()
            showHisHtml(ReadData)
        if form.has_key('action') and form['action'].value == 'clear':
            clearHisInfo()
        if form.has_key('action') and form['action'].value == 'reedit':
            showForm(who, howmany)
        if not form.has_key('action'):
            showForm(who, howmany)
    else:
        showError(error)

if __name__ == '__main__':
    process()