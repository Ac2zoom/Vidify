import os
import json

from gensim.summarization.summarizer import summarize
import spacy
import pandas as pd

import boto3

FILE_NAME = "/home/rock/data/angelhack_vidify/sample.txt"
f = open(FILE_NAME, "r")
text = f.read()

comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')

# get the text summary using gensim
text_summ = summarize(text, ratio=0.05)

# get the key phrases from Amazon Comprehend. Then drop the words & phrases with a low score
key_phrases = json.dumps(comprehend.detect_key_phrases(Text=text_summ, LanguageCode='en'))

# list of key-phrase dictionaries. then sort by phrase score descending
kp_ld = (json.loads(key_phrases))["KeyPhrases"]
kp_sorted = sorted(kp_ld, key=lambda d: -d['Score'])
phrases_to_drop = [d['Text'] for d in kp_sorted if d['Score'] < 0.98]
str_list = [None] * len(phrases_to_drop)
str_list[0] = text_summ.replace(phrases_to_drop[0], "")
for i in range(1, len(phrases_to_drop)):
    str_list[i] = str_list[i-1].replace(phrases_to_drop[i], "")
text_final = str_list[-1]

# get key phrases using spaCy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

# put all token parts in a pandas dataframe
data = []
cols = ['text', 'lemma', 'pos', 'tag', 'dep', 'shape', 'alpha', 'stop']
for token in doc:
    data.append((token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))

df = pd.DataFrame(data, columns=cols)

has_apostrophe = df.loc[:, 'text'].apply(lambda x: (x[0] in ["’", ".", ",", "-"])).to_list()
sw = df['stop'].to_list()
stopwords = [sw[i] if has_apostrophe[i]==False else True for i in range(len(sw))]

keep_word_list = [True] + [False if (stopwords[i]==True and (stopwords[i-1]==True or stopwords[i+1]==True)) \
    else True for i in range(1, len(stopwords)-1)] + [True]
drop_word_list = [False] + [True if ((stopwords[i]==True and (stopwords[i-1]==True or stopwords[i+1]==True)) \
                                    or (stopwords[i]==False and (stopwords[i-1]==True and stopwords[i+1]==True))) \
                            else False for i in range(1, len(stopwords)-1)] + [False]

words = df.loc[:, 'text']
words[drop_word_list] = "\n"
text_summ_2 = " ".join(words.to_list())
phrase_list = [phrase.strip() for phrase in text_summ_2.split("\n") if (len(phrase.split()) > 3)]

print(phrase_list)