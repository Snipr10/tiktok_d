from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import test_dava, test_car, test
urlpatterns = [
    path('test_dava', test_dava),
    path('test_car', test_car),
    path('test', test),

]
