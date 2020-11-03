from django.shortcuts import render #integrate the view to the html on templates
from django.shortcuts import redirect #redirect to other pages
from django.http import JsonResponse, HttpResponse #return data response to the page

from .models import Applet #importing my model 
from .forms import AppletForm #import the forms based in the model
from .serializers import AppletSerializer #importing serializer made to handle the model

import json
def applets_list(request): #Root /applets: list all Applets models instances
    instance = Applet.objects.all(); #Catch all instances in the database
    instance_dict = AppletSerializer(instance,many=True); #Serializes the instances
    instance_json = json.dumps(instance_dict.data) #Formats the instances to json
    return(render(request,'Applets/templates/list.html',{'Applets':json.loads(instance_json)})) #Handles how that json will be showed in the browser (iteration)
#=====================================================================
def applets_detail(request,id): #Active when a applet id (pk) is selected (an is in the url (pk [urls.py]))
    instance = Applet.objects.get(id=id); #get the specific applet by the primary key
    instance_dict = AppletSerializer(instance); #selected applet in serialized mode
    instance_json = json.dumps(instance_dict.data); #transforms to json
    instance_form =  AppletForm(request.POST or None, instance=instance); #Creates a form with POST (change) data, where the default values showed are the current values of the instance
    if (instance_form.is_valid()):
        instance_form.save(); #verify if is valid and saves it
        return(redirect('../'));
    return(render(request,'Applets/templates/detail.html',{'Applet':json.loads(instance_json),'formulario_modelo':instance_form}))
#=====================================================================
def applets_create(request): #creates a new applet
    if(request.method == 'GET'):
        instance_form = AppletForm(); #Just entering the page, define the form as GET
    elif(request.method == 'POST'):
        instance_form = AppletForm(request.POST) #Case sending information to DB, defines form as POST
        if instance_form.is_valid(): #verify if the form respects the model
            instance_form.save(); #salva os dados no BD
            return(redirect('../'));
    return(render(request,'Applets/templates/create.html',{'formulario_modelo':instance_form})) #sends to template to render it in html forms
#=====================================================================
def applets_delete(request,id):
    instance = Applet.objects.get(id=id); #get the deleting id
    instance.delete() #deletes from db
    return(redirect('../../')); #redirect to other page
#=====================================================================
def applets_download(request,id):
    instance = Applet.objects.get(id=id);
    instance_dict = AppletSerializer(instance);
    instance_json = json.dumps(instance_dict.data,indent=2);
    with open('./jsons/'+str(instance.id)+'.json','w') as file: file.write(instance_json);
    return(redirect('../../'));
#=====================================================================
from rest_framework import viewsets
class AppletView(viewsets.ModelViewSet):
    queryset = Applet.objects.all()
    serializer_class = AppletSerializer

# from rest_framework.parsers import JSONParser #Convert string into JSON format
# from rest_framework.renderers import JSONRenderer #Convert JSON format to dictionaries
# from rest_framework.response import Response #Smart response/quest (httpresponse,jsonresponse,etc.)
# from rest_framework.request import Request #//



            # return(JsonResponse(serializer.data,safe=False)); #return in form of JSON, safe=false for serializing non dict data

    # elif (request.method == 'POST'): #Case user is sending information (add a new applet)
    #     received_data = JSONParser().parse(request); #string received as request converted to JSON
    #     serializer =  AppletSerializer(data=received_data); #serialize the data
    #     if(serialized.is_valid()): 
    #         serializer.save();
    #         return(JsonResponse(serializer.data,status=201));
    #     return(JsonResponse(serilizer.error, status=400));

    # if(request.method == 'GET'):
        # serializer = AppletSerializer(applet); #selected applet in serialized mode
        # data_json = json.dumps(serializer.data);
    #     return(render(request,'Applets/templates/detail.html',
    #         {'Applet':json.loads(data_json),
    #         'formulario_modelo':AppletForm(request.POST)}))

        # return(JsonResponse(serializer.data)); #return his JSON

    # elif(request.method == 'PUT'):
    #     received_data = JSONParser().parse(request); #string to JSON
    #     serializer = AppletSerializer(applet, data=received_data);
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)

    # elif(request.method == 'DELETE'):
    #     applet.delete()
    #     return HttpResponse(status=204)