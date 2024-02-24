from pymystem3 import Mystem
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
from rank_bm25 import BM25Okapi
import numpy as np
import asyncio
import pickle
import json
import random
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
    Get dataframe from channel in form link-title-description
    """
    list_videos=[]
    #Cycle because it is maximum 50 for one time
    counter=5
    for i in range(counter):
        print(i)
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
    #print('data prepare')
    df=pd.DataFrame(columns=['link','title', 'Description'])
    for id in list_videos:
        descr,title=get_video_info(id)
        #print(id)
        link='https://youtu.be/'+str(id)
        df_temp=pd.DataFrame([{'link':link,'title':title,'Description':descr}])
        df = pd.concat([df, df_temp], ignore_index=True)
    return df

def make_json(file_path: str) -> json:
    #строка для получения links.json 
    df = pd.read_excel(file_path, index_col=False)
    title = list(df['title'])
    link = list(df['link'])
    #links = ['https://youtu.be/' + l for l in link]
    json_dict = {}
    for i in range(df.shape[0]):
        json_dict[str(i)] = {"link": link[i], "title": title[i]}   
    with open(db_path, "w") as read_file:
        json.dump(json_dict, read_file)

async def preprocess_text(text: str) -> List:
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in rus_stopwords
              and token != " "
              and token.strip() not in punctuation
              and token != 'https'
              and token != '://'
              and not token.isdigit()]
    return tokens


async def predict_with_trained_model(message: str,
                               path_to_model_desc=model_path_desc,
                               path_to_model_title=model_path_title,
                               path_to_links=db_path):
    with open(path_to_model_desc, 'rb') as bm25result_file:
        bm25_desc = pickle.load(bm25result_file)
    with open(path_to_model_title, 'rb') as bm25result_file:
        bm25_title = pickle.load(bm25result_file)

    message =await preprocess_text(message)

    scores_desc = bm25_desc.get_scores(message)
    index_desc = list(map(str, np.argsort(scores_desc)[-3:]))

    scores_title = bm25_title.get_scores(message)
    index_title = list(map(str, np.argsort(scores_title)[-3:]))
    #print('descr',scores_desc)
    #print('title',scores_title)


    index = index_desc + index_title

    score = []
    for ind in index:
        score.append((max(scores_desc[int(ind)], scores_title[int(ind)]), ind))
    score = sorted(list(set(score)), key=lambda tup: tup[0], reverse=True)[:3]
    #print("score_itog",score)

    #обрезаем где скор слишком маленький
    score = [item for item in score if item[0] > 3]


    with open(path_to_links, "r") as read_file:
        links = json.load(read_file)

    counter=1
    if len(score)>0:
        result = 'Вот что я нашел по данному запросу: \n'
    else:
        score = [(random.uniform(1, 5), str(random.randint(1, 230))) for i in range(3)]
        result = 'К сожалению, я ничего не нашел по твоему запросу и поэтому подберу тебе случайные видео.\nВозможно, они тебя заинтересуют. \n'
    for scr in score:
        result += f"{counter}. "+f'<a href="{links[scr[1]]["link"]}">{links[scr[1]]["title"]}</a>' + "\n"
        counter=counter+1
    return result