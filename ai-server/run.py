from dotenv import load_dotenv
load_dotenv()

from app import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True, workers=2)