from operator import imod
from django.urls import path
from attendance_app import views
from attendance_app.views import dashboard

app_name = 'attendance_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.attendanceListFilter.as_view(), name='attendance_list'),
    path('month-list/', views.monthlyAttendanceListFilter.as_view(), name='monthly_attendance_list'),
    path('attend-in', views.attendance_in, name='attend_in'),
    path('attend-out', views.attendance_out, name='attend_out'),
    path('month-repo', views.get_months_reports, name='get_months_report'),
    path('apply-leave-today', views.apply_leave_for_today, name='apply_leave_for_today'),
]
