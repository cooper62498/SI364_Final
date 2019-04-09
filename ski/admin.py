from django.contrib import admin
from ski.models import State, Mountain, Comments,Geography,Fav
# Register your models here.

admin.site.register(State)
admin.site.register(Mountain)
admin.site.register(Comments)
admin.site.register(Geography)
admin.site.register(Fav)
