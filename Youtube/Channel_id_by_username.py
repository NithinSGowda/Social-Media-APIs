from googleapiclient.discovery import build
import sys
import json

DEVELOPER_KEY = "API_KEY"
username = sys.argv[1]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

response = youtube.channels().list(
part="id", # Part signifies the different types of data you want
forUsername = username).execute()


if (response["pageInfo"]["totalResults"]) > 0:
    ChannelId = response["items"][0]["id"]
    dict={"Username":username,"ChannelId":ChannelId}
    with open(username+"_channelid.json", "w") as outfile:
        json.dump(dict, outfile)
