from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Post, Recommandation, Reaction, Evenement, Stage, Logement, Transport, EvenClub, EventSocial,TransportRequest

admin.site.unregister(User)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post)
admin.site.register(Recommandation)
admin.site.register(Reaction)
admin.site.register(Evenement)
admin.site.register(Stage)
admin.site.register(Logement)
admin.site.register(Transport)
admin.site.register(EvenClub)
admin.site.register(EventSocial)
admin.site.register(TransportRequest)