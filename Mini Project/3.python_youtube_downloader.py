# Akhtar Code
# Python Script to Generate Password

''' 
Instruction
1. Install pytube, pip install pytube (via Terminal)
'''

from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")

# Example
link = "https://www.youtube.com/watch?v=rzYNjC5RvMI"
Download(link)


