from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json

s3 = boto3.client('s3')

print('Loading function')

indexDoc = {
    "dataRecord" : {
        "properties" : {
          "createdDate" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "objectKey" : {
            "type" : "string"
          },
          "content_type" : {
            "type" : "string"
          },
          "content_length" : {
            "type" : "long"
          },
          "metadata" : {
            "type" : "string"
          }
        }
      },
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
      }
    }


def connectES(esEndPoint):
    print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
    try:
        esClient = Elasticsearch(
            hosts=[{'host': esEndPoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        return esClient
    except Exception as E:
        print("Unable to connect to {0}".format(esEndPoint))
        print(E)
        exit(3)

def createIndex(esClient):
    try:
        res = esClient.indices.exists('metadata-store')
        if res is False:
            esClient.indices.create('metadata-store', body=indexDoc)
	    return 1
    except Exception as E:
            print("Unable to Create Index {0}".format("metadata-store"))
            print(E)
            exit(4)

def indexDocElement(esClient,key,response):
    try:
	indexObjectKey = key
	indexcreatedDate = response['LastModified']
	indexcontent_length = response['ContentLength']
	indexcontent_type = response['ContentType']
	indexmetadata = json.dumps(response['Metadata'])
	retval = esClient.index(index='metadata-store', doc_type='documents', body={
    		'createdDate': indexcreatedDate,
    		'objectKey': indexObjectKey,
    		'content_type': indexcontent_type,
    		'content_length': indexcontent_length,
    		'metadata': indexmetadata
	})
    except Exception as E:
	print("Document not indexed")
	print("Error: ",E)
	exit(5)



def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    esClient = connectES("search-documents-6imwg72yhi3d65jrcdckpjruzi.us-east-1.es.amazonaws.com")
    createIndex(esClient)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
	indexDocElement(esClient,key,response)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
