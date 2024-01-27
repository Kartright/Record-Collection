import os
import sys
import base64
from requests import post, get
from dotenv import load_dotenv
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_album(token, album_title):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_title}&type=album&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]

    if len(json_result) == 0:
        print("No album with this name exists.")
        return None
    
    return json_result[0]


def get_album_tracks(token, id):
    url = f"https://api.spotify.com/v1/albums/{id}/tracks?&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def main():
    token = get_token()
    album_dict = user_album_dict()
    for artist in album_dict:
        print("-"*100)
        print(artist)
        print("-"*100)
        for album in album_dict[artist]:
            print(album)
            result = get_album(token,album)
            result_id = result["id"]
            tracks_info = get_album_tracks(token, result_id)
            num_of_tracks = tracks_info["total"]
            for i in range(num_of_tracks):
                name = tracks_info["items"][i]["name"]
                print(f"{i+1}. {name}")


def user_album_dict():
    f = open("record-list.txt",'r')
    album_dict = {}
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line == '':
            pass
        elif line[-1] == ':':
            artist = line[:-1]
            album_dict[artist] = []
        else:
            album_dict[artist].append(line)
    return album_dict

main()



