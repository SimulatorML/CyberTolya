from pymystem3 import Mystem
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
from rank_bm25 import BM25Okapi
import numpy as np
import pickle
import json
from typing import List
from bs4 import BeautifulSoup

import pandas as pd 
from googleapiclient.discovery import build

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('predict_with_trained_model')

mystem = Mystem()
rus_stopwords = stopwords.words('russian')
model_path_desc = "src/model/bm25_result_desc.pkl"
model_path_title = "src/model/bm25_result_title.pkl"
db_path = "db/links.json"
API_KEY='Lu322-Dc234'

'''
Get YouTube API service w API Key only
'''
def get_service():
    service = build('youtube', 'v3', developerKey=API_KEY)
    return service

def get_video_info(video_id: str = 'JLu322-Dcow'):
    """
    Get video description by id
    """
    r = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
    # print(json.dumps(r['items']))
    descr=r['items'][0]['snippet']['description']
    # print(r['items'][1]['snippet']['title'])
    # print(r['items'][1]['statistics']['viewCount'])
    return descr


def get_channel_videos_info(channel_id: str = 'UCiZtj9HjyudBwC2TywG0GzQ'):
    """
    Get dataframe by videos of the channel in style link-description (then we put it in excel-file)
    """
    list_videos=[]
    #We make a cycle because there is a limit by taking videos for one time
    r=None
    counter=4
    for i in range(counter):
        if r is not None:
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
        else:
            r = get_service().search().list(
            channelId=channel_id,
            part="snippet",
            type='video',
            order='rating',
            maxResults="50"
            # publishedAfter=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat(),
            # publishedBefore=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
            ).execute()
        for item in r['items']:   
            list_videos.append(item['id']['videoId'])
    
    descr_list=dict()
    for id in list_videos:
        descr=get_video_info(id)
        descr_list['https://youtu.be/'+str(id)]=descr
    df_video=pd.DataFrame(descr_list.items(), columns=['link', 'Description'])

    return df_video



def preprocess_text(text: str) -> List:
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in rus_stopwords
              and token != " "
              and token.strip() not in punctuation]
    return tokens


def predict_with_trained_model(message: str,
                               path_to_model_desc=model_path_desc,
                               path_to_model_title=model_path_title,
                               path_to_links=db_path):
    with open(path_to_model_desc, 'rb') as bm25result_file:
        bm25_desc = pickle.load(bm25result_file)
    with open(path_to_model_title, 'rb') as bm25result_file:
        bm25_title = pickle.load(bm25result_file)

    message = preprocess_text(message)

    scores_desc = bm25_desc.get_scores(message)
    index_desc = list(map(str, np.argsort(scores_desc)[-3:]))

    scores_title = bm25_title.get_scores(message)
    index_title = list(map(str, np.argsort(scores_title)[-3:]))

    index = index_desc + index_title

    score = []
    for ind in index:
        score.append((max(scores_desc[int(ind)], scores_title[int(ind)]), ind))
    score = sorted(list(set(score)), key=lambda tup: tup[0], reverse=True)[:3]

    with open(path_to_links, "r") as read_file:
        links = json.load(read_file)

    counter=1    
    result = 'Вот что я нашел по данному запросу: \n'
    for scr in score:
        if scr[0] > 0:
            result += f"{counter}. "+f'<a href="{links[scr[1]]["link"]}">{links[scr[1]]["title"]}</a>' + "\n"
            counter=counter+1
    return result