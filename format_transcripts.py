# look to housing problem to figure out concatenation
# write out full statements and punchlines
# write out timing

import os

chunks = []
all_words = []
state = 'alternatives'
new_word = {}

def is_end(word):
    w = list(word.strip())
    if w[-2] == '.' or w[-2] == ',':
        return True
    return False

for f in os.listdir('transcripts/Meyers/'):
    if 'Zainab' in f:
    #if 'txt' in f:
        full_path = 'transcripts/Meyers/' + f
        print full_path
        with open(full_path, 'rb') as transcript:
            ts = transcript.read()
        ts_split = ts.split('\n')
        counter = 0
        for i, s in enumerate(ts_split):
            # NEW SECTION
            if 'alternatives' in s:
                print ts_split[i+1]
                if counter > 0:
                    chunks.append(new_chunk)
                counter += 1
                new_chunk = {}
                new_chunk['words'] = []
            if 'words' in s:
                new_word = {}
            if 'start_time' in s:
                if not 'nanos' in ts_split[i+2]:
                    new_word['start'] = ts_split[i+1].strip()
                else:
                    new_word['start'] = ts_split[i+1].strip() + ' ' + ts_split[i+2].strip()
            if 'end_time' in s:
                if not 'nanos' in ts_split[i+2]:
                    new_word['end'] = ts_split[i+1].strip()
                else:
                    new_word['end'] = ts_split[i+1].strip() + ' ' + ts_split[i+2].strip()
            if 'word:' in s:
                new_word['word'] = s.split('word:')[1].strip()

            if 'start' in new_word and 'end' in new_word and 'word' in new_word:
                #all_words.append(new_word)
                new_chunk['words'].append(new_word)
                new_word = {}

# for i, c in enumerate(chunks):
#     print c
#     for w in c['words']:
#         if is_end(w['word']):
#             print '        STATEMENT'
#     print '       PUNCHLINE'
#     print '\n'




