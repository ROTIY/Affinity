from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str


class SongCreate(BaseModel):
    title: str
    artist: str
    album: str
    file_url: str

class SongOut(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    file_url: str
    class Config:
        orm_mode = True


class PlaylistCreate(BaseModel):
    name: str
    user_id: int

class PlaylistOut(BaseModel):
    id: int
    name: str
    user_id: int
    class Config:
        orm_mode = True
