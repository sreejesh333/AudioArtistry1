from django.db import models

# Create your models here.
from AudioArtistry.models import TimestampedUUIDModel



class Music(TimestampedUUIDModel):
    SINGLE = "Single"
    INTERVAL = "Interval"
    CHORDONE = "Chord_one"
    CHORDTWO = "Chord_two"
    music_type = ((SINGLE,SINGLE),(INTERVAL,INTERVAL),(CHORDONE,CHORDONE),(CHORDTWO,CHORDTWO))
    serial_num = models.IntegerField(default=0)
    music = models.FileField(null=True,blank=True,upload_to='media/')
    type = models.CharField(choices=music_type,null=True,blank=True,max_length=100)

class MusicImage(TimestampedUUIDModel):
    image = models.FileField(null=True,blank=True,upload_to='media/')
    merge_music = models.FileField(null=True,blank=True,upload_to='media/')
    latitude = models.DecimalField(null=True,blank=True,max_digits=20, decimal_places=6)
    longitude = models.DecimalField(null=True,blank=True,max_digits=20, decimal_places=6)

