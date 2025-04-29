from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

class CategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.TextField: {'widget': TinyMCE()},
            }



admin.site.register(Category,CategoryAdmin)
admin.site.register(MexicanCuisine)
admin.site.register(FrenchCuisine)
admin.site.register(PakistaniCuisine)
admin.site.register(ItalianCuisine)
admin.site.register(TurkishCuisine)
admin.site.register(UserOrder)
admin.site.register(SavedCarts)
