# -*- coding: utf-8 -*-
"""

@author: Jasper Yao
"""
#We assume that awscli is already good to go
import boto3
import os
import string
import sys
import subprocess
from tempfile import gettempdir
from contextlib import closing
from botocore.exceptions import BotoCoreError, ClientError

#Get access key from following
from polly.access_key import *
#Should contain:
# ACCESS_KEY
# SECRET_KEY

#First we need to establish credentials for the system
# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
# https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#iam-user-name-and-password
# https://docs.aws.amazon.com/cli/latest/reference/polly/index.html

#Create a client object for polly using Oregon server
#polly = boto3.client('polly', region_name='us-west-2')
#os.environ['aws_default_region'] = 'your_region_name'

#session = boto3.Session(
#    aws_access_key_id=ACCESS_KEY,
#    aws_secret_access_key=SECRET_KEY,
#    aws_session_token=SESSION_TOKEN,
#)


#PollySynth class for polly,
#Currently supports simple text
class PollySynth():
    
    #Guess of the not billable characters
    notbillable = string.punctuation.join(string.whitespace)
    
    def __init__(self):
        
        self.p = boto3.client(
        'polly',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-west-2')
        ## Possible Voices
        # Default Joannna  voices[22]
        self.voices = ['Aditi',
        'Amy','Astrid','Bianca','Brian','Carla','Carmen','Celine','Chantal','Conchita','Cristiano',
        'Dora','Emma','Enrique','Ewa','Filiz','Geraint','Giorgio','Gwyneth','Hans','Ines','Ivy',
        'Jacek','Jan','Joanna','Joey','Justin','Karl','Kendra','Kimberly','Lea','Liv','Lotte','Lucia','Mads',
        'Maja','Marlene','Mathieu','Matthew','Maxim','Mia','Miguel','Mizuki','Naja','Nicole','Penelope',
        'Raveena','Ricardo','Ruben','Russell','Salli','Seoyeon','Takumi','Tatyana','Vicki','Vitoria','Zeina',
        'Zhiyu']
                
    
    # For the simple instance of Mp3 generation for less than 6000 total characters
    # and less than 3000 billable characters, (Assuming this means alphanumeric)
    # produce a voice text and return the file path to that object
    def mp3_speak(self, filename, text: str, Voice = "Joanna"):
        
        # Create a suitable filename
        filename = filename + hex(hash(text)) + "-" + Voice + ".mp3"
        
        #We want to make sure that the max character limit is not exceeded per API 
        input_ = str(text)
        input_length = len(input_.strip(self.notbillable))
        if input_length >= 3000:
            print("Warning Characters >= 3000")
        if input_length >= 6000:
            print("Billable Characters >= 6000 \n Quitting!!")
            sys.exit(-1)
        try:
            # Request speech synthesis
            response = p.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=Voice)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1) #Maybe a good idea to remove

        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important as the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), filename)
        
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                    
                    return output
                
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)
    
    #Returns the file object we have just produced 
    #def get_file
