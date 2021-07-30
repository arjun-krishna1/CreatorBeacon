from django.contrib import admin

from .models import Creator, Fan, Event


admin.site.register(Creator)
admin.site.register(Fan)
admin.site.register(Event)
