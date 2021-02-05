from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User

import time
import re
from datetime import datetime
import json
import requests
from .forms import UserRegisterForm
from .models import *
from .util import *


#from django.contrib.sessions.models import Session
#Session.objects.all().delete()


def index(request):
    if request.user.is_authenticated:
        return render(request, 'weatherdata/index.html')
    else:
        return redirect('login')



def current_weather(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            city_name = request.POST.get('city')
            measurement_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            display_time = datetime.now().strftime("%H:%M %p, %d-%m-%Y")
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID=####'
            response = requests.get(url)
            response_object = response.json()

            if response:
                context = {
                    'http_response': response_object['cod'],
                    'city_name': response_object['name'],
                    'country': response_object['sys']['country'],
                    'measurement_time': measurement_time,
                    'display_time': display_time,
                    'temperature': round(response_object['main']['temp']),
                    'feels_like': round(response_object['main']['feels_like']),
                    'wind_speed': response_object['wind']['speed'],
                    'wind_direction': response_object['wind']['deg'] + 180,
                    'pressure': response_object['main']['pressure'],
                    'humidity': response_object['main']['humidity'],
                    'visibility': round(response_object['visibility'] / 1000, 2),
                    'info_main': response_object['weather'][0]['main'],
                    'info_description': response_object['weather'][0]['description'],
                    'info_icon': response_object['weather'][0]['icon']
                }

                return render(request, 'weatherdata/current_weather.html', context)
            else:
                messages.warning(request, 'No data for a given city, please try again.')

        return render(request, 'weatherdata/current_weather.html')
    else:
        return redirect('login')



def five_day_weather(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            city_name = request.POST.get('city')
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&APPID=####'
            response = requests.get(url)
            response_object = response.json()

            if response:
                context = {
                    'http_response': response_object['cod'],
                    'five_day_forecast': response_object['list'],
                    'city': city_name.title()
                }

                return render(request, 'weatherdata/five_day_weather.html', context)
            else:
                messages.warning(request, 'No data for a given city, please try again.')

        return render(request, 'weatherdata/five_day_weather.html')
    else:
        return redirect('login')



def nearest_installations(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            city_name = request.POST.get('city')
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key=####'
            geocode_api_response = requests.get(geocode_url)

            if geocode_api_response.json()['results']:
                lat = geocode_api_response.json()['results'][0]['geometry']['location']['lat']
                lng = geocode_api_response.json()['results'][0]['geometry']['location']['lng']

                airly_url = f'https://airapi.airly.eu/v2/installations/nearest?lat={lat}&lng={lng}&maxDistanceKM=3&maxResults=-1'
                headers = {
                    'apikey': '####'
                }
                response = requests.get(airly_url, headers=headers)

                response_object = response.json()

                if response_object:
                    context = {
                        'nearest_installations': response_object
                    }

                    return render(request, 'weatherdata/nearest_installations.html', context)
                else:
                    messages.warning(request, 'No data for a given city, please try again.')
            else:
                messages.warning(request, 'Invalid name of the city or town, please try again.')

        return render(request, 'weatherdata/nearest_installations.html')
    else:
        return redirect('login')




def current_air_quality(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            city_name = request.POST.get('city')
            measurement_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            display_time = datetime.now().strftime("%H:%M %p, %d-%m-%Y")

            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key=####'
            geocode_api_response = requests.get(geocode_url)

            if geocode_api_response.json()['results']:
                lat = geocode_api_response.json()['results'][0]['geometry']['location']['lat']
                lng = geocode_api_response.json()['results'][0]['geometry']['location']['lng']

                airly_url = f'https://airapi.airly.eu/v2/measurements/nearest?lat={lat}&lng={lng}'
                headers = {
                    'apikey': '####'
                }
                response = requests.get(airly_url, headers=headers)
                response_object = response.json()

                if not 'errorCode' in response_object:
                    context = {
                        'http_response': HttpResponse.status_code,
                        'city_name': city_name,
                        'measurement_time': measurement_time,
                        'display_time': display_time,
                        'pm1': response_object['current']['values'][0]['value'],
                        'pm25': response_object['current']['values'][1]['value'],
                        'pm10': response_object['current']['values'][2]['value'],
                        'pm25_limit': response_object['current']['standards'][0]['limit'],
                        'pm10_limit': response_object['current']['standards'][1]['limit'],
                        'index_value': round(response_object['current']['indexes'][0]['value']),
                        'index_level': response_object['current']['indexes'][0]['level'],
                        'index_description': response_object['current']['indexes'][0]['description'],
                        'index_color': response_object['current']['indexes'][0]['color']
                    }

                    return render(request, 'weatherdata/air_quality.html', context)
                else:
                    messages.warning(request, 'No data for a given city, please try again.')
            else:
                messages.warning(request, 'Invalid city name, please try again.')

        return render(request, 'weatherdata/air_quality.html')
    else:
        return redirect('login')



def save_data_in_db(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)

            data_type = data['data']['data_type']

            if data_type == 'current_weather':
                temperature = float(data['data']['temperature'])
                feels_like = float(data['data']['feels_like'])
                visibility = float(data['data']['visibility'])
                wind_speed = float(data['data']['wind_speed'])
                wind_direction = int(data['data']['wind_direction'])

                current_weather = CurrentWeather.objects.create(
                    user=request.user,
                    city_name=data['data']['city_name'],
                    country=data['data']['country'],
                    temperature=round(temperature),
                    feels_like=round(feels_like),
                    wind_speed=round(wind_speed),
                    wind_direction=round(wind_direction),
                    pressure=data['data']['pressure'],
                    humidity=data['data']['humidity'],
                    visibility=visibility,
                    main=data['data']['main'],
                    description=data['data']['description'],
                    icon=data['data']['icon'],
                    measurement_time=data['data']['measurement_time'],
                )

            elif data_type == 'current_air':
                current_air_quality = CurrentAirQuality.objects.create(
                    user=request.user,
                    city_name=data['data']['city_name'].title(),
                    pm1=float(data['data']['pm1']),
                    pm25=float(data['data']['pm25']),
                    pm10=float(data['data']['pm10']),
                    index_value=float(data['data']['index_value']),
                    index_level=data['data']['index_level'],
                    index_description=data['data']['index_description'],
                    index_color=data['data']['index_color'],
                    measurement_time=data['data']['measurement_time']
                )

            return JsonResponse({}, safe=False)



def delete_single_weather_data(request, id):
    if request.user.is_authenticated:
        CurrentWeather.objects.filter(id=id).delete()

        return redirect('profile', user=request.user)



def delete_all_weather_data(request):
    if request.user.is_authenticated:
        CurrentWeather.objects.filter(user=request.user).delete()

        return redirect('profile', user=request.user)



def delete_single_air_data(request, id):
    if request.user.is_authenticated:
        CurrentAirQuality.objects.filter(id=id).delete()

        return redirect('profile', user=request.user)



def delete_all_air_data(request):
    if request.user.is_authenticated:
        CurrentAirQuality.objects.filter(user=request.user).delete()

        return redirect('profile', user=request.user)



def profile_page(request, user):
    if request.user.is_authenticated:
        temperature_data = CurrentWeather.objects.filter(user=request.user).values('id', 'user', 'city_name', 'country', 'temperature', 'feels_like', 'wind_speed', 'wind_direction', 'pressure', 'humidity', 'visibility', 'measurement_time').order_by('-measurement_time')
        air_data = CurrentAirQuality.objects.filter(user=request.user).values('id', 'user', 'city_name', 'pm1', 'pm25', 'pm10', 'measurement_time').order_by('-measurement_time')

        context = {
            'temperature_data': temperature_data,
            'air_data': air_data,
            'files': list_files_info()
        }

        return render(request, 'weatherdata/profile_page.html', context)



def save_weatherdata_in_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            filename = request.POST['filename-input']

            if not filename:
                messages.warning(request, 'Fill in the name of the file you want to save and try again.')
                return redirect('profile', user=request.user)

            if re.search('^[0-9]', filename):
                messages.warning(request, 'Incorrect file name, please try again.')
                return redirect('profile', user=request.user)
            elif f'{filename}.xlsx' in list_filenames():
                messages.warning(request, f'File with name "{filename}" already exist, please try again.')
                return redirect('profile', user=request.user)
            else:
                weather_data = CurrentWeather.objects.filter(user=request.user).values('city_name', 'country', 'temperature', 'feels_like', 'wind_speed', 'wind_direction', 'pressure', 'humidity', 'visibility', 'measurement_time')
                print(weather_data)
                save_as_excel_file(filename, weather_data)
                messages.success(request, f'Weather data has been successfully saved in "{filename}.xlsx" file.')
                return redirect('profile', user=request.user)



def save_airdata_in_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            filename = request.POST['filename-input']

            if not filename:
                messages.warning(request, 'Fill in the name of the file you want to save and try again.')
                return redirect('profile', user=request.user)

            if re.search('^[0-9]', filename):
                messages.warning(request, 'Incorrect file name, please try again.')
                return redirect('profile', user=request.user)
            elif f'{filename}.xlsx' in list_filenames():
                messages.warning(request, f'File with name "{filename}" already exist, please try again.')
                return redirect('profile', user=request.user)
            else:
                air_data = CurrentAirQuality.objects.filter(user=request.user).values('city_name', 'pm1', 'pm25', 'pm10', 'measurement_time')
                save_as_excel_file(filename, air_data)
                messages.success(request, f'Air data has been successfully saved in "{filename}.xlsx" file.')
                return redirect('profile', user=request.user)



def open_excel_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        open_file(data['data'])

        return JsonResponse({}, safe=False)



def delete_excel_file(request, filename):
    delete_file(filename)
    messages.info(request, f'File "{filename}" has been deleted.')

    return redirect('profile', user=request.user)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully loged in.')
            return redirect('index')
        else:
            messages.warning(request, 'Wrong username and/or password.')
            return render(request, "weatherdata/login.html")
    else:
        return render(request, "weatherdata/login.html")



def logout_view(request):
    logout(request)
    return redirect('login')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account has been successfully created.')
            return redirect('login')
        else:
            messages.warning(request, 'Incorrect data, try again.')

    else:
        form = UserRegisterForm()

    return render(request, 'weatherdata/register.html', {'form': form})
