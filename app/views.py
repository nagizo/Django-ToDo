from calendar import calendar
from typing import Generic
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy
from django import forms
from .models import ToDo
from django.shortcuts import get_object_or_404
from .forms import ToDoForm
from django.shortcuts import render, redirect
from django. views.decorators.http import require_POST
from django.views import generic 
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import ContactForm 
from django.conf import settings
import textwrap
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordContextMixin)
from .forms import (LoginForm)
from django.core.exceptions import PermissionDenied
from django.db.models import Q, query
from . import mixins
from django.contrib.auth import views as auth_views
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from .forms import LoginForm
from django.contrib.sites.shortcuts import get_current_site


class IndexView(generic.ListView):
    model = ToDo
    template_name = 'app/index.html'
    # queryset = ToDo.objects.alive()

    def index(request):
        todo = ToDo.objects.order_by('time')
        
        """検索機能の処理"""
        keyword = request.GET.get('keyword')

        if keyword:
            todo = todo.filter(
                Q(title__icontains=keyword)
            )

    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            object_list = ToDo.objects.filter(title=q_word)
        else:
            if self.request.user.is_authenticated:
                object_list = ToDo.objects.filter(author=self.request.user)
            else:
                object_list = ToDo.objects.all()
        return object_list


class DetailView(generic.DetailView):
    model = ToDo
    template_name = 'app/detail.html'



class CreateView(generic.CreateView):
    form_class = ToDoForm
    template_name = 'app/new_memo.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
        

    def user_add(request):
        form = ToDoForm()
        return render(request, 'app/new_memo.html', context={'form': form})
            
@require_POST
def delete_memo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    todo.delete()
    # object = ToDo.objects.get(id=1)
    # object.delete(hard=True)

    return redirect('app:index')

class DeleteView(generic.edit.DeleteView):
    model = ToDo
    success_url = reverse_lazy('app:index')
    template_name = 'app/delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)


def edit_memo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    if request.method == "POST":
        form = ToDoForm(request.POST, instsnce=todo)
        form.save()
        return redirect('app:index')
    else:
        form = ToDoForm(instance=todo)
    return render(request, 'app/edit_memo.html',{'form': form, 'todo':todo })

class UpdateView(LoginRequiredMixin,generic.UpdateView):
    model = ToDo
    template_name = 'app/edit_memo.html'
    form_class = ToDoForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

#お問い合わせ
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']
        subject = 'お問合わせありがとうございます。'
        contact = textwrap.dedent('''
        ※このメールはシステムからの自動返信です。

        {name} 様
        
        お問い合わせありがとうございます。
        以下の内容でお問い合わせを受け付けました。
        内容を確認させていただき、ご返信させていただきますので、少々お待ちください。

        ----------------------------------

        ・お名前
        {name}

        ・メールアドレス
        {email}

        ・メッセージ
        {message}
        -----------------------------------
        株式会社　〇〇
        〒000-0000
        〇〇県〇〇市〇〇区〇〇1-0-0
        TEL 123-456-7890
        営業時間 8:00~17:00（月~金）
        WEB: https://www.......com/
        ''').format(
        name=name,
        email=email,
        message=message
    
        )
        to_list = [email]
        bcc_list = [settings.EMAIL_HOST_USER]
        try:
            message =  EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
            message.send()
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました。')
        return redirect('app:result')

    return render(request, 'contact/contact_form.html',{'form': form})

def result(request):
    return render(request, 'contact/contact_result.html')

class Login(LoginView):
    """"ログインぺージ"""
    form_class = LoginForm
    template_name = 'registration/login.html'

class Logout(LogoutView):
    """"ログアウトページ"""
    template_name = 'registration/logged_out.html'

class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダー"""
    template_name = 'app/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class WeekCalendar(mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダー"""
    template_name = 'app/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context
        

class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'app/week_with_schedule.html'
    model = ToDo
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        context['week_row'] = zip(
            calendar_context['week_names'],
            calendar_context['week_days'],
            calendar_context['week_day_schedules'].values()
        )
        return context

class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = ToDo
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

