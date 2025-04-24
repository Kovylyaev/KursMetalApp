from django.urls import path
from .views import Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("upload_grey_image", Index.as_view(), name="upload_grey_image"),
]