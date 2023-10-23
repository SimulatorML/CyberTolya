from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd
import pickle
from typing import List
from pymystem3 import Mystem
import nltk
from nltk.corpus import stopwords
from string import punctuation
nltk.download('stopwords')

import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bm25_ranking')


mystem = Mystem()
rus_stopwords = stopwords.words('russian')

data_path_file="files/video_dataset.xlsx"

model_path_desc = "src/model/bm25_result_desc.pkl"
model_path_title = "src/model/bm25_result_title_test.pkl"

def preprocess_text(text: str) -> List:
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in rus_stopwords
              and token != " "
              and token.strip() not in punctuation
              and token != 'https'
              and token != '://'
              and not token.isdigit()]
    return tokens


def train_model(model_type: str,path_to_file=data_path_file):
    """
    Args:
        corpus (List): str
    """
    df=pd.read_excel(path_to_file)
    corpus = list(df[model_type]) 
    preprocessed_corpus=[]
    corpus=corpus[:10]
    #i для контроля выполнения
    i=0
    for cor in corpus:
        lemmas=preprocess_text(cor)
        preprocessed_corpus.append(lemmas)
        print('finished',i)
        i=i+1
    print("training finished")
    bm_25 = BM25Okapi(corpus)
    with open(model_path_title, 'wb') as bm25result_file:
        pickle.dump(bm_25, bm25result_file)


def predict_with_trainde_model(message: str, path_to_model):
    with open(path_to_model, 'rb') as bm25result_file:
        bm25_result = pickle.load(bm25result_file)
    message = preprocess_text(message)
    scores = bm25_result.get_scores(message)
    index = np.argmax(scores)
    logger.info(f"Predict {index}")


if __name__ == "__main__":
    #обучение модели на датасете с описаниями/названиями видео (работает некоторое продолжительное время на ПК)
    
    train_model('title')
    #train_model('description')

       
