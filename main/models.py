from django.db import models
import re
from datetime import date, datetime



# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors
    

class travelmanager(models.Manager):
    def basic_validator(self, post_data):
        errors ={}
        #today = date.today()
        if len(post_data['destination']) < 2: 
            errors['destination'] = 'IGDAF, write a decent title'

        if len(post_data['description']) < 15:
            errors['description'] = 'Description should have at least fifteen characters'
        
        if datetime.strptime(post_data['travel_from'],"%Y-%m-%d").date() > datetime.strptime(post_data['travel_to'],"%Y-%m-%d").date():
            errors['travel_to'] = 'Better Talk to Marty Mc Fly'
            
        if datetime.strptime(post_data['travel_from'],"%Y-%m-%d").date() < datetime.today().date():
            errors['travel_from'] = 'Your departure should be later than today'
            
        return errors 


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES, default='user')  
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
    
    
class Travel(models.Model):
    destination= models.CharField(max_length=100)
    description = models.TextField()
    travel_from = models.DateField()
    travel_to = models.DateField()
    creator = models.ForeignKey(User, related_name="created_travels", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    travellers = models.ManyToManyField(User, related_name='travels') 
    objects = travelmanager()
    
    
    def __str__(self):
        return f"{self.destination}"

    def __repr__(self):
        return f"{self.destination}"