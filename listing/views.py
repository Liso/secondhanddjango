# -*- coding: utf-8 -*-
import base64
import requests
import pytz
import uuid

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.generic import View
from datetime import datetime
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from scrapinghub import Connection
from listing.serializers import UserSerializer, GroupSerializer, PostSerializer
from listing.models import Post
from digg_paginator import DiggPaginator

# Create your views here.

def index(request):
    keyword = request.GET.get('kw')
    wanted_tag = u'求购'
    if keyword:
        post_list = Post.objects.filter(title__contains=keyword).order_by('-last_updated_at')
        wanted_post_list = Post.objects.filter(title__contains=keyword, tag=wanted_tag).order_by('-last_updated_at')
    else:
        post_list = Post.objects.all().order_by('-last_updated_at')
        wanted_post_list = Post.objects.filter(tag=wanted_tag).order_by('-last_updated_at')
    paginator = DiggPaginator(post_list, 17, body=5) # Show 17 posts per page
    wanted_paginator = DiggPaginator(wanted_post_list, 17, body=5) # Show 17 posts per page

    page = request.GET.get('page')
    wpage = request.GET.get('wpage')
    try:
        if not page:
            posts = paginator.page(1)
        else:
            posts = paginator.page(page)

        if not wpage:
            wanted_posts = wanted_paginator.page(1)
        else:
            wanted_posts = wanted_paginator.page(wpage)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
        wanted_posts = wanted_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        wanted_posts = wanted_paginator.page(wanted_paginator.num_pages)
    return render_to_response('listing/index.html', {"posts": posts, "wanted_posts": wanted_posts}, context_instance=get_common_context(request))

def home(request):
    keyword = request.GET.get('kw')
    if keyword:
        post_list = Post.objects.filter(title__contains=keyword).order_by('-last_updated_at')
    else:
        post_list = Post.objects.all().order_by('-last_updated_at')
    paginator = DiggPaginator(post_list, 17, body=5) # Show 17 posts per page

    page = request.GET.get('page')
    try:
        if not page:
            posts = paginator.page(1)
        else:
            posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render_to_response('listing/home.html', {"posts": posts}, context_instance=RequestContext(request))

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def getScrapyRes(url):
    private_key = settings.SCRAPINGHUB_KEY
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    auth = "Basic %s" % b64
    headers = {'Content-type': 'application/json', 'Authorization': auth}
    return requests.get(url, headers=headers).json()
 
# fetch chineseinsfbay
@user_passes_test(lambda u: u.is_superuser)
def fetchChineseInSFBay(request):
    job = request.GET.get("job")
    crawlerUrl = 'https://storage.scrapinghub.com/items/65427/1/' + job + '?format=json'
    return fetcher(crawlerUrl)
 
# fetch chineseinsfbay
@user_passes_test(lambda u: u.is_superuser)
def fetchMoonbbs(request):
    job = request.GET.get("job")
    crawlerUrl = 'https://storage.scrapinghub.com/items/65427/2/' + job + '?format=json'
    return fetcher(crawlerUrl)

@user_passes_test(lambda u: u.is_superuser)
def fetchHourly(request):
    conn = Connection(settings.SCRAPINGHUB_KEY)
    project = conn[65427]
    jobs = project.jobs(state='finished', has_tags='hourly', count=2)
    for job in jobs:
        saveItems(job.items())
    return HttpResponse('success')
 
def fetcher(crawlerUrl):
    res = getScrapyRes(crawlerUrl)
    return saveItems(res)

def saveItems(res):
    for entry in res:
        link = str(entry['link'])
        link_hash = uuid.uuid3(uuid.NAMESPACE_DNS, link)
        updated_values = {'url': link, 'tag': entry['tag'], 'title': entry['title'], 'last_updated_at': parseTime(entry['timestamp'])}
        p, created = Post.objects.update_or_create(url_index=link_hash, defaults=updated_values)
    return HttpResponse('success')

# time_string is expected as 2016-05-17
def parseTime(time_string):
    tz = pytz.timezone('America/Los_Angeles')
    try:
        return tz.localize(datetime.strptime(time_string, "%Y-%m-%d"))
    except ValueError:
        format = '%Y-%m-%d %I:%M %p'
        try:
          return tz.localize(datetime.strptime(time_string, format))
        except ValueError:
          return datetime.now(tz)

def get_common_context(request):
    return RequestContext(request, {'request': request, 'user': request.user})
