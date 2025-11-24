
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cv_home, name='cv_home'),
    path('cv/<str:lang>/', views.cv_view, name='cv_view'),
    path("download-cv/", views.download_cv, name="download_cv"),
    path("log-print-click/", views.log_print_click, name="log_print_click"),
    path("log-download-click/", views.log_download_click, name="log_download_click"),
]
