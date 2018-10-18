# look to housing problem to figure out concatenation
# label full statements and punchlines
# write out timing
#figure out apostrophes

import os
import re

chunks = []
all_statements = []


def is_end(word):
    w = list(word.strip())
    if w[-2] == '.' or w[-2] == ',':
        return True
    return False

def process_chunks(chunks):
    statements = []
    delimiters = [',', '.', '?', '!']
    for i, c in enumerate(chunks):
        delims = 0
        for d in delimiters:
            if d in c:
                statements[-1] = statements[-1] + d
                delims = delims + 1
        if delims == 0 and not c == '':
            statements.append(c)
    print statements



def process_transcript(transcript):
    print '\n'
    print 'New:'
    transcript = transcript.split('transcript:')[1].strip()
    transcript = re.sub('"', '', transcript)
    transcript = re.split('([?.,!])', transcript)
    process_chunks(transcript)


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
            if 'transcript' in s:
                process_transcript(s)

# for i, c in enumerate(chunks):
#     print c
#     for w in c['words']:
#         if is_end(w['word']):
#             print '        STATEMENT'
#     print '       PUNCHLINE'
#     print '\n'




