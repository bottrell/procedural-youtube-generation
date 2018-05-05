'''
#code to download youtube videos
from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
stream = yt.streams.first()
stream.download()
'''


'''
#code to concatenate video clips
from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("myvideo.mp4")
clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
clip3 = VideoFileClip("myvideo3.mp4")
final_clip = concatenate_videoclips([clip1,clip2,clip3])
final_clip.write_videofile("my_concatenation.mp4")
'''
import requests
import urllib
import os
from bs4 import BeautifulSoup
import json
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
print(THIS_FOLDER + "/videos")
my_file = os.path.join(THIS_FOLDER + "/videos", 'highlight_to_download_.mp4')

client_id = '3w25cnut69wvv1za2ddw6bfe917150'
client_secret = 'vsdeigzx7pfynxat34gfi7942yrn6z'
clip = requests.get("https://clips.twitch.tv/SeductivePeacefulMarjoramUWot").text
soup = BeautifulSoup(clip, 'html.parser')
#print(soup.prettify())
info = (soup.find_all("script")[-1])
info = str(info)
new_string = 
#url = """videos/https://clips-media-assets2.twitch.tv/AT-cm%7C28580236752-offset-17372-480.mp4"""
#urllib.request.urlretrieve("https://clips-media-assets2.twitch.tv/AT-cm%7C28580236752-offset-17372-480.mp4", my_file)