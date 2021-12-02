from django.shortcuts import redirect, render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
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

        list_times = []
        for i in range(5):
            time_b4 = date_time_obj + timedelta(minutes=10)
            # print(time_b4)
            list_times.append(time_b4)
            date_time_obj = time_b4
        # print(list_times[1])
        for i in range(5):
            time_b4 = date_time_obj + timedelta(minutes=-10)
            # print(time_b4)
            list_times.append(time_b4)
            date_time_obj = time_b4
        # print(date_time_obj)
        # print(type(date_time_obj))
        # print(times)
        # print(list_times)
        urltime = url + "?timestamp=" + str(times)
        # print(urltime)
        response = urllib.request.urlopen(urltime) 
        result = json.loads(response.read())
        latitude = str(result["latitude"])
        longitude = str(result["longitude"])
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)
        
        if location == None:
            print("The ISS location probably in a location where coverage is not available")
        else:
            

            # print(location.raw, latitude + ", " + longitude)
            context['location'] = location.address
            context['latitude'] = latitude
            context['longitude'] = longitude
            context['time'] = time
            context['date'] = date
            context['dates'] = list_times
        return render(request, 'home.html', context)
        # return redirect('home')
    else:
        
        latitude = str(result["latitude"])
        longitude = str(result["longitude"])
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)
        # location = geolocator.reverse("3.1275272211037284 , 101.59307183409135")
        # print(result['iss_position']["longitude"])
        
        # print(location, latitude + ", " + longitude)
        
    return render(request, 'home.html', context)

