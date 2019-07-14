import json
import requests
from gensim.summarization.summarizer import summarize
import boto3

comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')

FILE_NAME = "/home/rock/data/angelhack_vidify/sample.txt"


def get_key_phrases(url_or_file=FILE_NAME, words=None):
    """
    Returns a tuple having (gensim_summarization, comprehend_phrases)
    """
    if url_or_file is None:
        text = words
    elif "http" in url_or_file:
        text = requests.get(url_or_file).text
    else:
        file = FILE_NAME
        f = open(file, "r")
        text = f.read()
        f.close()

    def comprehend_phrases(text_summ):
        """
        Get phrases from Amazon Comprehend
        """
        text_summ_list = text_summ.split("\n")
        phrases = [None] * len(text_summ_list)
        for i in range(len(text_summ_list)):
            sentence = text_summ_list[i]
            key_phrases = json.dumps(comprehend.detect_key_phrases(Text=sentence, LanguageCode='en'))
            kp_ld = (json.loads(key_phrases))["KeyPhrases"]
            sent_phrases = [phrase['Text'] for phrase in kp_ld if len(phrase['Text'].split()) > 1 ]
            phrases[i] = sent_phrases
        return phrases

    # get the text summary using gensim. 10% of all sentences
    text_summ = summarize(text, ratio=0.10)

    # get the key phrases from the gensim summarization using Amazon Comprehend
    phrases_list = comprehend_phrases(text_summ)

    return text_summ, phrases_list
