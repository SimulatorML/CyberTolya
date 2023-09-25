from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd
import pickle
from typing import List

from src.utils.preprocess import preprocess_text

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bm25_ranking')


def train_model(corpus: List):
    """
    Args:
        corpus (List): str
    """
    bm_25 = BM25Okapi(corpus)
    with open('../src/model', 'wb') as bm25result_file:
        pickle.dump(bm_25, bm25result_file)


def predict_with_trainde_model(message: str, path_to_model):
    with open(path_to_model, 'rb') as bm25result_file:
        bm25_result = pickle.load(bm25result_file)
    message = preprocess_text(message)
    scores = bm25_result.get_scores(message)
    index = np.argmax(scores)
    logger.info(f"Predict {index}")


if __name__ == "__main__":
    df = pd.read_excel('../file/video_descr.xlsx')
    links = df['link']