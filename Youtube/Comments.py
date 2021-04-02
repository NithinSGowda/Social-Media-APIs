from googleapiclient.discovery import build
import sys
import json

DEVELOPER_KEY = "APIKEY"
videoId = sys.argv[1]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

response=youtube.commentThreads().list(
part='snippet,replies',
videoId=videoId
).execute()

comment = []
Author_name = []
date = []
Author_channel_id = []
likes = []
totalReplyCount = []
replies_=[]

while response:
    for item in response['items']:
        comment.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
        Author_name.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        Author_channel_id.append(item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
        date.append(item['snippet']['topLevelComment']['snippet']['updatedAt'])
        likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
        totalReplyCount.append(item['snippet']['totalReplyCount'])
        reply = item['snippet']['totalReplyCount']
        reply_text =[]
        reply_likes = []
        reply_date = []
        reply_author = []
        reply_channel_id = []
        if reply>0:
            for reply in item['replies']['comments']:
                reply_text.append(reply['snippet']['textDisplay'])
                reply_author.append(reply['snippet']['authorDisplayName'])
                reply_channel_id.append(reply['snippet']['authorChannelId']['value'])
                reply_date.append(reply['snippet']['updatedAt'])
                reply_likes.append(reply['snippet']['likeCount'])
                replies_dict = {'Comment':reply_text,'Author_name':reply_author,'Date':reply_date,'Author_channel_id':reply_channel_id,'Likes':reply_likes}
                new_replies_dict = [{"Comment":a, "Author_name":b , "Date":c, "Author_channel_id":d , "Likes":e} for a, b,c,d,e in zip(replies_dict["Comment"], replies_dict["Author_name"], replies_dict["Date"], replies_dict["Author_channel_id"], replies_dict["Likes"])]
                replies_.append(new_replies_dict)
        else:
            replies_.append({})

    if 'nextPageToken' in response:
        response = youtube.commentThreads().list(
                part = 'snippet,replies',
                videoId = video_id
            ).execute()
    else:
        youtube_dict = {'Comment':comment,'Author_name':Author_name,'Date':date,'Author_channel_id':Author_channel_id,'Likes':likes,'totalReplyCount':totalReplyCount,"replies":replies_}
        break

new_youtube_dict = [{"Comment":a, "Author_name":b , "Date":c, "Author_channel_id":d , "Likes":e, "totalReplyCount":f , "replies":g} for a, b,c,d,e,f,g in zip(youtube_dict["Comment"], youtube_dict["Author_name"], youtube_dict["Date"], youtube_dict["Author_channel_id"], youtube_dict["Likes"], youtube_dict["totalReplyCount"], youtube_dict["replies"])]

with open(videoId+".json", "w") as outfile:
    json.dump(new_youtube_dict, outfile)
