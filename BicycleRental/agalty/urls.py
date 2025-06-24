from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('AboutUs', views.AboutUs, name = 'AboutUs'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('HowItWork', views.HowItWork, name = 'HowItWork'),
    path('checkout', views.checkout, name = 'checkout'),
    path('contact', views.contact, name = 'contact'),
    path('StartRide', views.start_ride, name = 'StartRide'),
    path('EndRide', views.end_ride, name = 'EndRide'),
    path('SearchByStations', views.search_by_stations, name = 'SearchByStations'),
    path('premium', views.premium, name = 'premium'),
    path('reviews', views.reviews, name = 'reviews'),
    path('fga', views.fga, name = 'fga'),
    path('PrivacyPolicy', views.PrivacyPolicy, name = 'PrivacyPolicy'),
    path('TermsOfService', views.TermsOfService, name = 'TermsOfService'),
]
