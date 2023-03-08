from __main__ import app
from flask import request, Response, make_response
from pymongo import MongoClient
from decouple import config
from datetime import datetime
import bcrypt
import json
import jwt
from middleware import check_token
PREFIX = "/api"
uri = config('MONGO_URI')
projection = {'_id': 0}


@app.route(PREFIX + '/login', methods=['POST'])
def login():
    user = request.json['user']
    user_pass = request.json['pass']
    client = MongoClient(uri)
    users = client["piano"]["users"]
    target_user = users.find_one({"user": user}, projection)
    if target_user:
        checked = bcrypt.checkpw(user_pass.encode(), target_user["pass"].encode())
        if checked:
            time = datetime.now().timestamp()
            secret = config('ACCESS_TOKEN_SECRET')
            token = jwt.encode({"name": user, "time": time}, secret, algorithm='HS256')
            response = make_response("200")
            response.set_cookie("token", token, httponly=True, max_age=7*24*3600)
            return response
        else:
            return make_response("401", 401)
    else:
        return Response('401', status=401)


@app.route(PREFIX + '/signUp', methods=['POST'])
def sign_up():
    user = request.json['user']
    client = MongoClient(uri)
    users = client["piano"]["users"]
    target_user = users.find_one({"user": user}, projection)
    if target_user:
        return Response('401', status=401)
    else:
        pass_hash = bcrypt.hashpw(request.json['pass'].encode(), bcrypt.gensalt())
        default_song = json.load(open('data/default_song.json'))
        users.insert_one({ "user": user, "pass": pass_hash.decode()})
        songs = client["piano"]["songs"]
        songs.insert_one({
            "id": datetime.now().timestamp(),
            "user": user,
            "title": "Elise",
            "song": default_song
        })
    client.close()
    return Response('200', status=200)


@app.route(PREFIX + '/checkUser', methods=['POST'])
@check_token()
def check_user():
    return "200"


@app.route(PREFIX + '/logout', methods=['POST'])
def logout():
    response = make_response("200", 200)
    response.delete_cookie('token')
    return response
