# look to housing problem to figure out concatenation
# label full statements and punchlines
# write out timing

import os
import re
import nltk
from nltk.corpus import cmudict
d = cmudict.dict()

extra_words = {'trippin': 2, 'dinero': 3, 'iconic': 3, 'sound-check': 2, '2': 1, 'smoothie': 2, 'flappy': 2, 'cuz': 1, 'f******': 2, 'well-trained': 2, '15th': 2}


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

def pos(statement):
    return nltk.pos_tag(statement.split())

def syll(statement):
    syllables = []
    for word in statement.split():
        syllables.append(nsyl(word))
    return syllables

def reformat(statement, pos, syll):
    statement_features = []
    print len(statement.split())
    print len(pos)
    print len(syll)
    print '\n'

    for i, word in enumerate(statement.split()):
        statement_features.append([word, pos[i], syll[i]])
    return statement_features




def nsyl(word):
    if word.lower() in d.keys():
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    elif word.lower() in extra_words.keys():
        return extra_words[word.lower()]
    else:
        # default for unknown
        return 1

for f in os.listdir('transcripts/Specials/'):
    if 'txt' in f:
        #chunks = []
        all_statements = []
        path_to_output = './features/' + f.split('.txt')[0] + '.csv'
        print path_to_output
        full_path = 'transcripts/Specials/' + f
        print full_path
        with open(full_path, 'rb') as transcript:
            ts = transcript.read()
        ts_split = ts.split('\n')
        counter = 0
        for i, s in enumerate(ts_split):
            if 'transcript' in s:
                process_transcript(s)

        features_file = open(path_to_output, 'wb')
        print path_to_output
        for s in all_statements:
            for i, p_s in enumerate(s):
                if i == len(s) - 1:
                    text_to_write = str(reformat(p_s, pos(p_s), syll(p_s))) + 'PUNCHLINE'
                    #text_to_write = p_s + ', ' + pos(p_s) + syll(p_s) + ', PUNCHLINE'+'\n'
                    #print p_s, '__label__PUNCHLINE'
                else:
                    text_to_write = str(reformat(p_s, pos(p_s), syll(p_s))) + 'STATEMENT'
                    #text_to_write = p_s + ', ' + pos(p_s) + syll(p_s) + ', STATEMENT'+'\n'
                    #print p_s, '__label__STATEMENT'
                print text_to_write
                #features_file.write(text_to_write)



