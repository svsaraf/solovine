from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.text import slugify
import math
import random
from django.db.models import Q
from friends.models import Contact
# Create your views here.

def public_posts(request):
    context = {}
    context['posts'] = Post.objects.filter(public=True).annotate(num_comments=Count('comment')).all().order_by('-timestamp')[:20]
    context['public'] = True
    return render(request, 'posts/posts.html', context)

def public_post(request, title):
    context = {}
    context['posts'] = Post.objects.filter(public=True).filter(slug=title).annotate(num_comments=Count('comment'))
    context['comments'] = Comment.objects.filter(post=Post.objects.filter(public=True).filter(slug=title)[0]).filter(parentcomment=None).order_by('-timestamp')
    context['public'] = True
    return render(request, 'posts/postdetail.html', context)

@login_required(login_url='/login')
def posts(request):
    context = {}
    requestuser = request.user
    # note that this does a where x = a or x = b style query and is thus less efficient than an inner join. 
    exp = Q(author=requestuser)
    for author in Contact.objects.filter(sender=requestuser, accepted=True).values_list('receiver', flat=True):
        exp = exp | Q(author=author)
    context['posts'] = Post.objects.filter(exp).annotate(num_comments=Count('comment')).all().order_by('-timestamp')
    return render(request, 'posts/posts.html', context)

@login_required(login_url='/login')
def post(request, title):
    context = {}
    context['posts'] = Post.objects.filter(slug=title).annotate(num_comments=Count('comment'))
    context['comments'] = Comment.objects.filter(post=Post.objects.filter(slug=title)[0]).filter(parentcomment=None).order_by('-timestamp')
    return render(request, 'posts/postdetail.html', context)

@login_required(login_url='/login')
def getcommentreply(request, commentid):
    context = {}
    if commentid != 0:
        context['posts'] = Post.objects.filter(comment__pk=commentid)[0]
    else:
        context['posts'] = Post.objects.get(pk=request.POST.get("postvalue", ""))
    context['commentid'] = commentid
    return render(request, 'posts/reply.html', context)

@login_required(login_url='/login')
def commentreply(request, commentid):
    context = {}
    if request.method == 'POST':
        posts = request.POST.get("postvalue", "")
        commenttext = request.POST.get("commenttext", "")

        currpost = Post.objects.get(pk=posts)
        if commentid != 0:
            parentcomment = Comment.objects.get(pk=commentid)
            level = parentcomment.level + 1
        else:
            parentcomment = None
            level = 0
        user = request.user
        c = Comment(author=user, post=currpost, parentcomment=parentcomment, text=commenttext, level=level)
        c.save()
        if commentid != 0:
            c.level = 1
        else:
            c.level = 0
        context['c'] = c
    else:
        pass
    return render(request, 'posts/comment.html', context)

@login_required(login_url='/login')
def create(request):
    context = {}
    if request.method == 'GET':
        if request.GET.get('title'):
            context['title'] = request.GET.get('title')
        else:
            context['title'] = ''
        if request.GET.get('link'):
            context['link'] = request.GET.get('link')
        else:
            context['link'] = ''
        return render(request, 'posts/create.html', context)        
    elif request.method == 'POST':
        title = request.POST.get("title", "")
        link = request.POST.get("link", "")
        editorvalue = request.POST.get("editorvalue", "")
        public = request.POST.get("public", "")
        public_bool = (public == 'public')
        user = request.user
        slug = slugify(title[:100])
        if len(Post.objects.filter(slug=slug)) > 0:
            slug += '-' + str(math.floor(random.uniform(1000,9999)))
        if title == None or title == '':
            context['message'] = 'You need a title :)'
        else:
            p = Post(author=user, title=title, text=editorvalue, link=link, slug=slug, public=public_bool)
            p.save()
            context['message'] = 'Message posted!'
            response = render(request, 'posts/success.html', context)
            response['X-IC-Redirect'] = '/post/' + slug
            return response
        return render(request, 'posts/success.html', context)
    return render(request, 'posts/create.html', context)
