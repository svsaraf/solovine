from django.contrib import admin
import feeds.models

# Register your models here.
admin.site.register(feeds.models.RSSFeed)
admin.site.register(feeds.models.RSSEntry)