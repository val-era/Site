
from django.contrib import admin
from .models import Message, Photo, ToJson

admin.site.register(Message)
admin.site.register(Photo)
admin.site.register(ToJson)
