import os
import sys
import json
import glob
import urllib
import requests
from pytube import YouTube
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, concatenate_videoclips
#client_id = '3w25cnut69wvv1za2ddw6bfe917150'
#client_secret = 'vsdeigzx7pfynxat34gfi7942yrn6z'

def download_twitch_highlight(clip_origin):
	#get the html of the clip's webpage
	clip = requests.get(clip_origin).text
	soup = BeautifulSoup(clip, 'html.parser')

	#Since the video url is hidden in a script, we have to parse the script
	#This should work regardless of how the script is set up
	info = (soup.find_all("script")[-1])
	info = str(info)
	new_string = info.split("[")
	new_string = new_string[-1]
	dic = new_string.split("]")[0]
	dic = "[" + dic + "]"
	obj = json.loads(dic)
	url = obj[0]["source"]
	filename = url.split("/")[-1]
	THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
	my_file = os.path.join(THIS_FOLDER + "/videos", filename)

	#url = """videos/https://clips-media-assets2.twitch.tv/AT-cm%7C28580236752-offset-17372-480.mp4"""
	urllib.request.urlretrieve(url, my_file)


def download_youtube_clip(clip_origin):
	#code to download youtube videos
	from pytube import YouTube
	yt = YouTube(clip_origin)
	stream = yt.streams.first()
	stream.download('videos/')


def make_vid():
	#code to concatenate video clips
	#go into videos folder, iterate through file names
	print("made it")
	filename_list = []
	for filename in glob.iglob('videos/*.mp4'):
		filename_list.append(filename)

	video_clips = []
	for x in filename_list:
		clip = VideoFileClip(x)
		if clip.size() != (1280,720):
			clip = clip.resize( (1280,720) )

		video_clips.append(clip)

	final_clip = concatenate_videoclips(video_clips)
	final_clip.write_videofile("exportedvideo.mp4")

	'''clip1 = VideoFileClip("myvideo.mp4")
	clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
	clip3 = VideoFileClip("myvideo3.mp4")
	final_clip = concatenate_videoclips([clip1,clip2,clip3])
	final_clip.write_videofile("my_concatenation.mp4")'''

#download_twitch_highlight("https://clips.twitch.tv/AbrasiveArtsyAnacondaDatBoi")
#download_youtube_clip('https://www.youtube.com/watch?v=beVsBZ7yYuA&feature=youtu.be')
make_vid()

