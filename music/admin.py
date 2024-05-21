from django.contrib import admin
from .models import *

# Register your models here.
class MusicAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
         'updated_at',
         'serial_num',
         'music',
         'type',
     )

class MusicImageAdmin(admin.ModelAdmin):
        list_display = (
         'id',
         'created_at',
         'updated_at',
         'image',
         'merge_music',
         'latitude',
         'longitude',
     )
        
admin.site.register(Music,MusicAdmin)
admin.site.register(MusicImage,MusicImageAdmin)
