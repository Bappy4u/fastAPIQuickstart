from typing import Annotated

from fastapi import BackgroundTasks, Form, Response

from models.models import FormData
from utils.email_utils import send_email


def login(data: Annotated[FormData, Form()], response: Response, background_tasks: BackgroundTasks):
    response.set_cookie(key="session_id", value="abc123")
    background_tasks.add_task(
        send_email,
        email=f"{data.username}@example.com",
        subject="Welcome to BookStore",
        body=f"Hi {data.username}, you have successfully logged in."
    )
    return {"message": "Logged in"}