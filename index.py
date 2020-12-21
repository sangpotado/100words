import re
import sqlite3

def index():
    conn = sqlite3.connect('index.sqlite')
    cur = conn.cursor()

    # cur.execute('''DROP TABLE Ind''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Ind
        (item_id TEXT, 
        author_id INTERGER, 
        title TEXT UNIQUE,
        status INTEGER)
        ''')
    
    cur.executescript('''CREATE TABLE IF NOT EXISTS Status
        (status_id INTEGER UNIQUE,
        status TEXT UNIQUE);
        
        INSERT OR IGNORE INTO Status (status_id, status) VALUES (1, 'Retrieved');
        INSERT OR IGNORE INTO Status (status_id, status) VALUES (2, 'not yet retrieved');
        INSERT OR IGNORE INTO Status (status_id, status) VALUES (3, 'fail to retrieve')
        ''');
     
    cur.execute('''CREATE TABLE IF NOT EXISTS Author
        (id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
        name TEXT UNIQUE)''');
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Frequency
        (item_id TEXT,
        word_id INTEGER,
        freq INTEGER)
        ''');
    cur.execute('''CREATE TABLE IF NOT EXISTS Words
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        word TEXT UNIQUE)
        ''')

    fh = open('gutindex.txt', encoding="utf8")
    author = input("enter author's name/first then last name ")

    blist = list()
    for line in fh:
        if (author.lower() in line.lower()) and ('audio' not in line.lower()):
            t = re.findall('([a-zA-Z].*), by' , line)
            if len(t) < 1 : continue
            else: title = t[0]
            itn = re.findall('\s\s\s([0-9].+)' , line)
            if len(itn) < 1 : continue
            else: itemnum = itn[0]          
            cur.execute('''INSERT OR IGNORE INTO Author (name)
                VALUES ( ? )''', (author, ) )
            cur.execute('SELECT id FROM Author WHERE name = ? ', (author, ))
            author_id = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO Ind (item_id, author_id, title)
                VALUES (?, ?, ? )''', (itemnum, author_id, title))
            cur.execute('UPDATE Ind SET status=2 WHERE status IS NULL')
            cur.execute('SELECT status FROM Ind WHERE item_id = ?', (itemnum, ))
            try: 
                stat = cur.fetchone()[0]
                print(title, itemnum, stat)
            except: print(title, itemnum)
    conn.commit()
    return author
      