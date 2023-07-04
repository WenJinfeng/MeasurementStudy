
import azure.functions as func
import boto3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
# from sklearn.externals import joblib
import joblib
import json
import pandas as pd
from time import time
import re
import io

s3_client = boto3.client('s3', aws_access_key_id="AKIAUMD2BUWBSHVKCSPR",                          aws_secret_access_key="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",       region_name="us-east-1")

cleanup_re = re.compile('[^a-z]+')

tmp = '/tmp/'

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def main(req: func.HttpRequest) -> func.HttpResponse:
    tm_st = time() * 1000
    
    dataset_bucket = "cynthiaeastbucket"
    dataset_object_key = "reviews20mb.csv"
    model_bucket = "cynthiaeastbucket1"
    model_object_key = "lr_model_new.pk"  # example : lr_model_new.pk
    # model_object_key ="lr_model.pk"

    obj = s3_client.get_object(Bucket=dataset_bucket, Key=dataset_object_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    # df = pd.read_csv("reviews20mb.csv")

    start = time()
    df['train'] = df['Text'].apply(cleanup)

    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])

    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression()
    model.fit(train, df['Score'])
    latency = time() - start

    model_file_path = tmp + model_object_key
    # model_file_path = model_object_key
    joblib.dump(model, model_file_path)

    s3_client.upload_file(model_file_path, model_bucket, model_object_key)

  
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

