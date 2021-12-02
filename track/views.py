from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.geocoders import Nominatim
import urllib.request 
import json
# Create your views here.


def displayISS(request):
    # url = "http://api.open-notify.org/astros.json"
    # url = "http://api.open-notify.org/iss-now.json" 
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    response = urllib.request.urlopen(url) 
    result = json.loads(response.read())

    if request.POST:
        pass
    else:
        latitude = str(result["latitude"])
        longitude = str(result["longitude"])
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+","+longitude)
        # location = geolocator.reverse("11.001202151377, -125.29176594612")
        # print(result['iss_position']["longitude"])
        print(location, latitude, longitude)
        context = {'result':result}
        return render(request, 'home.html', context)

@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        pass
        # return Response(serializer.data)