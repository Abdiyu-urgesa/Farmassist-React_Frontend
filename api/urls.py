from django.urls import path
from . import views
from .view import privatesector_view 
from .view import region_view 
from .view import zone_view 
from .view import federal_view 
from .view import resource_view
from .view import woreda_view 
from .view import KebeleAdmin_view 
from .view import kebeleBusiness_view 
from .view import farmer_view
from .view import post_view
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


    path('zones/', zone_view.getZones, name="get-all-zones"),
    path('zone/create', zone_view.createZone,
         name="create-zone"),
    path('zone/<str:pk>', zone_view.getZone, name="get-one-zone"),
    path('zone/<str:pk>/update/', zone_view.updatZone, name="update-zone"),
    path('woreda/<str:pk>', woreda_view.getWoreda, name="get-one-woreda"),
    path('woreda/<str:pk>/update/', woreda_view.updateWoreda, name="update-woreda"),

    path('kebeleadmins/', KebeleAdmin_view.getKebeleAdmins, name="get-all-zones"),
    path('kebeleadmin/create', KebeleAdmin_view.createKebeleAdmins,
         name="create-kebeleadmin"),
    path('kebeleadmin/<str:pk>', KebeleAdmin_view.getkebeleadmin, name="get-one-kebeleadmin"),
    path('kebeleadmin/<str:pk>/update/', KebeleAdmin_view.updateKebeleAdmin, name="update-kebeleadmin"),

    path('kebelebusinesses/', kebeleBusiness_view.getKebeleBusiness, name="get-all-zones"),
    path('kbelebusiness/create', kebeleBusiness_view.createKebeleBusiness,
         name="create-kbelebusiness"),
    path('kbelebusiness/<str:pk>', kebeleBusiness_view.getKebeleBusines, name="get-one-kbelebusiness"),
    path('kbelebusiness/<str:pk>/update/', kebeleBusiness_view.updateKebeleBusiness, name="update-kbelebusiness"),
    
    path('privates/', privatesector_view.getPrivateSectors, name="get-all-privates"),
    path('privates/create', privatesector_view.createPrivateSector,
         name="create-private-sector"),
    path('private/<str:pk>', privatesector_view.getprivateSector, name="get-one-private"),
    path('private/<str:pk>/update/', privatesector_view.updatePrivateSector, name="update-private"),


    path('farmers/', farmer_view.getFarmers, name="get-all-farmer"),
    path('farmer/create', farmer_view.createFarmer,name="create-farmer"),
    path('farmer/<str:pk>', farmer_view.getFarmer, name="get-one-farmer"),
    path('farmer/<str:pk>/update/', farmer_view.updateFarmer, name="update-farmer"),

    path('resources/', resource_view.getResources, name="get-all-resource"),
    path('resources/create', resource_view.createResource, name="get-all-resource"),
    path('sentresources/', resource_view.getSentResource, name="get-all-sent-resource"),
    path('recievedresources/', resource_view.getrecievedResource, name="get-all-recieved-resource"),
    path('recievedresources/accept/', resource_view.acceptResource),
    path('resource/', resource_view.getResource, name="get-one-resource"),
    path('transfer/', resource_view.transferResource, name="transfer-resource"),

    path('posts/', post_view.getPosts, name="get-all-posts"),
    

]
