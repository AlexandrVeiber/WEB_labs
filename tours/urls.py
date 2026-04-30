from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tour/<slug:tour_slug>/', views.tour_detail, name='tour_detail'),
    path('category/<slug:cat_slug>/', views.category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_tourlist, name='tag'),
    path('direction/<slug:dir_slug>/', views.direction, name='direction'),
    path('contacts/', views.contacts, name='contacts'),
    path('prices/', views.prices, name='prices'),
    path('archive/<int:year>/', views.archive, name='archive'),

    path('add-form/', views.add_tour_form, name='add_tour_form'),
    path('add-model-form/', views.add_tour_model_form, name='add_tour_model_form'),
    path('upload/', views.upload_file, name='upload_file'),
]