from django.shortcuts import render #integrate the view to the html on templates
from django.http import JsonResponse, HttpResponse #return data response to the page

from .models import Applet #importing my model 
from .serializers import AppletSerializer #importing my serializer

from rest_framework.parsers import JSONParser #Convert string into JSON format
from rest_framework.renderers import JSONRenderer #Convert JSON format to dictionaries

def applets_list(request): #Activate when its to be showed all applets (no aditional info in the url (urls.py))
    if (request.method == 'GET'): #If user is requesting Data, Then show all applets
        applets = Applet.objects.all();
        serializer = AppletSerializer(applets,many=True); #sem many=True dá erro
        list_applets = serializer.data; #Take the serialized content
        return(JsonResponse(list_applets,safe=False)); #return in form of JSON, safe=false for serializing non dict data

    elif (request.method == 'POST'): #Case user is sending information (add a new applet)
        received_data = JSONParser().parse(request); #string received as request converted to JSON
        serializer =  AppletSerializer(data=received_data); #serialize the data
        if(serialized.is_valid()): 
            serializer.save();
            return(JsonResponse(serializer.data,status=201));
        return(JsonResponse(serilizer.error, status=400));

def applets_detail(request,pk): #Active when a applet id (pk) is selected (an is in the url (pk [urls.py]))
    applet = Applet.objects.get(pk=pk); #get the specific applet by the primary key

    if(request.method == 'GET'):
        serializer = AppletSerializer(applet); #selected applet in serialized mode
        return(JsonResponse(serializer.data)); #return his JSON

    elif(request.method == 'PUT'):
        received_data = JSONParser().parse(request); #string to JSON
        serializer = AppletSerializer(applet, data=received_data);
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif(request.method == 'DELETE'):
        applet.delete()
        return HttpResponse(status=204)
