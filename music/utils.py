from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS 
from pydub import AudioSegment

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded_tag = TAGS.get(tag, tag)
            if decoded_tag == 'GPSInfo':
                gps_data = {}
                for gps_tag in value:
                    sub_decoded_tag = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded_tag] = value[gps_tag]
                exif_data[decoded_tag] = gps_data
            else:
                exif_data[decoded_tag] = value
    return exif_data

def get_gps_info(exif_data):
    if 'GPSInfo' in exif_data:
        gps_info = {}
        for key in exif_data['GPSInfo']:
            gps_info[GPSTAGS.get(key, key)] = exif_data['GPSInfo'][key]
        return gps_info
    else:
        return None

def get_coordinates(gps_info):
    if gps_info:
        latitude = gps_info.get('GPSLatitude')
        longitude = gps_info.get('GPSLongitude')
        if latitude and longitude:
            latitude_ref = gps_info.get('GPSLatitudeRef', 'N')
            longitude_ref = gps_info.get('GPSLongitudeRef', 'W')
            lat = (latitude[0] + latitude[1]/60.0 + latitude[2]/3600.0) * (-1 if latitude_ref in ['S', 'W'] else 1)
            lon = (longitude[0] + longitude[1]/60.0 + longitude[2]/3600.0) * (-1 if longitude_ref in ['S', 'W'] else 1)
            return lat, lon
    return None

def extract_gps_location(image_path):
    try:
        image = Image.open(image_path)
        exif_data = get_exif_data(image)
        # print("---------",exif_data)
        gps_info = get_gps_info(exif_data)
        coordinates = get_coordinates(gps_info)
        return coordinates
    except Exception as e:
        print("Error:", e)
        return None
    
def merge_audio_files(input_files, output_file):
    # Create empty audio segment to store merged audio
    merged_audio = AudioSegment.empty()
    
    # Iterate over input files and append them to merged_audio
    for file in input_files:
        audio = AudioSegment.from_file(file)
        merged_audio += audio
    
    # Export merged audio to output file
    a = merged_audio.export(output_file, format="mp3")  # Change format if needed

    return a 

# List of input audio files to merge
# input_files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]

