from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

client_file = 'speech-zero-key.json'  # Add your client(json) file here
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# Load audio file
speech_file = 'test.wav'  # Add your audio file here
with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

# Configure speaker diarization separation between speakers
diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
    max_speaker_count=10,
)

# Configure audio settings for the audio file
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=8000,
    language_code="pt-BR",
    diarization_config=diarization_config,
    model='phone_call',
)

print("Waiting for operation to complete...")

# Transcribe audio
response = client.recognize(config=config, audio=audio)

# Get the first result
result = response.results[-1]

# Each result is for a consecutive portion of the audio. Iterate through
words_info = result.alternatives[0].words

# Printing out the output:
for word_info in words_info:
    print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")

# Create a dictionary to store the words spoken by each speaker
speaker_sentences = {}

# Iterate through the results to collect words by speaker
for result in response.results:
    for word_info in result.alternatives[0].words:
        speaker_tag = word_info.speaker_tag

        if speaker_tag == 0:
            continue

        # If this is the first word from this speaker, initialize a list
        if speaker_tag not in speaker_sentences:
            speaker_sentences[speaker_tag] = []
        # Append the word to the list for this speaker
        speaker_sentences[speaker_tag].append(word_info.word)

# Convert lists of words into sentences and print them
for speaker_tag, words in speaker_sentences.items():
    sentence = ' '.join(words)
    print(f"Speaker {speaker_tag}: {sentence}")
