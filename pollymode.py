# -*- coding: utf-8 -*-
"""

@author: Jasper Yao
"""
#We assume that awscli is already good to go
import boto3
import os
import sys
import subprocess
from tempfile import gettempdir
from contextlib import closing
from botocore.exceptions import BotoCoreError, ClientError


#Get access key from following
from polly.access_key import *

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
p = boto3.client(
        'polly',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-west-2'
)
try:
    # Request speech synthesis
    response = p.synthesize_speech(Text="Hello world!", OutputFormat="mp3",
                                        VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
    with closing(response["AudioStream"]) as stream:
        output = os.path.join(gettempdir(), "speech.mp3")

        try:
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)

else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)



