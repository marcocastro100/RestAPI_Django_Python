from django.http import HttpResponse #return data response to the page
from .models import Applet #Import applet DB model
from .models import AppletForm, SearchForm #Import Applet form (all fields) and Search (context, language)
from .models import AppletSerializer #importing created serializer (convert a structure to a dictionary)

############################______G U I______##################################################################
from django.shortcuts import render #integrate the view to the html on templates
from django.shortcuts import redirect #redirect to other pages
import json #Work with json files

#==============================================================================
def applets_list(request): #Root /applets: list all Applets models instances
    instance = Applet.objects.all(); #Catch all instances in the database
    instance_dict = AppletSerializer(instance,many=True); #Serializes the instances
    instance_json = json.dumps(instance_dict.data) #Formats the instances to json for browser purposes
    return(render(request,'Applets/templates/list.html',{'Applets':json.loads(instance_json)})) #Handles how that json will be showed in the browser (iteration)

#=====================================================================
def applets_detail(request,id): #Active when a applet id (pk) is selected (an is in the url (pk [urls.py]))
    instance = Applet.objects.get(id=id); #get the specific applet by the primary key
    instance_dict = AppletSerializer(instance); #selected applet in serialized mode
    instance_json = json.dumps(instance_dict.data); #To json for correcly show in browser
    instance_form =  AppletForm(request.POST or None, instance=instance); #Creates a form with POST (change) data, where the default values showed are the current values of the instance
    if (request.method == 'POST'):
        instance_form.save(); #verify if is valid and saves it
    return(render(request,'Applets/templates/detail.html',{'Applet':json.loads(instance_json),'formulario_modelo':instance_form}))

#=====================================================================
def applets_create(request): #creates a new applet
    if(request.method == 'GET'):
        instance_form = AppletForm(); #Just entering the page, define the form as GET
    elif(request.method == 'POST'):
        instance_form = AppletForm(request.POST); #Case sending information to DB, defines form as POST
        instance_form.save();
    return(render(request,'Applets/templates/create.html',{'formulario_modelo':instance_form})) #sends to template to render it in html forms

#=====================================================================
def applets_delete(request,id):
    instance = Applet.objects.get(id=id); #get the deleting id
    instance.delete() #deletes from db
    return(redirect('../../')); #redirect to other page

#=====================================================================
import os #Controls the Operacional system (create a folder/file if not exists yet)
def applets_download(request,id):
    instance = Applet.objects.get(id=id);
    instance_dict = AppletSerializer(instance);
    instance_json = json.dumps(instance_dict.data,indent=2);
    if not os.path.exists('./jsons'): os.makedirs('./jsons'); #Check if folder jsons exists and creates if not
    with open('./jsons/'+str(instance.id)+'.json','w') as file: file.write(instance_json);
    return(redirect('../../'));

#=====================================================================
def applets_search(request):
    if(request.method == 'GET'):
        instance_form = SearchForm(); #Form with only key search fields
        return(render(request,'Applets/templates/search.html',{'form':instance_form}))

    if(request.method == 'POST'):
        requested = {}; #create a dictionary for filtering in the DB
        requested['context'] = request.POST['context'];
        requested['language'] = (request.POST['language']);
        instances = Applet.objects.filter(context=requested['context'],language=requested['language']); #Take the instances in the BD with the informed keys
        instances_dict = AppletSerializer(instances,many=True);
        instances_json = json.dumps(instances_dict.data) #To json for correcly show in browser
        instance_form = SearchForm(instance=instances[0]); #instances to continue with current search key values in the form
        return(render(request,'Applets/templates/search.html',{'form':instance_form,'instances':json.loads(instances_json)}))

#=====================================================================



############################______A P I______##################################################################
from rest_framework.views import APIView #enables the use of class view (better looking and same as function)
from rest_framework.response import Response #Smart response (json, api, error handling, etc)
from rest_framework import status #status from response to avoid error page

#=====================================================================
    #Dealing with a external system requiring not specified applet in url
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
        else: return(HttpResponse('Bad Data Input')) #400 = BadRequest

#======================================================================================================
        #External System requiring a specific applet
    # from django.views.decorators.csrf import csrf_exempt
class api_detail(APIView): 

        #Gets the current instance of applet givened by url
    def pick_instance(self,id):
        current_instance = Applet.objects.get(id=id);
        return(current_instance);

        #Show the applet in json format    
    def get(self,request,id):
        instance = self.pick_instance(id);
        instance_dict = AppletSerializer(instance);
        return(Response(instance_dict.data));

        #Delete the applet from the server        
    def delete(self,request,id):
        instance = self.pick_instance(id);
        instance.delete()
        return(Response(status=204)) #204 = No Content

        #Modify the applet in the server database    
    def put(self,request,id):
        instance = self.pick_instance(id);
        instance_dict = AppletSerializer(instance,data=request.data);
        if(instance_dict.is_valid()):
            instance.save();
            return(Response(instance_dict.data));
        else:
            return(HttpResponse('Bad Data Input!'))
        return(Response(status=200));

#======================================================================================================
    #Search for jsons returns by key search in the model
class api_search(APIView): 
    def get(self,request): #only generates the form for search
        return(HttpResponse('Envie um method POST com as keys: context=[Geometria, Calculo, Estatistica, Aritimetica, Trigonometria, Algebra, Probabilidade, Funcoes] e language=[EN,PT]'))

    def post(self,request): #Makes a search for the entry data, returning the jsons maching the pattern
        requested = {}; #makes a dictionary to receive the parameters
        requested['context'] = request.data['context']; #add context data in dict
        requested['language'] = request.data['language']; #add language data in dict
        instances = Applet.objects.filter(context=requested['context'],language=requested['language']); #filter the applets to be returned
        instances_dict = AppletSerializer(instances,many=True); #only a serialization for json formating
        return(Response(instances_dict.data)); #sends the data in json format