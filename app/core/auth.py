import os
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    elif api_key == os.getenv("DEFECT_TRACKER_API_KEY"):
        return api_key
    else:
        raise HTTPException(status_code=401, detail="Could not validate API key")
    
