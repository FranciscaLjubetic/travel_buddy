from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from main.decorators import login_required
from main.models import User, Travel
from django.db import IntegrityError
from django.db.models import Q


@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

@login_required
def travels(request):
    your_id = request.session['user']['id']
    you = User.objects.get(id = your_id)
    your_total_travels = Travel.objects.filter(Q(creator = you) | Q(travellers = you)) 
    other_users_travels = [trip for trip in Travel.objects.all() if trip not in your_total_travels]
    context = {
        'other_users_travels': other_users_travels,
        'your_total_travels': your_total_travels,
    }
    return render(request, 'travels.html', context)

@login_required
def travelsadd(request):
    if request.method == 'GET':
    
        return render(request, 'travelsadd.html')
    
    else:
        desti= request.POST['destination']
        description =request.POST['description']
        travel_from =request.POST['travel_from']
        travel_to = request.POST['travel_to']
        creator_id = request.session['user']['id']
        new_creator = User.objects.get(id = creator_id)
        
        errors = Travel.objects.basic_validator(request.POST)
    
        old_travels = Travel.objects.filter(destination= desti)
        if len(old_travels) > 0:
            messages.error(request,"This trip already exists.")
            return redirect("/travelsadd")
    
        if len(errors) > 0:
            for llave, error_message in errors.items():
                messages.error(request, error_message)
            return redirect('/travelsadd') 

        try:
            Travel.objects.create(destination = desti, description = description, travel_from = travel_from, travel_to = travel_to, creator = new_creator)
        except IntegrityError:
            messages.error(request, 'Please, try with a new trip.')
            return redirect('/travelsadd')

    messages.success(request, 'Travel successfully created')
    return redirect('/travels')
    

@login_required
def destination(request, nam):
    your_id = request.session['user']['id']
    you = User.objects.get(id = your_id)
    this_travel = Travel.objects.get(id = int(nam))
    this_travel_travellers_without_you = User.objects.filter(travels = this_travel).exclude(id = your_id)
    context = {
        'this_travel': this_travel,
        'this_travel_travellers_without_you': this_travel_travellers_without_you,
    }
    return render(request, 'destination.html', context)

@login_required
def cancel(request, nem):
    this_travel = Travel.objects.get(id = int(nem))
    your_id = request.session['user']['id'] 
    you= User.objects.get(id = your_id)
    this_travel_travellers = User.objects.filter(travels = this_travel)
    if you not in this_travel_travellers:
        messages.error(request,"You cannot cancel twice.")
        return redirect('/travels')
    this_travel.travellers.remove(you)	
    #you.travels.remove(this_travel)
    this_travel.save()
    #you.save()
    return redirect('/travels')

@login_required
def delete(request, nim):
    this_travel = Travel.objects.get(id = int(nim))
    del this_travel
    return redirect('/travels')

@login_required
def joining(request, nim):
    this_travel = Travel.objects.get(id = int(nim))
    your_id = request.session['user']['id'] 
    you= User.objects.get(id = your_id)
    #si you ya esta como traveller de este viaje, tirarle error
    this_travel_travellers = User.objects.filter(travels = this_travel)
    for guy in this_travel_travellers:
        if guy.id == your_id:
            messages.error(request,"You are already in.")
            return redirect("/travels")
        
    this_travel.travellers.add(you)
    messages.success(request,"Now you are already in.")
    this_travel.save()
    return redirect('/travels')
