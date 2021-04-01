from googleapiclient.discovery import build
import sys
import json


DEVELOPER_KEY = "AIzaSyDNJsMDURjieOpkobhDSGs9rR0o2Anv-PI"
channelId = sys.argv[1]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

search_response = youtube.channels().list(
part="statistics", # Part signifies the different types of data you want
id = channelId
).execute()

viewCount = search_response["items"][0]["statistics"]["viewCount"]
subscriberCount = search_response["items"][0]["statistics"]["subscriberCount"]
hiddenSubscriberCount = search_response["items"][0]["statistics"]["hiddenSubscriberCount"]
videoCount = search_response["items"][0]["statistics"]["videoCount"]

statistics_dict={"viewCount":viewCount,"subscriberCount":subscriberCount,"hiddenSubscriberCount":hiddenSubscriberCount,"videoCount":videoCount}

with open(channelId+".json", "w") as outfile:
    json.dump(statistics_dict, outfile)
