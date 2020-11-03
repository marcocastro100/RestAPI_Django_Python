from django.shortcuts import render #integrate the view to the html on templates
from django.shortcuts import redirect #redirect to other pages
from django.http import JsonResponse, HttpResponse #return data response to the page

from .models import Applet #importing my model 
from .forms import AppletForm #import the forms based in the model
from .serializers import AppletSerializer #importing serializer made to handle the model

#======Custom admin page======
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

#========API=========
from django.shortcuts import get_object_or_404 #if item not exists, return 404 instad error page
from rest_framework.views import APIView    #enables the use of class view (better looking and same as func)
from rest_framework.response import Response #Smart response
from rest_framework import status #status from response to avoid error page

#Dealing with a external system requiring not specified applet in url=================================
class api_list(APIView): 
#Show all applets in json format
    def get(self,request): #format=None: deal with extra url parameter (like .json)
        instance = Applet.objects.all();
        instance_dict = AppletSerializer(instance,many=True);
        return(Response(instance_dict.data));
#Create a new applet (post=create)
    def post(self,request):
        new_instance = request.data;
        new_instance_dict = AppletSerializer(data=new_instance);
        if(new_instance_dict.is_valid()):
            new_instance_dict.save();
            return Response(new_instance_dict.data,status=201); #201 = Created
        else: return(Response(new_instance_dict.error,status=400)) #400 = BadRequest

#External System requiring a specific applet=========================================================
from django.views.decorators.csrf import csrf_exempt
class api_detail(APIView): 
#Gets the current instance of applet givened by url
    def get_instance(self,id):
        current_instance = Applet.objects.get(id=id);
        return(current_instance);
#Show the applet in json format    
    def get(self,request,id):
        instance = self.get_instance(id);
        instance_dict = AppletSerializer(instance);
        return(Response(instance_dict.data));
#Modify the applet in the server database    
    def put(self,request,id):
        instance = self.get_instance(id);
            # instance_dict = AppletSerializer(instance,data=request.data);
        instance.title = request.data['title'];
        instance.description = request.data['description'];
        instance.language = request.data['language'];
        instance.location = request.data['location'];
        instance.interactivity = request.data['interactivity'];
        instance.context = request.data['context'];
        instance.copyright = request.data['copyright'];
            # if(instance_dict.is_valid()):
            #     instance.save();
            #     return(Response(instance_dict.data));
            # else:return(Reponse(instance_dict.errors,status=400))
        instance.save();
        return(Response(status=status.HTTP_200_OK));
#Delete the applet from the server        
    def delete(self,request,id):
        instance = self.get_instance(id);
        instance.delete()
        return(Response(status=204)) #204 = No Content

from rest_framework import viewsets
class AppletView(viewsets.ModelViewSet):
    queryset = Applet.objects.all()
    serializer_class = AppletSerializer