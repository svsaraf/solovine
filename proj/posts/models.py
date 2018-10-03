from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete='cascade')
    title = models.CharField(max_length=50)
    text = models.TextField()
    link = models.URLField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name + ": " + self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete='cascade')
    post = models.ForeignKey(Post, on_delete='cascade')
    parentcomment = models.ForeignKey('self', null=True, blank=True, on_delete='cascade')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name + ": " + self.text

    def get_children(self):
        return Comment.objects.filter(parentcomment=self)