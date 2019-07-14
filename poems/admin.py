from django.contrib import admin
from .models import Poem, ChangePassword, Rating, Review, Notification

# Register your models here.

admin.site.register(Poem)
admin.site.register(ChangePassword)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Notification)
