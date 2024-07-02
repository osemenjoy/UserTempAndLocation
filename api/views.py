from django.shortcuts import render
from rest_framework.views import APIView
import requests
from decouple import config
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class HelloApiView(APIView):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
        
        if not client_ip:
            client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            location = geo_data.get('city', 'unknown')
        else:
            location = 'unknown'

        weather_api_key = config("WEATHER_API_KEY")
        weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={weather_api_key}')
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temp = weather_data['main']["temp"]
            temperature = f"{temp} degrees celcius"
        else:
            temperature = 'unknown'

        visitor_name = visitor_name.replace('"', '')
        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} in {location} "
        resp = Response(
            {
                "client_ip": client_ip,
                "location": location,
                "greeting": greeting
            }, status=status.HTTP_200_OK
        )        
        return resp