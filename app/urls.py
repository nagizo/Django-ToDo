from django.urls import path
from django.views.generic.edit import CreateView
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>',views.DetailView.as_view(), name='detail'),
    path('new_memo', views.CreateView.as_view(), name='new_memo'),
    path('delete_memo/<int:pk>', views.DeleteView.as_view(), name='delete_memo'),
    path('edit_memo/<int:pk>',views.UpdateView.as_view(), name='edit_memo'),
    path('contact/', views.contact,name='contact_form'), #お問合せページ
    path('contact/result/', views.result, name='contact_result'),#お問合わせ後のフォーム
    path('week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path('week_with_schedule/<int:year>/<int:month>/<int:day>/',views.WeekWithScheduleCalendar.as_view(),name='week_with_schedule'), 
    path('month_with_schedule/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    
    #path('flag_memo',views.ListView.as_view(), name='flag_memo'),
 
]