from fastapi import Header, HTTPException
from typing_extensions import Optional
from secrets import SECRET_KEY

# Dependency to handle API key authentication
def api_key_auth(api_key: Optional[str] = Header(None)):
    if api_key != SECRET_KEY:  # You can replace with your custom logic
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key