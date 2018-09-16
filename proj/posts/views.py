from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.text import slugify
# Create your views here.
@login_required(login_url='/login')
def posts(request):
    context = {}
    context['posts'] = Post.objects.annotate(num_comments=Count('comment')).all().order_by('-timestamp')
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
    if request.method == 'POST':
        title = request.POST.get("title", "")
        link = request.POST.get("link", "")
        editorvalue = request.POST.get("editorvalue", "")
        user = request.user
        slug = slugify(title[:100])
        p = Post(author=user, title=title, text=editorvalue, link=link, slug=slug)
        p.save()
        context['message'] = 'Message posted!'
        return render(request, 'posts/success.html', context)
    return render(request, 'posts/create.html', context)





