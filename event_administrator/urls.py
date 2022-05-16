from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), 
path("accounts/", include("django.contrib.auth.urls"), ),
path("event/", include("manage_currency.urls"))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
