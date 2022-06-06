from django.urls import path
from organizations import views

app_name = 'organizations'

urlpatterns = [
    path('', views.organization, name='organization'),
    path('ownerlogin/',views.owner_login,name='owner-login')

]