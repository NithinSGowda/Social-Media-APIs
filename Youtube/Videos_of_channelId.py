from googleapiclient.discovery import build
import sys
import pandas as pd

DEVELOPER_KEY = "API_KEY"
ChannelId = sys.argv[1]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

response = youtube.search().list(maxResults=50,
part="snippet,id",
order = "date",
channelId = ChannelId
).execute()

videoId = []
title = []
description = []
publishTime = []

for item in response["items"]:
    videoId.append(item["id"]["videoId"])
    title.append(item["snippet"]["title"])
    description.append(item["snippet"]["description"])
    publishTime.append(item["snippet"]["publishTime"])

dict = {"videoId":videoId,"Title":title,"description":description,"publishTime":publishTime}
df=pd.DataFrame(data=dict)
df.to_json(ChannelId+"_videos.json",orient="records")
