from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://roymatiyit_db_user:HdHF5zSzxO81oh0b@googmaus.zecrrjy.mongodb.net/?retryWrites=true&w=majority&appName=Googmaus"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["affinity_music_app"]

# Collections
users_collection = db["users"]
songs_collection = db["songs"]
playlists_collection = db["playlists"]
