from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import test
urlpatterns = [
    path('test', test)
]
