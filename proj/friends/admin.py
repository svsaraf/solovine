from django.contrib import admin
import friends.models

# Register your models here.
admin.site.register(friends.models.Contact)
admin.site.register(friends.models.CircleEntry)
admin.site.register(friends.models.PostContact)