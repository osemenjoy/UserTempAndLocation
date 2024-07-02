from django.urls import path
from .views import *


urlpatterns = [
    path('hello/', HelloApiView.as_view(), name="hello"),
]