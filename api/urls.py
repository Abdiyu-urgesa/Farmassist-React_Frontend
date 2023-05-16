from django.urls import path
from . import views
from .view import privatesector_view 
from .view import region_view 
from .view import federal_view 
from .view import resource_view
from rest_framework_simplejwt.views import (TokenRefreshView,)
urlpatterns = [
    
    path('', views.getRoutes, name="routes"),
    path('user/<str:pk>/delete/', views.deleteUser, name="delete-user"),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    path('federals/', federal_view.getFederals, name="get-all-federals"),
    path('federal/create', federal_view.createFederal,
         name="create-federal"),
    path('federal/<str:pk>', federal_view.getFederal, name="get-one-federal"),
    path('federal/<str:pk>/update/', federal_view.updatFederal, name="update-federal"),


     path('regions/', region_view.getRegions, name="get-all-federals"),
    path('region/create', region_view.createRegion,
         name="create-region"),
    path('region/<str:pk>', region_view.getRegion, name="get-one-region"),
    path('region/<str:pk>/update/', region_view.updatRegion, name="update-region"),



    path('privates/', privatesector_view.getPrivateSectors, name="get-all-privates"),
    path('privates/create', privatesector_view.createPrivateSector,
         name="create-private-sector"),
    path('private/<str:pk>', privatesector_view.getprivateSector, name="get-one-private"),
    path('private/<str:pk>/update/', privatesector_view.updatePrivateSector, name="update-private"),

    path('resources/', resource_view.getResources, name="get-all-resource"),
    path('sentresources/', resource_view.getSentResource, name="get-all-sent-resource"),
    path('recievedresources/', resource_view.getrecievedResource, name="get-all-recieved-resource"),
    path('resource/', resource_view.getResource, name="get-one-resource"),
    path('transfer/', resource_view.transferResource, name="transfer-resource"),
    

]
