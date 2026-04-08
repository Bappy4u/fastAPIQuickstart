from typing import Annotated

from fastapi import BackgroundTasks, Form, Response

from models.models import FormData
from utils.email_utils import send_email


def signup(data: Annotated[FormData, Form()], response: Response, background_tasks: BackgroundTasks):
    # In a real application, you would save the user to a database
    # For now, we'll just simulate user registration
    response.set_cookie(key="session_id", value="abc123")
    background_tasks.add_task(
        send_email,
        email=f"{data.username}@example.com",
        subject="Welcome to BookStore - Account Created",
        body=f"Hi {data.username}, your account has been successfully created."
    )
    return {"message": "Account created successfully", "username": data.username}