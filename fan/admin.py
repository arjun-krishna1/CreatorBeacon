from django.contrib import admin

from .models import (
    Creator,
    Fan,
    Event,
    Prize,
    Entry
)

admin.site.register(Creator)
admin.site.register(Fan)
admin.site.register(Event)
admin.site.register(Prize)
admin.site.register(Entry)
