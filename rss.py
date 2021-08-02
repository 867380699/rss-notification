import os
import time
import feedparser
from pathlib import Path

feedUri = 'http://127.0.0.1:1200/readhub/category/topic'
filepath = str(Path.home()) + '/readhub/txt/'

newFeeds = feedparser.parse(feedUri)

summary = [{'title': f.title} for f in newFeeds.entries]

h = int(time.strftime('%H'))
h_text = '早' if h < 12 else '午' if h < 18 else '晚'
c_now = time.strftime('%Y年%m月%d日')

filename = "Readhub-%s%s.txt" % (c_now.replace(' ', ''), h_text)

c_file = open(filepath + filename, 'w')

c_file.write('%s %s\n\n' % (c_now, h_text))
for s in summary:
    c_file.write('%s\n\n' % s['title'])

c_file.close()

os.system(f'termux-notification -t {filename.split(".")[0]} --action "termux-share -d {filepath}{filename}"')
