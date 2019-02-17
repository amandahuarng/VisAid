# VisAid
A tool that allows you to identify surrounding objects using your voice.


## Make sure you install the following packages before running: 
- sox 
- Google Cloud authentication
- houndify
- json
- io
- sys
- os
- NumPy
- Houndify Python SDK


## Run your program with this line of code: 
rec -p | sox - -c 1 -r 16000 -t s16 -L - | ./sample_stdin.py *CLIENT ID* *CLIENT KEY*
 
Replace *CLIENT ID* and *CLIENT KEY* with your unique keys on your Houndify Dashboard
