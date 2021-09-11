from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('travelsadd', views.travelsadd),
    path('travels/destination/<nam>', views.destination),
    path('cancel/<nem>', views.cancel),
    path('delete/<nim>', views.delete),
    path('joining/<nam>', views.joining),
]
