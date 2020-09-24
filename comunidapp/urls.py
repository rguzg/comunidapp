from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Apps.Users import urls as urls_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls_users)),
]


from .import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, 
# document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, 
# document_root=settings.MEDIA_ROOT)
