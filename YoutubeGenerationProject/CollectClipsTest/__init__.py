import logging
from xmlrpc.client import DateTime
from datetime import datetime
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import secrets
import praw
import json

KEY_VAULT_URI = "https://kv-jjb-prod-use2.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

#Constants
SUBREDDIT_NAME = "GlobalOffensive"
CLIENT_ID = client.get_secret("praw-client-id")
CLIENT_SECRET = client.get_secret("praw-client-secret")
USER_AGENT = client.get_secret("praw-user-agent")
REDIRECT_URI = client.get_secret("praw-redirect-uri")
REFRESH_TOKEN = client.get_secret("praw-refresh-token")

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

    subreddit = reddit.subreddit(SUBREDDITNAME)

    #Getting all top posts
    topPosts = []
    for submission in subreddit.hot(limit=50):
        topPosts += submission
        print(submission.title)

    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )