import os
import sys
import json
import glob
import urllib
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips
from reddit import *
from youtube import *

def make_vid():
	#code to concatenate video clips
	#go into videos folder, iterate through file names
	#print("made it")
	filename_list = []
	for filename in glob.iglob('videos/*.mp4'):
		filename_list.append(filename)

	video_clips = []
	for x in filename_list:
		clip = VideoFileClip(x)
		if clip.size != (1280,720):
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
def main():
	