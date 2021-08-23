import datetime

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.parsing_by_hashtag import parsing_hashtag
from core.parsing_by_username import parsing_username


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test_dava(request):
    # parsing_hashtag('test')
    s = False
    while s == False:
        s = parsing_username('dava_m', datetime.date.today())
    return Response("Ok")


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test_car(request):
    s = False
    while s == False:
        s = parsing_hashtag('s')
    return Response("Ok")