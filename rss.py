import os
import time
from pathlib import Path
import feedparser
from ebooklib import epub

feedUri = 'http://127.0.0.1:1200/readhub/category/topic'
filepath = str(Path.home()) + '/readhub/txt/'

newFeeds = feedparser.parse(feedUri)

summary = [{'title': f.title} for f in newFeeds.entries]

h = int(time.strftime('%H'))
h_text = '早' if h < 12 else '午' if h < 18 else '晚'
c_now = time.strftime('%Y年%m月%d日')

title = f'{c_now} {h_text}'

filename = f"Readhub-{title.replace(' ', '')}.epub"

book = epub.EpubBook()

book.set_title(title)
book.set_language('zh-CN')
book.add_author('readhub')
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style = """
BODY { text-align: justify; }
h1,h2 { margin-bottom: 1em }
"""

default_css = epub.EpubItem(uid='style_default', file_name="style/default.css", media_type="text/css", content=style)

c1 = epub.EpubHtml(title="feed", file_name="feed.xhtml")
c1.set_language('zh-CN')
c1.add_item(default_css)

c1.content=f'<h1>{title}</h1>'

for s in summary:
    c1.content += f'<h2>{s["title"]}</h2>'

book.add_item(c1)
book.add_item(default_css)
book.spine = ['nav', c1]
book.toc = ((epub.Link('feed.xhtml', f'{title}', 'feed'),))

epub.write_epub(f'{filepath}{filename}', book, {})

os.system(f'termux-notification -t {filename.split(".")[0]} --action "termux-share -d {filepath}{filename}"')
