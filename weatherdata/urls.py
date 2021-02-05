from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current', views.current_weather, name='current_weather'),
    path('five_day_weather', views.five_day_weather, name='five_day_weather'),
    path('installations', views.nearest_installations, name='installations'),
    path('air_quality', views.current_air_quality, name='air_quality'),

    path('save_in_db', views.save_data_in_db),
    path('delete_single_weather/<int:id>', views.delete_single_weather_data, name='delete_single_weather'),
    path('delete_all_weather', views.delete_all_weather_data, name='delete_all_weather'),
    path('delete_single_air/<int:id>', views.delete_single_air_data, name='delete_single_air'),
    path('delete_all_air', views.delete_all_air_data, name='delete_all_air'),
    path('save_weatherdata', views.save_weatherdata_in_file, name='save_weatherdata'),
    path('save_airdata', views.save_airdata_in_file, name='save_airdata'),
    path('open_file', views.open_excel_file),
    path('delete_file/<str:filename>', views.delete_excel_file, name="delete_file"),

    path('profile/<str:user>', views.profile_page, name='profile'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register')
]
