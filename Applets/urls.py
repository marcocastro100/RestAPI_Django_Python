from django.urls import path, include #way to redirect web page to the project tree structure
from . import views

# from rest_framework import routers
# router = routers.DefaultRouter()
# router.register('rest',views.AppletView)

urlpatterns = [
    path('',views.applets_list,name='list'),
    path('<int:id>/',views.applets_detail,name='detail'), #when a integer (pk) is in the url, redirect to detail json show
    path('create/',views.applets_create,name='create'),
    path('delete/<int:id>/',views.applets_delete,name='delete'),
    path('download/<int:id>/',views.applets_download,name='download'),
    path('search/',views.applets_search,name='search'),

    path('api/',views.api_list.as_view(),name='api_list'),
    path('api/<int:id>/',views.api_detail.as_view(),name='api_detail'),
    path('api/search/',views.api_search.as_view(),name='api_search'),

    

    # path('rest/',include(router.urls)),
]
