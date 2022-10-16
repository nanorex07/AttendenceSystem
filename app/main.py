from fastapi import FastAPI, staticfiles
from numpy import record
from .routers import community, auth, member, records
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(todo.router)
app.include_router(community.router)
app.include_router(auth.router)
app.include_router(member.router)
app.include_router(records.router)


@app.get("/")
def home():
    return {"message": " /docs for documentation "}
