import imageio
imageio.plugins.ffmpeg.download()
from fileinput import filename
import logging as log
import os
import sys
import json
import glob
import requests
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import azure.functions as func
import youtube_dl

#TWITCH
#originally obtained from https://gist.github.com/chevignon93/f99b0d7642d898e3df2c4bd08d94f622
#ended up using youtube-dl so I didn't have to do the scraping myself
def download_twitch_highlight(path, clip_origin):
    ydl_opts = {"nooverwrites" : True,
                "outtmpl": path+'/%(title)s.%(ext)s'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([clip_origin])

    return("%(title)s.%(ext)s")

#YOUTUBE
def download_youtube_clip(path, clip_origin):
    #code to download youtube videos
    yt = YouTube(clip_origin)
    if yt.length < 300:  
        stream = yt.streams.filter(res="720p").first()
        stream.download(path)

def say_hello():
    return "hello"
