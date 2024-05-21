
# Create your views here.
from .models import *
from .serializers import *
from rest_framework import generics, status
from django.http import FileResponse, HttpResponse,JsonResponse
from .utils import *
from rest_framework.response import Response
from django.core.files.base import ContentFile



class SaveImage(generics.CreateAPIView):
    queryset = MusicImage.objects.all()
    serializer_class = ImageSerializer

    def create (self,request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            b = serializer.save()
            coordinates = extract_gps_location(data['image'])
            music_type = data['type']
            if coordinates:
                a = []
                a.extend(str(coordinates[0]))
                a.extend(str(coordinates[1]))
                result = [char for char in a if char != '.']
                music_data = []
                for i in result:
                    try:
                        music_file  = Music.objects.get(serial_num = i,type=music_type)
                        music_data.append(music_file.music)
                    except:
                        continue
                
                output_file = "merged_audio.mp3"
        
                merged_music = merge_audio_files(music_data,output_file)

                merged_music.seek(0)

                b.merge_music.save('merged_music.mp3', ContentFile(merged_music.read()))
                b.save()
                merged_music.close()

            else:
                print("No GPS coordinates found.")

            
        response = HttpResponse(b.merge_music.read(), content_type="audio/mpeg")
        response["Content-Disposition"] = f'attachment; filename="music.mp3"'
        return response
    


class DownloadMusic(generics.RetrieveAPIView):
    queryset = MusicImage.objects.all()
    serializer_class = ImageSerializer

    def get(self,request,*args,**kwargs):
        request_id = self.kwargs.get('id')
        data = MusicImage.objects.get(id = request_id)

        response = HttpResponse(data.merge_music.read(), content_type="audio/mpeg")
        response['Content-Disposition'] = 'inline; filename="music.mp3"'
        return response


        