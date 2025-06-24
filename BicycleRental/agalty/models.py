from django.db import models
from django.utils import timezone

# Create your models here.

class Register(models.Model):
    FirstName = models.CharField(blank=False, max_length=20, default='Ahmed', verbose_name='First Name')
    LastName = models.CharField(blank=False, max_length=20, default = 'Nazeer', verbose_name='Last Name')
    phone = models.IntegerField(null=False, max_length=11, default = '01556162788', verbose_name='Phone')
    email = models.EmailField(null=False, max_length=100, default = 'ahmed.m.nazeer.18@gmail.com', verbose_name='E-mail')
    password = models.CharField(null=False, max_length=50, default = '123', verbose_name='Password')
    
    def __str__(self):
        return self.FirstName + " " + self.LastName
    

    class Meta:
        verbose_name = 'Register'
        ordering = ['FirstName']




class SearchByStations(models.Model):
    class Meta:
        verbose_name = 'Search By Stations'
        ordering = ["stationName"]
        
    def __str__(self):
        return self.stationName
    
    stationName = models.CharField(max_length=255)
    eNum = models.IntegerField()
    mNum = models.IntegerField()



class StartRide(models.Model):
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=14)
    start_station = models.ForeignKey('SearchByStations', on_delete=models.CASCADE, related_name='start_station')
    end_station = models.ForeignKey('SearchByStations', on_delete=models.CASCADE, related_name='end_station')
    bike_type = models.CharField(max_length=50, choices=[('manual', 'Manual'), ('electrical', 'Electrical')])
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Start Ride'
        verbose_name_plural = 'Start Rides'
        ordering = ['-full_name']

    def __str__(self):
        return f"{self.full_name} - {self.start_station.stationName} to {self.end_station.stationName}"


class CheckoutRide(models.Model):
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=14)
    trip_number = models.IntegerField()  # Link to StartRide trip ID
    bike_type = models.CharField(max_length=50)
    days = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    seconds = models.IntegerField(default=0)
    payment_type = models.CharField(max_length=100, default='Not selected')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.full_name} | Trip #{self.trip_number}"
    
