import imageio
imageio.plugins.ffmpeg.download()
import pathlib
import logging
from xmlrpc.client import DateTime
from datetime import datetime
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os
import praw
import json
import unicodedata
import re
import tempfile
from CollectClipsTest.download_clips import *  

#Azure Key Vault
KEY_VAULT_URI = "https://kv-jjb-prod-use2.vault.azure.net/"
credential = DefaultAzureCredential(managed_identity_client_id="725a00b2-ea8b-4791-8244-6929992e9858")
client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

#Azure Blob Storage
SA_CONNECTION_STRING = client.get_secret("youtubegeneration-sa-connectionstring").value
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(SA_CONNECTION_STRING)


#Constants
SUBREDDIT_NAME = "GlobalOffensive"
CLIENT_ID = client.get_secret("praw-client-id").value
CLIENT_SECRET = client.get_secret("praw-client-secret").value
USER_AGENT = client.get_secret("praw-user-agent").value
REDIRECT_URI = client.get_secret("praw-redirect-uri").value
REFRESH_TOKEN = client.get_secret("praw-refresh-token").value

#Main
def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info(f"Collecting top 5 reddit clips at {datetime.now()}")

    
    #Authentication
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret = CLIENT_SECRET,
                         user_agent=USER_AGENT,
                         redirect_uri=REDIRECT_URI,
                         refresh_token=REFRESH_TOKEN
                         )

    subreddit = reddit.subreddit(SUBREDDIT_NAME)

    submission_list = []
    #Getting all top posts
    for submission in subreddit.hot(limit=50):
        if "youtu" in submission.url or "clips" in submission.url:
            submission_list.append(submission.url)

    submission_dict = {}
    for x in range(len(submission_list)):
        submission_dict[x] = submission_list[x]
    
    upload_file_path = tempfile.gettempdir() + "/downloadedfiles/"
    #download any twitch clips to blob storage
    for clipname in submission_list:
        if ("youtu" in clipname):
            try:
                download_youtube_clip(upload_file_path, clipname)
            except:
                continue
        if ("twitch" in clipname):
            try:
                download_twitch_highlight(upload_file_path, clipname)
            except:
                continue
    
    output_to_blob(upload_file_path)

    return func.HttpResponse(json.dumps(submission_dict))
    

def output_to_blob(path):
    #Updating file names to not include invalid characters
    all_file_names = [f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f)) and ".mp4" in f]
    
    for name in all_file_names:
        old_name = name
        new_name = (((old_name.replace(" ", "")).replace("'", "")).replace("!", ""))
        os.replace(f"{path}/{old_name}", f"{path}/{new_name}")

    all_file_names = [f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f)) and ".mp4" in f]

    #upload to blob storage and delete from local storage
    for x in all_file_names:
        out_path = os.path.join(path, x)
        print(f"uploading file:{out_path}")
        try:
            blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container="clips", blob=x)
            with open(out_path, "rb") as data:
                blob_client.upload_blob(data)
        except:
            pass
        os.remove(out_path)
        out_path = ""