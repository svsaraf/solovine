from django.contrib import admin
import posts.models

# Register your models here.
admin.site.register(posts.models.Post)
admin.site.register(posts.models.Comment)