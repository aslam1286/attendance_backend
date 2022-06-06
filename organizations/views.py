from django.shortcuts import render

def organization(request):
    return render(request,'organization.html')

def owner_login(request):
    return render(request,'ownerlogin.html')