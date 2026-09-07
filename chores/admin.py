from django.contrib import admin
from .models import Member, Chore, Assignment


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'frequency_days', 'effort_points')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('chore', 'member', 'due_date', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'due_date')
