from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register, SearchByStations, StartRide, CheckoutRide
from django.contrib import messages
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.utils import timezone


# Create your views here.

def home(request):
    stations = SearchByStations.objects.all()  # Load all stations to show in <select>
    selected_station = None
    selected_station_id = request.GET.get('station')  # Get selected station ID from form

    if selected_station_id:
        try:
            selected_station = SearchByStations.objects.get(id=selected_station_id)
        except SearchByStations.DoesNotExist:
            selected_station = None
    return  render(request,'_3galty/home.html', {'stations': stations,
        'selected_station': selected_station})



def AboutUs (request):
    return  render(request,'_3galty/AboutUs.html')



def register (request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('phone')
        mail = request.POST.get('email')
        passwordd = request.POST.get('password')

        data = Register(FirstName=first_name, LastName=last_name, phone=telephone, email=mail, password=passwordd)
        data.save()
        
        messages.success(request, 'Account has been successfuly created.')
        
        return redirect ('login')

    return render(request,'_3galty/register.html')



def login(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=mail)
            if user.password == password:
                return render(request, '_3galty/home.html')
            else:
                messages.error(request, "Invalid Password")
        except Register.DoesNotExist:
            messages.error(request, "Invalid E-mail")

        return redirect('login')

    return render(request, '_3galty/login.html')




def contact (request):
    return  render(request,'_3galty/contact.html')



def search_by_stations(request):
    stations = SearchByStations.objects.all()  # Load all stations to show in <select>
    selected_station = None
    selected_station_id = request.GET.get('station')  # Get selected station ID from form

    if selected_station_id:
        try:
            selected_station = SearchByStations.objects.get(id=selected_station_id)
        except SearchByStations.DoesNotExist:
            selected_station = None

    return render(request, '_3galty/SearchByStations.html', {
        'stations': stations,
        'selected_station': selected_station
    })




def start_ride(request):
    stations = SearchByStations.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        national_id = request.POST.get('national_id')
        start_station_id = request.POST.get('start_station')
        end_station_id = request.POST.get('end_station')
        bike_type = request.POST.get('bike_type')

        if not all([full_name, national_id, start_station_id, end_station_id, bike_type]):
            messages.error(request, "Invalid booking! Please fill all fields.")
            return redirect('StartRide')

        start_station = SearchByStations.objects.get(id=start_station_id)
        end_station = SearchByStations.objects.get(id=end_station_id)

        if bike_type == 'manual' and start_station.mNum <= 0:
            messages.error(request, "No manual bikes available at this station.")
            return redirect('StartRide')
        
        if bike_type == 'electrical' and start_station.eNum <= 0:
            messages.error(request, "No electrical bikes available at this station.")
            return redirect('StartRide')

        if bike_type == 'manual':
            start_station.mNum -= 1
        else:
            start_station.eNum -= 1

        start_station.save()

        # Save the ride
        new_ride = StartRide.objects.create(
            full_name=full_name,
            national_id=national_id,
            start_station=start_station,
            end_station=end_station,
            bike_type=bike_type,
            start_time=timezone.now()
        )

        # Save only ride ID to session
        request.session['ride_id'] = new_ride.id

        messages.success(request, "Your ride has been started!")
        return redirect('EndRide')

    return render(request, '_3galty/StartRide.html', {'stations': stations})




def end_ride(request):
    ride_id = request.session.get('ride_id')
    ride = None

    if ride_id:
        try:
            ride = StartRide.objects.get(id=ride_id)
        except StartRide.DoesNotExist:
            ride = None

    if request.method == 'POST' and ride:
        ride.end_time = timezone.now()
        ride.save()

        duration = ride.end_time - ride.start_time
        total_seconds = int(duration.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        request.session['checkout_data'] = {
            'full_name': ride.full_name,
            'national_id': ride.national_id,
            'trip_number': ride.id,
            'bike_type': ride.bike_type,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'start_time': str(ride.start_time), 
            'end_time': str(ride.end_time)      
        }

        return redirect('checkout')

    return render(request, '_3galty/EndRide.html', {'ride': ride})






def checkout(request):
    checkout_data = request.session.get('checkout_data')
    price = 0

    print("checkout_data loaded:", checkout_data)

    if checkout_data is None:
        messages.error(request, "No ride found! Please start and end a ride first.")
        return redirect('home')

    # Extract values
    days = checkout_data['days']
    hours = checkout_data['hours']
    minutes = checkout_data['minutes']
    seconds = checkout_data['seconds']
    bike_type = checkout_data['bike_type']

    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

    if bike_type == 'electrical':
       
        price += (total_seconds / 3600) * 8  

        if days >= 1:
            price = days * 50 + (hours * 8) + (minutes * 8 / 60)
            if days >= 7:
                weeks = days // 7
                remaining_days = days % 7
                price = weeks * 300 + remaining_days * 50 + (hours * 8) + (minutes * 8 / 60)

    elif bike_type == 'manual':
        price += (total_seconds / 3600) * 4  
        if days >= 1:
            price = days * 20 + (hours * 4) + (minutes * 4 / 60)
            if days >= 7:
                weeks = days // 7
                remaining_days = days % 7
                price = weeks * 100 + remaining_days * 20 + (hours * 4) + (minutes * 4 / 60)

    
    price = round(price, 2)

    checkout_data['total_price'] = price

    # Convert dictionary to object
    class CheckoutData:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)

    checkout_data = CheckoutData(checkout_data)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')

        if not payment_type or payment_type == "choose type of pay":
            messages.error(request, "Please select a payment method.")
            return redirect('checkout')

        CheckoutRide.objects.create(
            full_name=checkout_data.full_name,
            national_id=checkout_data.national_id,
            trip_number=checkout_data.trip_number,
            bike_type=checkout_data.bike_type,
            days=checkout_data.days,
            hours=checkout_data.hours,
            minutes=checkout_data.minutes,
            seconds=checkout_data.seconds,
            payment_type=payment_type,
            total_price=price,
        )

        # Clear session
        request.session.pop('checkout_data', None)
        request.session.pop('ride_id', None)

        messages.success(request, "Checkout Completed Successfully!")
        return redirect('home')

    return render(request, '_3galty/checkout.html', {'checkout_data': checkout_data})




def HowItWork (request):
    return  render(request,'_3galty/HowItWork.html')



def premium (request):
    return  render(request,'_3galty/premium.html')



def reviews (request):
    return  render(request,'_3galty/reviews.html')



def fga (request):
    return  render(request,'_3galty/fqa.html')



def PrivacyPolicy (request):
    return  render(request,'_3galty/PrivacyPolicy.html')



def TermsOfService (request):
    return  render(request,'_3galty/TermsOfService.html')

