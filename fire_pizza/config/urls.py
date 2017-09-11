from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    url(r'^', include('pizza_app.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
