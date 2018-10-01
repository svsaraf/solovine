from django.shortcuts import render
from django.http import HttpResponse
from feeds.models import RSSFeed, RSSEntry
import feedparser
from time import mktime
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def feeds(request):
    entries = RSSEntry.objects.all().order_by('feed', '-published')
    d = {}
    for item in entries:
        if item.feed.title in d:
            if len(d[item.feed.title]) < 20:
                d[item.feed.title].append(item)
        else:
            d[item.feed.title] = []
            d[item.feed.title].append(item)
    context = {'feeds': d}
    return render(request, 'feeds/feeds.html', context)

@login_required(login_url='/login')
def getfeedadd(request):
    context = {}
    return render(request, 'feeds/addfeed.html', context)

@login_required(login_url='/login')
def addfeed(request):
    context = {}
    if request.method == 'POST':
        feedlink = request.POST.get('feedlink')
        obj = feedparser.parse(feedlink)
        if obj.bozo == 0 and obj.status == 200:
            etag = ''
            modified = ''
            try:
                etag = obj.feed.etag
            except AttributeError:
                pass
            try:
                modified = obj.feed.modified
            except AttributeError:
                pass
            r, created = RSSFeed.objects.update_or_create(source=obj.feed.title_detail.base, title=obj.feed.title, defaults={'etag': etag, 'modified': modified})
            context['message'] = 'Thanks!'
            populatefeeds()
            return render(request, 'feeds/message.html', context)
        else:
            context['message'] = 'Bad RSS feed.'
            return render(request, 'feeds/message.html', context)
    context['message'] = 'Not sure waht happened?'
    return render(request, 'feeds/message.html', context)


def populatefeeds():
    feeds = RSSFeed.objects.all()
    for feed in feeds:
        #print('Starting: ' + feed.source)
        obj = feedparser.parse(feed.source, modified=feed.modified)
        if obj.status == 304:
            pass
            # RSS feed is already up to date
        elif obj.feed is None: 
            pass
            # invalid feed
        elif obj.status == 200:
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
                #print('Adding entries...')
                try:
                    a, created = RSSEntry.objects.update_or_create(feed=feed,
                                 title=article.title,
                                 defaults = {'link': article.link,
                                            'published': datetime.fromtimestamp(mktime(article.published_parsed)),
                                            'summary': article.summary}
                                )
                except:
                    #print('failed')
                    #xml sometimes doesn't have all values. Ignore them for now.
                    pass
    return    
