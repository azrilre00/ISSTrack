from django.shortcuts import redirect, render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from datetime import datetime
import urllib.request 
import json
from track.forms import ISSForm
# Create your views here.


def displayISS(request):
    # url = "http://api.open-notify.org/astros.json"
    # url = "http://api.open-notify.org/iss-now.json" 
   
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    response = urllib.request.urlopen(url) 
    result = json.loads(response.read())
    form = ISSForm()
    context = {'result': result, 'form': form}

    if request.POST:
        date = request.POST['date']
        # print(type(date))
        # print(date)
        time = request.POST['time']
        # print(daytime)
        
        datetimes_ISS = str(date + " " + time)
        # print(type(datetimes_ISS))
        # print(datetimes_ISS)
        date_time_obj = datetime.strptime(datetimes_ISS, '%Y-%m-%d %H:%M')
        times = datetime.timestamp(date_time_obj)
        # print(date_time_obj)
        # print(type(date_time_obj))
        # print(times)
        urltime = url + "?timestamp=" + str(times)
        # print(urltime)
        response = urllib.request.urlopen(urltime) 
        result = json.loads(response.read())
        latitude = str(result["latitude"])
        longitude = str(result["longitude"])
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)
        print(location, latitude + ", " + longitude)
        return redirect('home')
    else:
        
        latitude = str(result["latitude"])
        longitude = str(result["longitude"])
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)
        # location = geolocator.reverse("3.1275272211037284 , 101.59307183409135")
        # print(result['iss_position']["longitude"])
        
        # print(location, latitude + ", " + longitude)
        
        return render(request, 'home.html', context)

