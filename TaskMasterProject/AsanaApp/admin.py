from django.contrib import admin
from .models import Task,Team,Project,Comment

# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Comment)