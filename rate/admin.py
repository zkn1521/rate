from django.contrib import admin

# Register your models here.
from rate.models import Module, Professor, ModuleInstance

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(ModuleInstance)