from fastapi import APIRouter, HTTPException, status
import schemas
import mongo
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate):
    if mongo.users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    result = mongo.users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    user_dict["username"] = user.username
    user_dict["email"] = user.email
    return user_dict

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin):
    db_user = mongo.users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/playlists", response_model=schemas.PlaylistOut)
def create_playlist(playlist: schemas.PlaylistCreate):
    playlist_dict = playlist.dict()
    result = mongo.playlists_collection.insert_one(playlist_dict)
    playlist_dict["id"] = str(result.inserted_id)
    return playlist_dict

@router.get("/playlists", response_model=list[schemas.PlaylistOut])
def list_playlists():
    playlists = list(mongo.playlists_collection.find())
    for p in playlists:
        p["id"] = str(p["_id"])
    return playlists

@router.get("/playlists/user/{user_id}", response_model=list[schemas.PlaylistOut])
def get_user_playlists(user_id: int):
    playlists = list(mongo.playlists_collection.find({"user_id": user_id}))
    for p in playlists:
        p["id"] = str(p["_id"])
    return playlists

@router.post("/songs", response_model=schemas.SongOut)
def create_song(song: schemas.SongCreate):
    song_dict = song.dict()
    result = mongo.songs_collection.insert_one(song_dict)
    song_dict["id"] = str(result.inserted_id)
    return song_dict

@router.get("/songs", response_model=list[schemas.SongOut])
def list_songs():
    songs = list(mongo.songs_collection.find())
    for s in songs:
        s["id"] = str(s["_id"])
    return songs

@router.get("/songs/{song_id}", response_model=schemas.SongOut)
def get_song(song_id: str):
    song = mongo.songs_collection.find_one({"_id": ObjectId(song_id)})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    song["id"] = str(song["_id"])
    return song
