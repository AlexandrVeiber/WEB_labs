from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tours import views

admin.site.site_header = 'Панель администрирования Новосибирск-Тур'
admin.site.index_title = 'Управление турами и справочниками'
admin.site.site_title = 'Админ-панель Новосибирск-Тур'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tours.urls')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found