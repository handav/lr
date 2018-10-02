#https://cloud.google.com/speech-to-text/docs/async-time-offsets

import io
import os
import wave

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage

# Instantiates a client
client = speech.SpeechClient()
storage_client = storage.Client()
bucket = storage_client.get_bucket('laughingroomstorage')

#folder = '/Volumes/Seagate Backup Plus Drive/Hannah_Data/LaughingRoom/full_dataset/Conan/'
transcripts = '/Users/hannahdavis/Documents/LaughingRoom/Text/transcripts/'

def process(filename):
    # The name of the audio file to transcribe
    # sample: laughingroomstorage/conan/Adam Cayton-Holland Stand-Up 02_09_16  - CONAN on TBS-FQ3VAS5vyHY.flac
    file_name = 'gs://laughingroomstorage/conan/' + filename
    transcript_file = transcripts + filename.split('.flac')[0]+ '.txt'
    
    # wave_file = wave.open(file_name, "rb")
    # frame_rate = wave_file.getframerate()
    # wave_file.close()
    # print frame_rate

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44000,
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))

        for word_info in result.alternatives[0].words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))

    with open(transcript_file, 'w') as ts:
        ts.write(response.results)

for blob in bucket.list_blobs():
    try:
        #print blob.id
        if 'Adam Cayton' in blob.id:
            print blob.id
        #     transcript_path = transcripts + filename
        #     if os.path.isfile(transcript_path) == False:
        #         process(filename)
    except UnicodeEncodeError:
        print 'unicode error'
        pass
