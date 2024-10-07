from pydub.utils import mediainfo

file_path = 'test2.mp3'  # Change this to the path of your audio file


# Check the sample rate(Hz) of the audio file
def get_sample_rate(file_path):
    audio_info = mediainfo(file_path)
    sample_rate = audio_info['sample_rate']
    return sample_rate


print(f"Sample Rate: {get_sample_rate(file_path)} Hz")
