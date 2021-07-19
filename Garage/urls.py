from django.urls import path
from . import views


urlpatterns = [
    # home 
    path('',views.home,name="GarageHome"), 
    # search
    path('search/',views.search,name = "search"),
    # vehicle paths for add, delete, remove
    path('delete/vehicle/<str:vehicleNo>/',views.deleteVehicle,name = "deleteVehicle"),
    path('update/vehicle/',views.updateVehicle, name= "updateVehicle"),
    path('add/vehicle/',views.addVehicle, name="addVehicle"),
    # services paths for add , remove, delete
    path('delete/service/<str:vehicleNo>/<str:serviceid>/',views.removeServiceByID,name = "deleteService"),
    path('update/service/<str:vehicleNo>/<str:serviceid>/',views.updateService,name = "updateService"),
    path('add/service/<str:vehicleNo>/',views.addService,name="addService")

]

