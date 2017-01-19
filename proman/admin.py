from django.contrib import admin

from .models import Project, Team, Task

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from directmessages.models import Message
from shoutbox.models import ChatMessage

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sender','recipient', 'content', )

# ----------------------------------------------------------------
class TeamAdmin(admin.ModelAdmin):
    list_display = ('project', 'member',)


# ------------------------------------------ User Model --------------------------------------------------
class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    show_change_link = True


class UserAdmin(admin.ModelAdmin):
    inlines = [ProjectInline, ]
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('last_login', 'date_joined')}),
        ('Informacje personalne', {'fields': ('first_name', 'last_name', 'email')}),
        ('Uprawnienia', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Grupy', {'fields': ('groups',)}),
    )
    readonly_fields = ('last_login','date_joined',)

# ------------------------------------------- Project Model -------------------------------------------------
class TaskInline(admin.StackedInline):
    model = Task
    readonly_fields = ('description',)
    show_change_link = True
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    list_display = ('name','owner','startdate','enddate','id', 'passforjoin', 'complete_proc')

# ------------------------------------------ Task Model -----------------------------------


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name','project','short_description','create_date','contractor', 'weight', 'complete_proc')


# ---------------------------------------   CHAT MESSAGES ------------------------------
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'message', 'timestamp')

# ------------------------------------------- Registration ---------------------------
admin.site.unregister(Message)
admin.site.register(Message, MessageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)