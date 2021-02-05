from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class CurrentWeather(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(default='', max_length=256)
    country = models.CharField(default='', max_length=256)
    temperature = models.IntegerField(default=0, blank=True, verbose_name='Temperature (C)')
    feels_like = models.IntegerField(default=0, blank=True)
    wind_speed = models.IntegerField(default=0, blank=True)
    wind_direction = models.IntegerField(default=0, blank=True)
    pressure = models.IntegerField(default=0, blank=True)
    humidity = models.IntegerField(default=0, blank=True)
    visibility = models.DecimalField(default=0, blank=True, max_digits=6, decimal_places=2)
    main = models.CharField(default='', max_length=256)
    description = models.CharField(default='', max_length=256)
    icon = models.CharField(default='', max_length=256)
    measurement_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'current weather {self.measurement_time}'


class CurrentAirQuality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(default='', max_length=256)
    pm1 = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    pm25 = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    pm10 = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    index_value = models.IntegerField(default=0, blank=True)
    index_level = models.CharField(default='', max_length=256)
    index_description = models.CharField(default='', max_length=256)
    index_color = models.CharField(default='', max_length=256)
    measurement_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'air quality {self.measurement_time}'
