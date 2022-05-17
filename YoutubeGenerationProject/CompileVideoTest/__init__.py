from distutils.command.upload import upload
import imageio
#imageio.plugins.ffmpeg.download()
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
from moviepy.editor import VideoFileClip, concatenate_videoclips

#Azure Key Vault
KEY_VAULT_URI = "https://kv-jjb-prod-use2.vault.azure.net/"
credential = DefaultAzureCredential(managed_identity_client_id="725a00b2-ea8b-4791-8244-6929992e9858")
client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

#Azure Blob Storage
SA_CONNECTION_STRING = client.get_secret("youtubegeneration-sa-connectionstring").value
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(SA_CONNECTION_STRING)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Compiling clips into a video at {datetime.now()}')
    file_path = tempfile.gettempdir()
    upload_file_path = tempfile.gettempdir() + "/downloadedfiles/"
    output_file_path = tempfile.gettempdir() + "/output/exportedvideo.mp4"
    download_all_files_from_blob(upload_file_path)
    compile_clips_to_video(file_path)
    output_to_blob(output_file_path)
    remove_local_videos(upload_file_path)

    return func.HttpResponse(f"successfully downloaded videos")


def download_all_files_from_blob(path):
    client = BLOB_SERVICE_CLIENT.get_container_client( container="clips")
    my_blobs = client.list_blobs()
    for blob in my_blobs:
        print(blob.name)
        bytes = client.get_blob_client(blob).download_blob().readall()
        download_file_path = path + blob.name
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(bytes)


def compile_clips_to_video(path):
    output_video_path = path + "/output/"
    allvids = path + "/downloadedfiles/"
    all_file_names = [f for f in os.listdir(allvids)
                    if os.path.isfile(os.path.join(allvids, f)) and ".mp4" in f]

    #combine all clips to one file
    filename_list = []
    for x in all_file_names:
        out_path = os.path.join(allvids, x)
        print(f"adding file:{out_path}")
        filename_list.append(out_path)

    video_clips = []
    for x in filename_list:
        logging.info(x)
        clip = VideoFileClip(x)
        if clip.size != (1280,720):
            clip = clip.resize( (1280,720) )

        video_clips.append(clip)

    final_clip = concatenate_videoclips(video_clips)
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    final_clip.write_videofile(f"{output_video_path}/exportedvideo.mp4")

def output_to_blob(path):
    logging.info(f"uploading file:{path}")
    try:
        blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container="exported", blob="exportedvideo.mp4")
        with open(path, "rb") as data:
            blob_client.upload_blob(data)
    except:
        pass
    os.remove(path)

def remove_local_videos(path):
    all_file_names = [f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f)) and ".mp4" in f]

    #remove all local videos
    filename_list = []
    for x in all_file_names:
        out_path = os.path.join(path, x)
        print(f"removing local file:{out_path}")
        os.remove(out_path)
