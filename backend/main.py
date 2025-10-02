from fastapi import FastAPI
import routers

app = FastAPI()

app.include_router(routers.router)

@app.get("/")
def read_root():
    return {"message": "Affinity Music App Backend"}
