from django.contrib import admin
from .models import Character, Tamagotchi, Feeding, Photo, Skill

# Register your models here.
admin.site.register(Character)
admin.site.register(Tamagotchi)
admin.site.register(Feeding)
admin.site.register(Photo)