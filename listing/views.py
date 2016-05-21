import base64
import requests

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from listing.serializers import UserSerializer, GroupSerializer

# Create your views here.

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

class ListItems(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        private_key = "8a94547f3ac24f18ab3dfac27602edb4"
        b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
        auth = "Basic %s" % b64
        headers = {'Content-type': 'application/json', 'Authorization': auth}
        url = 'https://storage.scrapinghub.com/items/65427/1/2'
        return Response(requests.get(url, headers=headers).text)
