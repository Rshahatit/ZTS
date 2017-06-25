# ZTS
## Transcribes video using Microsofts Cognitive Services Video Indexer API.
  Video Indexer API Documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/video-indexer/video-indexer-overview

## Mission:
  To create meeting minutes after a virtual recorded meeting so that attendees can focus rather than take notes.

## Features:
    Creates a transcript of the meeting. Which entails "who said what" in chronological order.
    Detects the face/scene changes that come with Zoom meetings based on who's speaking .
    Automatically runs after meeting is ended.
        Zoom automatically saves video file to same folder after the meeting is over.
        We used that to our advantage and wrote a simple Apple Folder Action Script that will run every time a file is added to that folder.
    Emails transcript to all attendees.
    Posts transcript to specific slack channels. 
