from configparser import ConfigParser
import feedparser
from datetime import datetime, timedelta
import os
import codecs
import sqlite3

def main():
    config = ConfigParser()
    config.read('DailyRss.conf')
    rss_list_path = config['config']['list']
    daily_note = config['config']['daily_note']
    db_path = config['config']['sqlite']

    conn = sqlite3.connect(db_path)
    cur=conn.cursor()

    # テーブルの存在確認
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='items'")
    result = cur.fetchone()[0]
    
    if result==0:
        cur.execute("CREATE TABLE items(id STRING PRIMARY KEY)")
        conn.commit()
    
    f = open(rss_list_path, 'rt')
    rss_list = f.readlines()
    f.close()
    now = datetime.now()
    oneday = timedelta(days=1)
    yesterday = now - oneday

    title = str(yesterday.year).zfill(4) + '-' + str(yesterday.month).zfill(2) + '-' + str(yesterday.day).zfill(2)
    note_path = os.path.join(daily_note, title + ".md")
    print(note_path)
    note=codecs.open(note_path, 'a', 'utf-8')

    for rss_list_item in rss_list:
        d = feedparser.parse(rss_list_item)

        for entry in d.entries:

            published = entry.published_parsed

            if published.tm_year == yesterday.year and published.tm_mon == yesterday.month and published.tm_mday == yesterday.day:
                detail = entry.summary
                
                cur.execute('SELECT COUNT(*) FROM items WHERE id=' + "'" +  entry.id + "'")
                result = cur.fetchone()[0]
                
                if result == 0:
                    note.write("* " + entry.published + " " + detail + "\n")
                    id = str(entry.id)
                    print(id)
                    cur.execute("INSERT INTO items (id) VALUES('" + id + "')")
                    conn.commit()

    cur.close()
    note.close()
    conn.close()

if __name__ == '__main__':
    main()
