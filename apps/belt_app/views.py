from django.shortcuts import render, redirect
from models import Users, Trips, Joiners
from django.db.models import Count
from django.contrib import messages
import bcrypt
import re 
from datetime import date, datetime, timedelta


# Create your views here.

def index(request):
    return render(request, 'belt_app/index.html')

def register(request):

    user = Users.usersManager.add(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm'])

    if user[0] == False:
        for message in user[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['user_id'] = user[1].id 
        print "successful registration"
        return redirect('/success')

def login(request):
    
    user = Users.usersManager.login(request.POST['email'], request.POST['password'])

    if user[0] == False:
        for message in user[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['user_id'] = user[1].id
        return redirect('/success')

def success(request):

    user = Users.usersManager.get(id=request.session['user_id'])
    trips = Trips.objects.all()

    context = {
        "user" : user,
        "trips" : trips
    }
    return render(request, 'belt_app/success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/success')

def addtrip(request):
    return render(request, 'belt_app/addtrip.html')

def create(request):

    destination = request.POST['destination']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    plan = request.POST['plan']

    user = Users.usersManager.get(id=request.session['user_id'])

    startcheck = datetime.strptime(start_date, '%Y-%m-%d')
    if datetime.strptime(start_date, '%Y-%m-%d') <= datetime.now():
        print "Start must be after today's date"
        return redirect('/success')

    endcheck = datetime.strptime(end_date, '%Y-%m-%d')
    if datetime.strptime(end_date, '%Y-%m-%d') <= datetime.now():
        print "End must be after today's date"
        return redirect('/success')

    trip = Trips.objects.create(destination=destination,start_date=start_date,end_date=end_date,plan=plan,user=user)
  
    return redirect('/success')

def destination(request,id):

    trip = Trips.objects.get(id=id)
    u = Users.usersManager.filter(id=id)
    joiners = Joiners.objects.all()
    
    
    destination = trip.destination
    start = trip.start_date
    end = trip.end_date
    plan = trip.plan
    userfirst = trip.user.first_name
    userlast = trip.user.last_name
    this = trip.id
    
    context = {
        "this" : this,
        "destination" : destination,
        "start" : start,
        "end" : end,
        "plan" : plan,
        "userfirst" : userfirst,
        "userlast" : userlast,
        "joiners" : joiners
    }

    print context
    
    return render(request, 'belt_app/trip.html', context)


def join(request, trip_id):

    joiners = Joiners.objects.filter(user_id = request.session['user_id']).filter(trip_id=trip_id)

    if len(joiners) == 0:
        user = Users.usersManager.get(id=request.session['user_id'])
        trip = Trips.objects.get(id=trip_id)

        joiner = Joiners.objects.create(user=user,trip=trip)
        print "successfully joined"
        return redirect('/success')
    
    else:
        print"You already joined this trip"
        return redirect('/success')

