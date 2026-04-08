from typing import Optional

from fastapi import Cookie, HTTPException


def get_profile(session_id: Optional[str] = Cookie(None)):
    if session_id != "abc123":
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"message": "Welcome user"}