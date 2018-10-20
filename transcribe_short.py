#https://cloud.google.com/speech-to-text/docs/async-time-offsets
#https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html#google.cloud.storage.blob.Blob

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

transcripts = '/Users/hannahdavis/Documents/LaughingRoom/Text/transcripts/'

def process(filename):
    # The name of the audio file to transcribe
    file_name = 'gs://laughingroomstorage/specials/' + filename
    transcript_file = transcripts + filename.split('.flac')[0]+ '.txt'
    
    audio = types.RecognitionAudio(uri=file_name)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='en-US',
        profanity_filter=True,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result(timeout=100000)
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
    print response.results
    # recognized_text = 'Transcribed Text: \n'
    # for i in range(len(response.results)):
    #     recognized_text += response.results
    with open(transcript_file, 'w') as ts:
        for r in response.results:
            ts.write("%s\n" % r)

for blob in bucket.list_blobs():
    if 'specials' in blob.id:
        try:
            print blob.id
            if 'mono' in blob.id:
                fn = blob.id.split('specials/')[1].split('.flac')[0]+'.flac'
                print fn
                transcript_path = transcripts + fn.split('.flac')[0]+ '.txt'
                if os.path.isfile(transcript_path) == False:
                    process(fn)
        except UnicodeEncodeError:
            print 'unicode error'
            pass
