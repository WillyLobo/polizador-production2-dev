from django.contrib import admin
from fallout.models import CharFallout

class FalloutAdmin(admin.ModelAdmin):
    pass

admin.site.register(CharFallout, FalloutAdmin)
