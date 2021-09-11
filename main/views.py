from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from main.decorators import login_required
from main.models import User, Travel
from django.db import IntegrityError


@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

def travels(request):
    travels = Travel.objects.all()
    you_id = request.session['user']['id']
    you = User.objects.get(id = you_id)
    your_travels = Travel.objects.filter (travellers = you)
    your_created_travels = Travel.objects.filter (creator = you)
    other_users_travels = [trip for trip in Travel.objects.all() if trip.id not in your_travels]
    context = {
        'your_travels': your_travels,
        'your_created_travels':your_created_travels,
        'other_users_travels': other_users_travels,
    }
    return render(request, 'travels.html', context)

def travelsadd(request):
    #errors = Travel.objects.basic_validator(request.POST)
    if request.method == 'GET':
    
        return render(request, 'travelsadd.html')
    
    else:
        destination= request.POST['destination']
        description =request.POST['description']
        travel_from =request.POST['travel_from']
        travel_to = request.POST['travel_to']
        creator_id = request.session['user']['id']
        new_creator = User.objects.get(creator = creator_id)
        first_participant = User.objects.get(creator = creator_id)
        
    #errors = Users.objects.basic_validator(request.POST)
    
    '''
    if len(errors) > 0:
        for llave, error_message in errors.items():
            messages.error(request, error_message)
        return redirect('/travelsadd')
    '''

    try:
        Travel.objects.create(destination = destination, description = description, travel_from = travel_from, travel_to = travel_to, creator = new_creator, travellers = first_participant )
    except IntegrityError:
        messages.error(request, 'This travel already exist')
        return redirect('/travelsadd')

    messages.success(request, 'Travel successfully created')
    return redirect('/travels')
    

def destination(request, nam):
    this_travel = Travel.objects.get(id = int(nam))
    this_travel_users = User.objects.filter(travel = this_travel)
    
    context = {
        'this_travel': this_travel,
        'this_travel_users': this_travel_users,
    }
    return render(request, 'destination.html', context)

def cancel(request, nem):
    this_travel = Travel.objects.get(id = int(nem))
    your_id = request.session['user']['id'] 
    you= User.objects.get(creator = your_id)
    #travel_to_cancel = Travel.objects.filter(travellers = you)
    this_travel.travellers.remove(you)	
    you.travels.remove(this_travel)
    this_travel.save()
    you.save()
    return redirect('/travels')

def delete(request, nim):
    this_travel = Travel.objects.get(id = int(nim))
    del this_travel
    return redirect('/travels')

def joining(request, nam):
    this_travel = Travel.objects.get(id = int(nim))
    your_id = request.session['user']['id'] 
    you= User.objects.get(creator = your_id)
    this_travel.travellers.add(you)
    return redirect('/travels')
