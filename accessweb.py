import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3
from gettext import gettext 
import re
from index import index

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()
  
author = index()

adrss = input('pick a book item number ')
while True:
    cur.execute('SELECT status FROM Ind WHERE item_id = ?', (adrss, ))
    compar = cur.fetchone()[0]
    if compar == 1 :
        print('item had already been retrieved, try another one')
        adrss = input('pick another book item number ')
    elif compar == 3 :
        print('failed to retrieve before, try another one')
        adrss = input('pick another book item number ')
    else: break

# filename = adrss + ".txt"


url = "https://www.gutenberg.org/files/" + adrss + "/" + adrss + "-0.txt"
try :
    print('retrieving ', url)
    html = urllib.request.urlopen(url, context=ctx).read().decode("utf-8-sig")
    cur.execute('SELECT title FROM Ind WHERE item_id = ?', (adrss, ))
    title = cur.fetchone()[0]
    cur.execute('UPDATE Ind SET status = 1 WHERE item_id = ?', (adrss, ))
    print('book title ', title, ' --- item id ', adrss, ' --- author ', author)
    text = gettext(html, title, author)
except:
    print('fail to retrieve ', url)
    print('probably wrong url')
    cur.execute('UPDATE Ind SET status = 3 WHERE item_id = ?', (adrss, ))
    conn.commit()
    quit()


text = text.lower()
print('checking if i get the text - length text ', len(text))
d = dict()
words = re.findall('[a-z0-9]+', text)
for i in words:
    if i not in d:
        d[i] = 1
    else: d[i] +=1
wlist = list()
for i in d:
    x = (i, d[i])
    wlist.append(x)
wlist.sort(key=lambda tup: tup[1], reverse=True)

commonword = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'although', 'as', 'if', 'even', 'though', 'since', 'when', 'not', 'only', 'but', 'also', 
    'instead', 'addition', 'furthermore', 'likewise', 'after', 'however']
i = int((len(wlist)) / 10)
favwords = wlist[i:(i+100)]
print('100 words in top 10%: ', favwords)

countword = 0
countmiddleword = 0
for x in wlist:
    if x in commonword : continue
    elif x not in commonword :
        cur.execute('INSERT OR IGNORE INTO Words (word) VALUES ( ? ) ', (x[0], ))
        cur.execute('SELECT id FROM Words WHERE word = ? ', (x[0], ))
        word_id = cur.fetchone()[0]
        countword = countword + 1
        if x in favwords:
            cur.execute('''INSERT OR IGNORE INTO Frequency (item_id, word_id, freq) VALUES ( ?, ?, ? ) ''', (adrss, word_id, x[1] ))
            countmiddleword = countmiddleword + 1
conn.commit()  
print('there are ', countword, ' words in the text')
print('there are ', countmiddleword, ' words added to Favorite Words list for this book')


