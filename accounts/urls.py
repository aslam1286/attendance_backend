from operator import imod
from django.urls import path
from accounts import views
from attendance_app.views import dashboard

app_name = 'accounts'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('profile', views.user_profile, name='user_profile'),
    
]
