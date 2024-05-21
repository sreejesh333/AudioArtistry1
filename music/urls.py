from django.urls import path
from .views import *

urlpatterns = [
    path("saveimage/", SaveImage.as_view(), name="save_image"),
    path("downloadimage/<uuid:id>/", DownloadMusic.as_view(), name="download_image"),

]