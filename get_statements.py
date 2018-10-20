# look to housing problem to figure out concatenation
# label full statements and punchlines
# write out timing

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
                statements[-1] = statements[-1]
                delims = delims + 1
        if delims == 0 and not c == '':
            if '\\' in c:
                c = c.replace('\\', '')
            statements.append(c.strip())
    #statements.append('PUNCHLINE')
    all_statements.append(statements)
    # for s in statements:
    #     print s


def process_transcript(transcript):
    transcript = transcript.split('transcript:')[1].strip()
    transcript = re.sub('"', '', transcript)
    transcript = re.split('([?.,!])', transcript)
    process_chunks(transcript)


for f in os.listdir('transcripts/Meyers/'):
    if 'Zainab' in f:

    #if 'txt' in f:
        path_to_output = './statements/' + f
        print path_to_output
        statements_file = open(path_to_output, 'wb')
        full_path = 'transcripts/Meyers/' + f
        print full_path
        with open(full_path, 'rb') as transcript:
            ts = transcript.read()
        ts_split = ts.split('\n')
        counter = 0
        for i, s in enumerate(ts_split):
            if 'transcript' in s:
                process_transcript(s)

for s in all_statements:
    for i, p_s in enumerate(s):
        if i == len(s) - 1:
            text_to_write = p_s + '__label__PUNCHLINE'+'\n'
            #print p_s, '__label__PUNCHLINE'
        else:
            text_to_write = p_s + '__label__STATEMENT'+'\n'
            #print p_s, '__label__STATEMENT'
        statements_file.write(text_to_write)



