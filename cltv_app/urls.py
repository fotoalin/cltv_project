from django.urls import path

from .views import download_report, result, upload_file

urlpatterns = [
    path("", upload_file, name="upload_file"),
    path("result/<int:result_id>/", result, name="result"),
    path("download_report/<int:result_id>/", download_report, name="download_report"),
]
