from django.urls import path
from .api import CategoryResource



urlpatterns = [
    path('categories', CategoryResource.as_view())
]
