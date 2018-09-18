from django.contrib import admin

from .models import Ticket, Tag

admin.site.register(Ticket)
admin.site.register(Tag)
