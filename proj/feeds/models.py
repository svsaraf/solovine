from django.db import models

# Create your models here.
class RSSFeed(models.Model):
    source = models.URLField()
    title = models.CharField(max_length=100)
    etag = models.CharField(max_length=50, blank=True)
    modified = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.source + ": " + self.modified

class RSSEntry(models.Model):
    feed = models.ForeignKey(RSSFeed, on_delete='cascade', blank=True, null=True)
    title = models.CharField(max_length=200)
    link = models.URLField()
    author = models.CharField(max_length=200)
    published = models.DateTimeField()
    summary = models.TextField()

    def __str__(self):
        return self.title + " published by " + self.author
