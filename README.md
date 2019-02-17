# VisAid
A tool that allows you to identify surrounding objects using your voice.


## Make sure you install the following packages before running: 
- sox 
- houndify
- json
- io
- sys
- os
- NumPy
- [Houndify Python SDK](https://docs.houndify.com/sdks/docs/python#python-houndify-sdk
- [Google Cloud Vision API](https://cloud.google.com/vision/docs/reference/rest/)

## Authenticate with Google Cloud API prior to running code: 
Use this line: 
export GOOGLE_APPLICATION_CREDENTIALS=“/home/user/Downloads/[FILE_NAME].json”

## Run your program with this line of code: 
rec -p | sox - -c 1 -r 16000 -t s16 -L - | main.py *CLIENT ID* *CLIENT KEY*
 
Replace *CLIENT ID* and *CLIENT KEY* with your unique keys on your Houndify Dashboard
