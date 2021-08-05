from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.parsing_by_hashtag import parsing


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test(request):
    parsing('test')
    return Response("Ok")