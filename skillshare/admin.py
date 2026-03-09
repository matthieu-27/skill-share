from django.contrib import admin  # type: ignore

from .models import Category, CustomUser, Schedule, Skill

# Register your models here.
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Schedule)
admin.site.register(CustomUser)
