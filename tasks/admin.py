from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'is_done')
    list_filter = ('is_done',)
    search_fields = ('title', 'text')