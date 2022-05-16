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
from CollectClipsTest.download_clips import *  

#Azure Key Vault
KEY_VAULT_URI = "https://kv-jjb-prod-use2.vault.azure.net/"
credential = DefaultAzureCredential()
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
    
    upload_file_path = f'CollectClipsTest/downloadedfiles/'
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
    
    for file in os.listdir(upload_file_path):
        filename = os.fsdecode(file)
        print(filename)
        output_filename = upload_file_path + filename
        output_to_blob(output_filename, filename)

    return func.HttpResponse(json.dumps(submission_dict))
    
def output_to_blob(path, filename):
    blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container="clips", blob=filename)
    with open(path, "rb") as data:
        blob_client.upload_blob(data)
    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
    