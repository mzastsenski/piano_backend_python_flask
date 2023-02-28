from __main__ import app
from flask import request, Response
from pymongo import MongoClient
from decouple import config
from middleware import check_token
uri = config('MONGO_URI')
PREFIX = "/api"
projection = {'_id': 0}


@app.route(PREFIX + '/getSongs/<user>', methods=['GET'])
@check_token()
def get_product(user):
    client = MongoClient(uri)
    collection = client["piano"]["songs"]
    arr = []
    for x in collection.find({"user": user}, projection):
        arr.append(x)
    client.close()
    return arr


@app.route(PREFIX + '/post', methods=['POST'])
@check_token()
def post():
    client = MongoClient(uri)
    collection = client["piano"]["songs"]
    data = {
        "id": float(request.json['id']),
        "user": request.json['user'],
        "title": request.json['title'],
        "song": request.json['song'],
    }
    collection.insert_one(data)
    client.close()
    return Response('200', status=200)


@app.route(PREFIX + '/edit', methods=['PUT'])
@check_token()
def edit():
    client = MongoClient(uri)
    collection = client["piano"]["songs"]
    collection.update_one(
      {"id": request.json['id']},
      {"$set": {"title": request.json['title']}}
    )
    client.close()
    return Response('200', status=200)


@app.route(PREFIX + '/delete', methods=['DELETE'])
@check_token()
def delete():
    client = MongoClient(uri)
    collection = client["piano"]["songs"]
    collection.delete_one({"id": request.json['id']})
    client.close()
    return Response('200', status=200)