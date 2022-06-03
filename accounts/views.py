from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Profile


@csrf_exempt
def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('attendance_app:dashboard')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('attendance_app:dashboard')
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('attendance_app:dashboard')


@csrf_exempt
def user_profile(request):
    user = request.user
    accounts_obj = Profile.objects.filter(user_id=user).first()

    data_dict = dict()
    data_dict['first_name'] = accounts_obj.user.first_name
    data_dict['last_name'] = accounts_obj.user.last_name
    data_dict['dob'] = accounts_obj.dob
    data_dict['email'] = accounts_obj.user.email
    data_dict['dest'] = accounts_obj.dest
    data_dict['mobile_number'] = accounts_obj.mobile_number
    data_dict['city'] = accounts_obj.city
    data_dict['pincode'] = accounts_obj.pincode
    print("data_dict>>>>>", data_dict)

    return render(request,'profile.html', {'data': data_dict})
