from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "author": "Samuel Teshale",
        "title": "Welcome to My FastAPI Blog",
        "content": "Hello! My name is Samuel Teshale. This is my first FastAPI blog project.",
        "date_posted": "July 8, 2026",
    },
    {
        "id": 2,
        "author": "Samuel Teshale",
        "title": "Learning FastAPI",
        "content": "FastAPI is fast, modern, and easy to learn.",
        "date_posted": "July 8, 2026",
    },
]


@app.get("/")
@app.get("/posts")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "title": "Samuel Teshale Blog",
            "posts": posts,
        },
    )


@app.get("/api/posts")
async def get_posts():
    return posts