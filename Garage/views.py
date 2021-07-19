from django.shortcuts import render, redirect

from .forms import SearchForm, VehicalForm, updateServiceForm
from .utility import (extractVehicleData, removeVehicle, addVehical, fetchVehicleData,
                        updateVehileData, add_Service,deleteService, get_service, updateServiceData)




searchform = SearchForm()
vehicleform = VehicalForm()
global_context= {
        "searchForm" : searchform,
        "vehicleForm" : vehicleform}

def home(request):    
   return render(request, "Garage/index.html",context=global_context)

def search(request):
    context= {}
    context["vehicleForm"] = VehicalForm()
    context["searchForm"] = SearchForm()
    context["data"] = False
    if request.method == "GET":
        return redirect('GarageHome')
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            vehicle_number = form.cleaned_data.get("searchinput")
            data = extractVehicleData(vehicle_number)
            if data:
                vehicleData = {
                        "vehicleno" : data["vehicleno"],
                        "brand": data["brand"],
                        "model": data["model"]
                    }
                context["vehicleno"] = data["vehicleno"]
                context["vehicleForm"] = VehicalForm(initial=vehicleData)
                context["services"] = data["services"]
                context["data"] = True
    if not context["data"]:
        context["message"] = "data not found"
    return render(request,"Garage/index.html",context=context)


def addVehicle(request):
    context = global_context.copy()
    if request.method == "POST":
        form = VehicalForm(request.POST)
        if form.is_valid():
            data = {}
            data["vehicleno"] = form.cleaned_data.get("vehicleno")
            data["brand"] = form.cleaned_data.get("brand")
            data["model"] = form.cleaned_data.get("model")
            
            if addVehical(data):
                message = "Vehicle " + data["vehicleno"] + " Added."
                context["message"] = message
            else:
                # 25BMR 
                message = "Vehicle " + data["vehicleno"] + " Already exit."
                context["message"] = message

    return render(request,"Garage/index.html",context=context)



def updateVehicle(request):
    context = global_context.copy()
    if request.method == "POST":
        form = VehicalForm(request.POST)
        if form.is_valid():
            data = {}
            data["vehicleno"] = form.cleaned_data.get("vehicleno")
            data["brand"] = form.cleaned_data.get("brand")
            data["model"] = form.cleaned_data.get("model")
            
            if updateVehileData(data):
                message = "Vehicle " + data["vehicleno"] + " updated"
                context["message"] = message
            else:
                message = "some error"
                context["message"] = message

    return render(request,"Garage/index.html",context=context)
    
def deleteVehicle(request,vehicleNo):
    removeVehicle(vehicleNo)
    return redirect("GarageHome")          

    

def addService(request,vehicleNo):
    context={
        "vehicleno" : vehicleNo
    }
    if request.method == "GET":
        row = fetchVehicleData(vehicleNo)
        if row:
            context["found"] = True
            default = { "vehicleno" : vehicleNo }
            form = updateServiceForm(initial=default)
            context["form"] = form
            context["value"] = "hi"
            return render(request,"Garage/addServices.html",context = context)
        else: 
            context["found"] = False
            return render(request,"Garage/addServices.html",context = context)
    if request.method == "POST":
        context= {}
        context["vehicleForm"] = VehicalForm()
        context["searchForm"] = SearchForm()
        context["data"] = False
        form = updateServiceForm(request.POST)
        if form.is_valid():
            form_data = {
            "servicetype": form.cleaned_data.get("servicetype"),
            "vehicleno" : form.cleaned_data.get("vehicleno")
            }
            if add_Service(form_data):
                data = extractVehicleData(vehicleNo)
                if data:
                    vehicleData = {
                            "vehicleno" : data["vehicleno"],
                            "brand": data["brand"],
                            "model": data["model"]
                        }
                    context["vehicleno"] = data["vehicleno"]
                    context["vehicleForm"] = VehicalForm(initial=vehicleData)
                    context["services"] = data["services"]
                    context["data"] = True
                    return render(request,"Garage/index.html",context = context)
            return render(request,"Garage/outcheck.html")



def updateService(request,vehicleNo,serviceid):
    context = {}
    if request.method == "GET":
        if row := get_service(serviceid):
            _, servicetype,_ = row
            default = {
                "servicetype" : servicetype,
                "vehicleno" : vehicleNo
            }
            form = updateServiceForm(initial=default)
            context["form"] = form
            context["vehicleno"] = vehicleNo
            context["serviceid"] = serviceid
            context["get"] = True
            return render(request,"Garage/updateService.html",context=context)
        else:
            return redirect("GarageHome")
    if request.method == "POST":
        context["vehicleForm"] = VehicalForm()
        context["searchForm"] = SearchForm()
        context["data"] = False
        form = updateServiceForm(request.POST)
        if form.is_valid():
            data = {
                "servicetype" : form.cleaned_data.get("servicetype"),
                "serviceid": serviceid
            }
            if updateServiceData(data):
                if vehicle_data := extractVehicleData(vehicleNo):
                    context.update(vehicle_data)
                    default = {
                    "vehicleno" : vehicle_data["vehicleno"],
                    "brand": vehicle_data["brand"],
                    "model": vehicle_data["model"]
                }
                context["vehicleForm"] = VehicalForm(initial=vehicle_data)
                context["data"] = True
    return render(request,"Garage/index.html",context= context )
        


def removeServiceByID(request,vehicleNo,serviceid):
    context= {}
    context["vehicleForm"] = VehicalForm()
    context["searchForm"] = SearchForm()
    context["data"] = False
    if deleteService(serviceid):
        data = extractVehicleData(vehicleNo)
        if data:
            vehicleData = {
                    "vehicleno" : data["vehicleno"],
                    "brand": data["brand"],
                    "model": data["model"]
                }
            context["vehicleForm"] = VehicalForm(initial=vehicleData)
            context["vehicleno"] = data["vehicleno"]
            context["services"] = data["services"]
            context["data"] = True
    return render(request,"Garage/index.html",context=context)