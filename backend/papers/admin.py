from django.contrib import admin
from .models import CustomUser, Paper


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'teacher', 'status', 'submission_date')
    list_filter = ('status', 'field')
    search_fields = ('title', 'keywords', 'student__username', 'teacher__username')
    ordering = ('-submission_date',)
