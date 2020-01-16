from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from cricket.views import TeamCreateList


urlpatterns = [
    path('admin/', admin.site.urls),
	path('cricket/',include('cricket.urls')),
	path('',TeamCreateList.as_view(), name='team-create-list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)