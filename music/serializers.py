from rest_framework import exceptions, serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):

    class Meta :
        model = MusicImage
        fields = ['image']      
