from django.contrib import admin
from django.urls import path, include
from tours import views

admin.site.site_header = 'Панель администрирования Новосибирск-Тур'
admin.site.index_title = 'Управление турами и справочниками'
admin.site.site_title = 'Админ-панель Новосибирск-Тур'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tours.urls')),
]

handler404 = views.page_not_found