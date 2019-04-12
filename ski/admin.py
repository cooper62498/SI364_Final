from django.contrib import admin

from ski.models import Comments, Fav, Geography, Mountain, State

# Register your models here.

admin.site.register(State)
admin.site.register(Mountain)
admin.site.register(Comments)
admin.site.register(Geography)
admin.site.register(Fav)
