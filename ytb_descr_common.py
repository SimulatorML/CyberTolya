#AIzaSyBTv9_M_Dampia_3ODvD1D82lrxC8V9amg

#JLu322-Dcow -видео от Бабушкина с канала KC
#канал KC UCiZtj9HjyudBwC2TywG0GzQ

import json
import pandas as pd 
from googleapiclient.discovery import build
 
'''
!!!! Usefull links !!!!! 
https://github.com/googleapis/google-api-python-client
https://github.com/youtube/api-samples
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost
 
pip install --upgrade google-api-python-client
 
https://github.com/googleapis/google-cloud-python
'''
print('Hello,world!!!')
 
 
API_KEY = ###
 
'''
Get YouTube API service w API Key only
'''
def get_service():
    service = build('youtube', 'v3', developerKey=API_KEY)
    return service
 
'''
Get Channel Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/channels/list
 
Type og Channels Urls
https://www.youtube.com/channel/UCXlhVxzpYqr2WguSWbzRNMw
https://www.youtube.com/c/tntonlineru
https://www.youtube.com/user/tn4east
but my script works only w channel_id (hash)
or w user/tn4east -> replace id=channel_id to forUsername='username'
'''
def get_channel_info(channel_id = 'UCiZtj9HjyudBwC2TywG0GzQ'):
    r = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
    # print(json.dumps(r))
    print(r['items'][0]['snippet']['title'])
    print(r['items'][0]['snippet']['publishedAt'])
    print(r['items'][0]['statistics']['viewCount'])
 
'''
Get Video Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/videos/list
'''
def get_video_info(video_id = 'JLu322-Dcow'):
    r = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
    # print(json.dumps(r['items']))
    descr=r['items'][0]['snippet']['description']
    # print(r['items'][1]['snippet']['title'])
    # print(r['items'][1]['statistics']['viewCount'])
    return descr
    
 
 
if __name__ == '__main__':
    # get_channel_info()
    #get_channel_info('UCiZtj9HjyudBwC2TywG0GzQ')
    #get_video_info('OXtOhjeiTzw')
    #video_id='OXtOhjeiTzw'
    #print(r['items'])
    #r = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
    
    #video_id = 'JLu322-Dcow'
    #print(r['items'][0]['snippet']['description'])
    channel_id = 'UCiZtj9HjyudBwC2TywG0GzQ'
    # # request = youtube.channels().list(
    # #     part="contentDetails",
    # #     forUsername="username",
    # #     # id="oiwuereru8987",
    # # )
    # # request = get_service().playlists().list(
    # #     part="snippet",
    # #     channelId=channel_id
    # # )
    # # response = request.execute()

    # # print(response['items'][0]['id'])

    # #print(response)

    list_videos=[]
    

 
    r = get_service().search().list(
        channelId=channel_id,
        part="snippet",
        type='video',
        order='rating',
        maxResults="50"
        # publishedAfter=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat(),
        # publishedBefore=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    ).execute()
 
    # print(json.dumps(r))
    for item in r['items']:   
        list_videos.append(item['id']['videoId'])


    #print(f"nextPageToken {r['nextPageToken']}")

    # [print("%s, %s" % (item['snippet']['title'], item['id']['videoId'])) for item in r['items']]

    r = get_service().search().list(
        channelId=channel_id,
        part="snippet",
        type='video',
        order='rating',
        maxResults="50",
        pageToken=r['nextPageToken']
        # publishedAfter=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat(),
        # publishedBefore=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    ).execute()

    for item in r['items']:   
        list_videos.append(item['id']['videoId'])

    r = get_service().search().list(
        channelId=channel_id,
        part="snippet",
        type='video',
        order='rating',
        maxResults="50",
        pageToken=r['nextPageToken']
        # publishedAfter=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat(),
        # publishedBefore=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    ).execute()

    for item in r['items']:   
        list_videos.append(item['id']['videoId'])


    r = get_service().search().list(
        channelId=channel_id,
        part="snippet",
        type='video',
        order='rating',
        maxResults="50",
        pageToken=r['nextPageToken']
        # publishedAfter=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat(),
        # publishedBefore=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    ).execute()

    for item in r['items']:   
        list_videos.append(item['id']['videoId'])


    # #[print("%s, %s, https://youtu.be/%s" % (item['snippet']['title'], item['snippet']['publishedAt'], item['id']['videoId'])) for item in r['items']]
    # [print("%s, %s" % (item['snippet']['title'], item['id']['videoId'])) for item in r['items']]
    
    descr_list=dict()

    #print(type(r['items']))
    #print(list_videos)
    for id in list_videos:
        descr=get_video_info(id)
        descr_list['https://youtu.be/'+str(id)]=descr
        #descr_list[id]=descr

#    for i in descr_list:
 #       print (i, descr_list[i])   
#descr_list[new_key] = dictionary[old_key]
#del dictionary[old_key]
#descr_list.to_excel("C:\Users\Илья\Documents\KC_Simulator\CyberTolya\videos.xlsx")
#df = pd.DataFrame([descr_list])
#print(descr_list)
df=pd.DataFrame(descr_list.items(), columns=['link', 'Description'])
#print(df.head)
df.to_excel(r"C:\Users\Илья\Documents\KC_Simulator\CyberTolya\video_descr.xlsx")