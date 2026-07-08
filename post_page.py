from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

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


@app.get("/posts/{post_id}", include_in_schema=False)
async def post_page(request: Request, post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return templates.TemplateResponse(
                request=request,
                name="post.html",
                context={
                    "title": post["title"][:50],
                    "post": post,
                },
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
    )


@app.get("/api/posts")
async def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
    )


# -------------------------------
# Starlette HTTP Exception Handler
# -------------------------------
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


# -----------------------------------
# Request Validation Exception Handler
# -----------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )