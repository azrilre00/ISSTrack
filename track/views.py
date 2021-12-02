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
        time = request.POST['time']
        
        datetimes_ISS = str(date + " " + time)
        date_time_obj = datetime.strptime(datetimes_ISS, '%Y-%m-%d %H:%M')
        times = datetime.timestamp(date_time_obj)

        list_times_after = []
        list_times_before = []
        t1 = date_time_obj

        for i in range(5):
            time_b4 = t1 + timedelta(minutes=10)
            list_times_after.append(time_b4)
            t1 = time_b4

        for i in range(5):
            time_b4 = date_time_obj + timedelta(minutes=-10)
            list_times_before.append(time_b4)
            date_time_obj = time_b4
        # print(date_time_obj)
        # print(type(date_time_obj))
        # print(times)
        # print(list_times)
        urltime = url + "?timestamp=" + str(times)
        response = urllib.request.urlopen(urltime) 
        result = json.loads(response.read())

        latitude = str(result["latitude"])
        longitude = str(result["longitude"])

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)

        for i in list_times_after:
            print(i)

        
        if location == None:
            print("The ISS location probably in a location where coverage is not available")
        else:
            # print(location.raw, latitude + ", " + longitude)
            context['location'] = location.address
            context['latitude'] = latitude
            context['longitude'] = longitude
            context['time'] = time
            context['date'] = date
            context['dates_after'] = list_times_after
            context['dates_before'] = list_times_before
        return render(request, 'home.html', context)
        # return redirect('home')
    return render(request, 'home.html', context)


def after_date(request, date, times):
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    response = urllib.request.urlopen(url) 
    result = json.loads(response.read())
    list_times_after = []
    list_times_before = []
    t1 = date


    for i in range(5):
        time_b4 = t1 + timedelta(minutes=10)
        list_times_after.append(time_b4)
        t1 = time_b4
        urltime = url + "?timestamp=" + str(times)
        response = urllib.request.urlopen(urltime) 
        result = json.loads(response.read())

        latitude = str(result["latitude"])
        longitude = str(result["longitude"])

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude+", "+longitude)

        
