import praw
import os
import sys
import json
import glob
import urllib
import requests

#Goes to the specified subreddit and collects the video urls of the 25 top posts
#and returns them in a list format
def get_top_videos(subreddit_name):
	reddit = praw.Reddit(client_id='da1iTPWzHVxDRg',
                     	client_secret='3l-8FZ4tecVMx9VeFyeLKt4vCuU',
                     	password='Cabrera_24',
                     	user_agent='testscript by /u/fakebot3',
                     	username='Siqq_cs')


	subreddit = reddit.subreddit(subreddit_name)
	submission_list = []
	for submission in subreddit.hot(limit=25):
		if "youtu" in submission.url or "clips" in submission.url:
			submission_list.append(submission.url)
	
	return submission_list

get_top_videos("globaloffensive")