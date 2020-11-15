from django.urls import path, include #way to redirect web page to the project tree structure
from . import views

# from rest_framework import routers
# router = routers.DefaultRouter()
# router.register('rest',views.AppletView)

urlpatterns = [    
    path('',views.api_list.as_view(),name='api_list'),
    path('<int:id>/',views.api_detail.as_view(),name='api_detail'),
    path('search/',views.api_search.as_view(),name='api_search'),

    # path('rest/',include(router.urls)),
]