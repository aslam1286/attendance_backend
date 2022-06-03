from django.urls import path
from organizations import views

app_name = 'organizations'

urlpatterns = [
    path('', views.organization, name='organization'),

]