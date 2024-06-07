from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import download_report, home, recommendations, result, upload_file

urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload_file, name="upload_file"),
    path("result/<int:result_id>/", result, name="result"),
    path("download_report/<int:result_id>/", download_report, name="download_report"),
    path("recommendations/", recommendations, name="recommendations")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

