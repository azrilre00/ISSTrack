from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import urllib.request 
import json
# Create your views here.


def displayISS(request):
    # url = "http://api.open-notify.org/astros.json"
    url = "http://api.open-notify.org/iss-now.json" 
    response = urllib.request.urlopen(url) 
    result = json.loads(response.read())
    print(result['iss_position'])
    context = {'result':result}
    return render(request, 'home.html', context)

@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        pass
        # return Response(serializer.data)