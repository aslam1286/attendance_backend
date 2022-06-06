from datetime import datetime
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance_app.models import Attendance
from accounts.models import Leave
from django.http import HttpResponse
from .filter import ListFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Case, When, Value, CharField, Subquery, OuterRef
from django.db.models.functions import Concat, LPad, Extract, Cast

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    return render(request, 'dashboard.html', {"user": request.user})

def attendance_in(request):
    user = request.user
    attendance_obj = Attendance.objects.filter(employee_id = user.id).last()

    if attendance_obj is None:
        attend_in = Attendance(
            employee_id = user.id,
            today_date = datetime.now(),
            from_time = datetime.now().strftime("%H:%M:%S"),
            to_time = 0,
            total_time = 0,
        )
        attend_in.save()
        
        return JsonResponse({'retcode': 0, 'message': 'New entry added'})
    else:
        total = 0
        new_total_time = attendance_obj.total_time.split(":")
        for ele in range(0, len(new_total_time)):
            total = total + int(new_total_time[ele])
        if total > 0:
            attend_in = Attendance(
                employee_id = user.id,
                today_date = datetime.now(),
                from_time = datetime.now().strftime("%H:%M:%S"),
                to_time = 0,
                total_time = 0,
            )
            
            attend_in.save()
            return JsonResponse({'retcode': 0, 'message': 'New entry added'})
        else:
            time_now = datetime.now().strftime("%H:%M:%S")
            FMT = '%H:%M:%S'
            t_time = datetime.strptime(time_now, FMT) - datetime.strptime(attendance_obj.from_time, FMT)
            attendance_obj.to_time = time_now
            attendance_obj.total_time = t_time
            attendance_obj.save()
            return JsonResponse({'retcode': 1})


def attendance_out(request):
    if request.method == "POST":
        user = request.user
        attend_out = Attendance.objects.filter(employee_id = user.id).last()
        if attend_out.total_time == 0:
            return JsonResponse({'retcode': 0, 'message': 'Attendance not found.'})
        else:
            time_now = datetime.now().strftime("%H:%M:%S")
            FMT = '%H:%M:%S'
            t_time = datetime.strptime(time_now, FMT) - datetime.strptime(attend_out.from_time, FMT)
            attend_out.to_time = time_now
            attend_out.total_time = t_time
            attend_out.save()
            return JsonResponse({'retcode': 1})


@method_decorator(login_required, name='dispatch')
class attendanceListFilter(ListFilter):
    model = Attendance
    fields = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    search_fields = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    ordering = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    default_sortable_by = 'id'

    def get_queryset(self, request):
        user = request.user

        attendance_expression = self.model.objects.annotate(
            get_today_date=Concat(
                LPad(
                    Cast(Extract(OuterRef('today_date'), 'day'),
                         output_field=CharField()), 2, Value('0'),
                    output_field=CharField()
                ),
                Value('-'),

                LPad(
                    Cast(Extract(OuterRef('today_date'), 'month'),
                         output_field=CharField()), 2, Value('0'),
                    output_field=CharField()
                ),
                Value('-'),

                LPad(
                    Cast(Extract(OuterRef('today_date'), 'year'),
                         output_field=CharField()), 4, Value('0'),
                    output_field=CharField()
                ),
                
            ),
        ).all()

        queryset = self.model.objects.annotate(get_today_date=Case(When(today_date__isnull=False,then=Subquery(attendance_expression.values('get_today_date')[:1])),default=Value('-'))).filter(employee_id=user.id).values(*self.fields)
        return queryset


    
def get_months_reports(request):
    id = request.POST['id']
    month = request.POST['mnt']
    attendance_obj = Attendance.objects.filter(employee_id = id, today_date__month=month).values()
    
    count = 0
    for attendance in attendance_obj:
        count = count + 1

    return JsonResponse({"month_reports": list(attendance_obj), "count": count})


@method_decorator(login_required, name='dispatch')
class monthlyAttendanceListFilter(ListFilter):
    model = Attendance
    fields = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    search_fields = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    ordering = ['id', 'get_today_date', 'from_time', 'to_time', 'total_time']
    default_sortable_by = 'id'

    def get_queryset(self, request):

        attendance_expression = self.model.objects.annotate(
            get_today_date=Concat(
                LPad(
                    Cast(Extract(OuterRef('today_date'), 'day'),
                         output_field=CharField()), 2, Value('0'),
                    output_field=CharField()
                ),
                Value('-'),

                LPad(
                    Cast(Extract(OuterRef('today_date'), 'month'),
                         output_field=CharField()), 2, Value('0'),
                    output_field=CharField()
                ),
                Value('-'),

                LPad(
                    Cast(Extract(OuterRef('today_date'), 'year'),
                         output_field=CharField()), 4, Value('0'),
                    output_field=CharField()
                ),
            ),
        ).all()

        queryset = self.model.objects.annotate(get_today_date=Case(When(today_date__isnull=False,then=Subquery(attendance_expression.filter(employee_id = request.user.id).values('get_today_date')[:1])),default=Value('-'))).values(*self.fields)
        return queryset
    
def apply_leave_for_today(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        leave = Leave(subject=subject,message=message,user_id=user_id,date=datetime.now())
        leave.save()
        leave_date_str = str(leave.date)
        leave_date = leave_date_str[0:10]
        return JsonResponse({'retcode': 1, 'b':leave_date})
    else:
        return render(request,'profile.html')
    # attendance_obj = Attendance.objects.filter(employee_id=user_id)