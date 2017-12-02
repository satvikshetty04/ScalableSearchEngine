import boto3
import time
import uuid
import pickle
from elasticsearch import Elasticsearch, RequestsHttpConnection
from nltk.corpus import stopwords
from config import kinesis_stream_name as ksn, es_endpoint, s3_bucket, model_file_name
import pandas as pd
#
# categories = ['alt.atheism', 'sci.space', 'comp.graphics',
#               'rec.motorcycles', 'sci.electronics']
# AWS Clients
s3 = boto3.client("s3")
kinesis = boto3.client("kinesis")
es = Elasticsearch(
    hosts = [{'host': es_endpoint, 'port': 443}],
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

tmp_dir = './data'
stopwords = set(stopwords.words('english'))

def load_classifier():
    filename = '%s/%s.txt' %(tmp_dir, str(uuid.uuid4()))
    s3.download_file(s3_bucket, model_file_name, filename)
    return pickle.load(open(filename, 'rb'))

def classify(data, clf):
    features, model = clf["features"], clf["model"]
    df = pd.DataFrame()
    # print([str(data, 'utf-8')])
    df['news_overall'] = [data]
    print(df)
    for word in features:
        df[word] = df['news_overall'].str.count(word)
    df.drop(['news_overall'], axis=1, inplace=True)

    return model.predict(df)[0]

def put_s3(data):
    unique = str(uuid.uuid4()) + '.txt'
    filename = '%s/%s.txt' %(tmp_dir, unique)
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    s3.upload_file(filename, s3_bucket, unique)
    return unique

def create_es_index(filename, data, pred):
    clean_data = []
    for word in data.split():
        if word not in stopwords:
            clean_data.append(word.lower())
    es.index(index="news", doc_type="news", body={
        'link': filename,
        'text': ' '.join(clean_data),
        'category': pred
    })
    return

def consume_kinesis():
    kinesis = boto3.client("kinesis")
    describe = kinesis.describe_stream(
        StreamName=ksn
    )
    shard_id = describe['StreamDescription']['Shards'][0]['ShardId']
    shard_it =  kinesis.get_shard_iterator(
        StreamName=ksn,
        ShardId=shard_id,
        ShardIteratorType="LATEST"
    )["ShardIterator"]
    i = 0
    print("=" * 60)
    print("Ready to consume. Start putting into kinesis stream.")
    print("Might take a while after records put into kinesis.")
    print("=" * 60)
    while True:
        out = kinesis.get_records(
            ShardIterator=shard_it,
            Limit=10
        )
        clf = load_classifier()
        for record in out['Records']:
            i += 1
            pred = classify(str(record['Data'],'utf-8'), clf)
            filename = "https://s3.amazonaws.com/"+ s3_bucket +"/" + put_s3(record['Data'])
            print(str(i), pred, filename)
            create_es_index(filename, str(record['Data'],'utf-8'), pred)

        time.sleep(1) # This is needed as there is a limit to number of requests we can make
        shard_it = out["NextShardIterator"]

consume_kinesis()
