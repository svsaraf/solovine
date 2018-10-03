"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from registration import views as registration_views
from posts import views as posts_views
from feeds import views as feeds_views
from friends import views as friends_views
admin.site.site_header = 'Solovine admin'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', registration_views.home, name='home'),
    path('register/', registration_views.register, name='register'),
    path('login/', registration_views.login, name='login'),
    path('logout/', registration_views.logout, name='logout'),

    path('public/', posts_views.public_posts, name='public_posts'),
    path('public/<slug:title>/', posts_views.public_post, name='public_post'),
    path('posts/', posts_views.posts, name='posts'),
    path('post/<slug:title>/', posts_views.post, name='post'),
    path('getcommentreply/<int:commentid>/', posts_views.getcommentreply, name='getcommentreply'),
    path('reply/<int:commentid>/', posts_views.commentreply, name='commentreply'),
    path('create/', posts_views.create, name='create'),
    
    path('feeds/', feeds_views.feeds, name='feeds'),
    path('getfeedadd/', feeds_views.getfeedadd, name='getfeedadd'),
    path('addfeed/', feeds_views.addfeed, name='addfeed'),


    path('user/<str:email>/', friends_views.profile, name='userprofile'),
    path('accept/<str:email>/', friends_views.accept, name='acceptrequest'),
    path('send/<str:email>/', friends_views.send, name='sendrequest'),
    path('reject/<str:email>/', friends_views.reject, name='rejectrequest'),
    path('cancel/<str:email>/', friends_views.cancel, name='cancelrequest'),
]

