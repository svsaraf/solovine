from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
# Create your models here.
CIRCLE_TYPES = (
    ('a', 'alpha'), 
    ('b', 'bravo'), 
    ('c', 'charlie'), 
    ('d', 'delta'),
    ('e', 'echo'), 
    ('f', 'foxtrot'), 
    ('g', 'golf'),
    ('h', 'hotel'), 
    ('i', 'india'), 
    ('j', 'juliett'),
)

class Contact(models.Model):
    sender = models.ForeignKey(User, on_delete='cascade', related_name='sender')
    receiver = models.ForeignKey(User, on_delete='cascade', related_name='receiver')
    accepted = models.BooleanField()

    def __str__(self):
        return self.sender.username + " send to " + self.receiver.username 

class CircleEntry(models.Model):
    contact = models.ForeignKey(Contact, on_delete='cascade')
    circle = models.CharField(
        max_length=1, choices=CIRCLE_TYPES, default='a',
    )

    def __str__(self):
        return self.contact.sender.username + ": " + self.contact.receiver.username + " in " + self.circle

class PostContact(models.Model):
    post = models.ForeignKey(Post, on_delete='cascade')
    contact = models.ForeignKey(Contact, on_delete='cascade')

    def __str__(self):
        return self.post.title + " sent to " + self.contact.receiver.username