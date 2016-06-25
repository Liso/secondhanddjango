import base64
import requests

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.generic import View
from datetime import datetime
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from listing.serializers import UserSerializer, GroupSerializer, PostSerializer
from listing.models import Post
from digg_paginator import DiggPaginator

# Create your views here.

def index(request):
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
    private_key = "8a94547f3ac24f18ab3dfac27602edb4"
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    auth = "Basic %s" % b64
    headers = {'Content-type': 'application/json', 'Authorization': auth}
    return requests.get(url, headers=headers).json()
 
# fetch chineseinsfbay
def fetchChineseInSFBay(request):
    crawlerUrl = 'https://storage.scrapinghub.com/items/65427/1/4?format=json'
    return fetcher(crawlerUrl)
 
# fetch chineseinsfbay
def fetchMoonbbs(request):
    crawlerUrl = 'https://storage.scrapinghub.com/items/65427/2/3?format=json'
    return fetcher(crawlerUrl)

def fetcher(crawlerUrl):
    res = getScrapyRes(crawlerUrl)
    for entry in res:
        updated_values = {'title': entry.get('title'), 'last_updated_at': parseTime(entry.get('timestamp'))}
        p, created = Post.objects.update_or_create(url=entry.get('link'), defaults=updated_values)
    return HttpResponse('success')

# time_string is expected as 2016-05-17
def parseTime(time_string):
    try:
        return datetime.strptime(time_string, "%Y-%m-%d")
    except ValueError:
        datetime_string = datetime.today().date().strftime("%Y-%m-%d") + " " + time_string
        format = '%Y-%m-%d %I:%M %p'
        return datetime.strptime(datetime_string, format)
