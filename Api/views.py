from django.shortcuts import render
from django.http import HttpResponse
from .models import Applet
from .serializers import AppletSerializer

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
        else: return(HttpResponse('Bad Data Input')) #400 = BadRequest
#======================================================================================================
        #External System requiring a specific applet=========================================================
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
    #Search for jsons returns by key search in the model==================================
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

