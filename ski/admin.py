from django.contrib import admin
from ski.models import State, Mountain, Comments,Geography
# Register your models here.

admin.site.register(State)
admin.site.register(Mountain)
admin.site.register(Comments)
admin.site.register(Geography)
