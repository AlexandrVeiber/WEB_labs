from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToursHome.as_view(), name='home'),
    path('tour/<slug:tour_slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('category/<slug:cat_slug>/', views.TourCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagTourListView.as_view(), name='tag'),
    path('direction/<slug:dir_slug>/', views.DirectionTourListView.as_view(), name='direction'),

    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('prices/', views.PricesView.as_view(), name='prices'),
    path('archive/<int:year>/', views.ArchiveView.as_view(), name='archive'),

    path('add-form/', views.AddTourFormView.as_view(), name='add_tour_form'),
    path('add-model-form/', views.AddTourModelFormView.as_view(), name='add_tour_model_form'),
    path('edit/<slug:tour_slug>/', views.UpdateTourView.as_view(), name='edit_tour'),
    path('delete/<slug:tour_slug>/', views.DeleteTourView.as_view(), name='delete_tour'),

    path('upload/', views.UploadFileView.as_view(), name='upload_file'),
]