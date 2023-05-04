# DailyRSS

RSSをデイリーでMarkdownに落とします。
Obsidianとの併用が想定されています。
設定はDailyRSS.confに記述します。
以下のフォーマットになります。
```
[config]
list=lists/default.list
daily_note=<RSSのリストのパス>
sqlite=lists/rss.db
```

sqliteは同一エントリを多重処理するのを防ぐために用いられます。

## コマンドライン引数

python DailyRSS.py --date yyyy-MM-dd

--dateオプションをつけると任意の日付を対象にできます。
