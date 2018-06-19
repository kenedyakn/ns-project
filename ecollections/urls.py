from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/history/', views.upload_file, name='upload'),
    path('upload/collections/', views.upload_file_collections, name='upload_collections'),
    path('collections/', views.get_all_collections, name='collections'),
    path('master-file/', views.get_master_data, name='master_data'),
    path('collections/filter/', views.filter_search, name='filter'),
    path('<int:employer_id>/', views.detail, name='detail'),
    path('<int:employer_id>/results/', views.results, name='results'),
    path('<int:employer_id>/comment/', views.comment, name='comment'),
]