import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.app import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
