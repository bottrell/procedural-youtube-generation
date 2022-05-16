from distutils.command.upload import upload
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


KEY_VAULT_URI = "https://kv-jjb-prod-use2.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)
SA_CONNECTION_STRING = client.get_secret("youtubegeneration-sa-connectionstring").value
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(SA_CONNECTION_STRING)

upload_file_path = f'downloadedfiles/'


all_file_names = [f for f in os.listdir(upload_file_path)
                    if os.path.isfile(os.path.join(upload_file_path, f)) and ".mp4" in f]


for x in all_file_names:
    path = os.path.join(upload_file_path, x)
    print(path)
    blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container="clips", blob=x)
    #Upload the file to blob storage
    with open(path, "rb") as data:
        blob_client.upload_blob(data)
    #Delete the file from local storage
    os.remove(path)
    path = ""
# for file in os.listdir(upload_file_path):
#         filename = os.fsdecode(file)
#         print(filename)
#         output_filename = upload_file_path + filename
#         output_to_blob(output_filename, filename)

