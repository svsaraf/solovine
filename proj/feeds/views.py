from django.shortcuts import render
from django.http import HttpResponse
from feeds.models import RSSFeed, RSSEntry
import feedparser
from time import mktime
from datetime import datetime
# Create your views here.

def feeds(request):
    entries = RSSEntry.objects.all().order_by('feed')
    d = {}
    for item in entries:
        if item.feed.title in d:
            d[item.feed.title].append(item)
        else:
            d[item.feed.title] = []
            d[item.feed.title].append(item)
    print(d)
    context = {'feeds': d}
    return render(request, 'feeds/feeds.html', context)

def populatefeeds():
    feeds = RSSFeed.objects.all()
    for feed in feeds:
        obj = feedparser.parse(feed.source, modified=feed.modified)
        if obj.status == 304:
            pass
            # RSS feed is already up to date
        else:
            try:
                feed.etag = obj.etag
            except AttributeError:
                pass
            try:
                feed.modified = obj.modified
            except AttributeError:
                pass
            feed.save()
            for article in obj['entries']:
                a, created = RSSEntry.objects.get_or_create(feed=feed,
                             title=article.title,
                             link=article.link,
                             author=article.author,
                             published=datetime.fromtimestamp(mktime(article.published_parsed)),
                             summary=article.summary)
    return