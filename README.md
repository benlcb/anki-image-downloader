# anki-image-downloader
Adds images to your Anki flashcards

Currently, the script adds pictures to the back side of your cards, based on what is written on the back side of your cards. 
You can run the script like this: 

### 1. Google Search API
To be able to use the script, you need keys for the Google Search API. You can get those here: 
https://console.cloud.google.com/apis/dashboard

### 2. Set following environment variables. 
export GCS_DEVELOPER_KEY=fookey
export GCS_CX=barkey

### 3. Run the script 
python3 test.py /path/to/your/old/deck.apkg /path/where/you/want/the/new/file.apkg


