from django.urls import path

from .views import result, upload_file

urlpatterns = [
    path("", upload_file, name="upload_file"),
    path("result/<int:result_id>/", result, name="result"),
]
