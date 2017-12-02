import boto3
from sklearn.datasets import fetch_20newsgroups
from random import *
from config import kinesis_stream_name as ksn
import time
import pandas as pd

# categories = ['alt.atheism', 'sci.space', 'comp.graphics',
#               'rec.motorcycles', 'sci.electronics']
# news = fetch_20newsgroups(remove=("headers", "footers", "quotes"),
#                           categories=categories)
news = pd.read_csv(".//data//articles3.csv", usecols=[9])

kinesis = boto3.client("kinesis")

def handle_kinesis():
    # df = pd.DataFrame()
    # df['news_overall'] = news.loc[randint(0, len(news)-1)]
    response = kinesis.put_record(
        Data=news.loc[randint(0, len(news)-1)][0],
        StreamName=ksn,
        PartitionKey="partition_1"
    )
i = 0
while True:
    i += 1
    handle_kinesis()
    print("Putting Record %d into Kinesis" %(i))
    if i % 10 == 0:
        time.sleep(1)
