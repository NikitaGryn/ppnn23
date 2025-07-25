from django.urls import path
from jsonupload.views import JsonUploadFormView, JsonDataListView

urlpatterns = [
    path('upload/', JsonUploadFormView.as_view(), name="upload-json"),
    path('view/', JsonDataListView.as_view(), name="view-data"),
]