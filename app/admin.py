from django.contrib import admin
from .models import ToDo
#from django_boost.admin import LogicalDeletionModelAdmin


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_datetime', 'updated_datetime')
    list_display_links = ('id', 'title')

admin. site.register(ToDo, ToDoAdmin)

# @admin.register(ToDo)
# class MyModelAdmin(LogicalDeletionModelAdmin):
#     pass

# Register your models here.
