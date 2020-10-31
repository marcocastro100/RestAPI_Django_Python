from django.urls import path #way to redirect web page to the project tree structure
from . import views

urlpatterns = [
    path('',views.applets_list),
    path('<int:pk>/',views.applets_detail) #when a integer (pk) is in the url, redirect to detail json show
]
